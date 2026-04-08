"""
GenBI Chat Agent - Text-2-SQL with Data Lineage Awareness
Simple Python agent using Amazon Bedrock LLM + Knowledge Base RAG

Flow:
1. User asks a business question
2. Agent retrieves relevant schema/lineage/SQL context from Bedrock KB
3. Agent generates SQL query using Bedrock LLM
4. Agent executes SQL against Redshift
5. Agent formats response with data lineage explanation
"""

import json
import boto3
import time
import re

# AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
redshift_data = boto3.client('redshift-data', region_name='us-east-1')

# Configuration
KB_ID = "MYUSWRTES8"
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"  # Can be swapped with any Bedrock-supported model (Anthropic, Amazon Titan, Meta Llama, etc.)
WORKGROUP = "demo-sales-related"
DATABASE = "dev"
SCHEMA = "genbi_mart"


def retrieve_context(question: str, num_results: int = 5) -> str:
    """Retrieve relevant context from Bedrock Knowledge Base"""
    response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={'text': question},
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': num_results
            }
        }
    )

    contexts = []
    for result in response.get('retrievalResults', []):
        text = result.get('content', {}).get('text', '')
        if text:
            contexts.append(text)

    return "\n\n---\n\n".join(contexts)


def generate_sql(question: str, context: str) -> dict:
    """Generate SQL query using Bedrock LLM with RAG context"""
    system_prompt = """You are a SQL expert for the ABC Restaurant Group data warehouse.
You generate Redshift SQL queries based on the schema in genbi_mart.

RULES:
1. Always use fully qualified table names: genbi_mart.table_name
2. Always JOIN fact tables to dim_date using date_key for date filtering
3. Use COUNT(DISTINCT transaction_id) for order counts (fact_sales has one row per line item)
4. All monetary values are in HKD (Hong Kong Dollars)
5. Hong Kong has no sales tax
6. Return SQL that is ready to execute - no placeholders
7. Include comments explaining the query logic
8. For date filtering, use dim_date.full_date with date literals

JOIN KEY RULES (CRITICAL):
- Fact tables use NATURAL keys: store_id, item_id, channel_id, payment_method_id, customer_id
- Dim tables use SURROGATE keys: store_key, item_key, channel_key, payment_key
- JOIN fact to dim_store ON fact.store_id = dim_store.store_id
- JOIN fact to dim_menu_item ON fact.item_id = dim_menu_item.item_id
- JOIN fact to dim_channel ON fact.channel_id = dim_channel.channel_id
- JOIN fact to dim_payment_method ON fact.payment_method_id = dim_payment_method.payment_method_id
- JOIN fact to dim_date ON fact.date_key = dim_date.date_key (both use date_key)
- NEVER use store_key, item_key, channel_key, payment_key for joins with fact tables
- fact_customer_feedback PK is feedback_key (NOT feedback_id)
- fact_sales PK is sale_key, fact_labor PK is labor_key, fact_financial PK is financial_key

DASHBOARD RECOMMENDATION:
When the user's question relates to a specific business area, recommend the most relevant dashboard tab.
Available dashboards:
- Executive Summary (genbi-exec-dashboard): overall performance, revenue, regional comparisons, monthly trends
- Sales & Menu (genbi-sales-dashboard): menu items, categories, channels, payment methods, hourly sales
- Operations (genbi-ops-dashboard): labor costs, staffing, shift productivity, workforce utilization
- Customer Intelligence (genbi-cust-dashboard): satisfaction, CSAT, NPS, sentiment, ratings
- Financial Performance (genbi-fin-dashboard): EBITDA, net profit, margins, cost structure, P&L

DATA LINEAGE (CRITICAL - provide end-to-end pipeline trace):
When explaining data lineage, trace the FULL pipeline for every metric in your query.
Format the lineage with clear line breaks between each stage for easy reading.
Use this EXACT format with newlines between stages:

"Source System: [system name] ([description]) →\n\nS3 Raw Landing:\n[s3 path 1] ([file description]) AND\n[s3 path 2] ([file description]) →\n\nGlue ETL ([job name]): [transformation description] →\n\nRedshift [schema.table]:\n[row count] rows, grain = [one row per what] →\n\nDashboard Aggregation:\n[aggregation function and why]"

Example lineage for "total orders":
"Source System: POS terminals (McDonald's Hong Kong store registers) →\n\nS3 Raw Landing:\ns3://genbi-mcdhk-raw-530977327410/pos/transactions/ (monthly CSV: pos_transactions_YYYY_MM.csv contains transaction headers with transaction_id, store_id, order_date, channel_id, etc.) AND\ns3://genbi-mcdhk-raw-530977327410/pos/line_items/ (pos_line_items_YYYY_MM.csv contains line-level details: item_id, quantity, unit_price, line_total) →\n\nGlue ETL (load_fact_sales): Joins pos_transactions + pos_line_items ON transaction_id (INNER JOIN), creates one row per line item, casts order_date to date_key INT →\n\nRedshift genbi_mart.fact_sales:\n17.5M rows, grain = one row per line item per transaction →\n\nDashboard Aggregation:\nCOUNT(DISTINCT transaction_id) to convert from line-item grain to order grain (final metric = number of unique orders)"

TOPIC GUARDRAILS:
You are ONLY allowed to answer questions related to restaurant operations and dashboard analytics.
Allowed topics include: restaurant sales, revenue, orders, menu items, inventory, labor/staffing,
service performance, customer feedback/satisfaction, loyalty programs, equipment maintenance,
financial P&L, and dashboard navigation.

If the user asks about anything unrelated to restaurant operations (e.g., politics, weather,
personal advice, coding help, general knowledge, or any off-topic subject), do NOT generate SQL.
Instead, respond with this exact JSON:
{
    "sql": null,
    "explanation": "I'm the ABC Restaurant GenBI Assistant, specialized in restaurant operations analytics. I can help with questions about sales, revenue, orders, menu performance, inventory, labor costs, customer satisfaction, financial P&L, and more. Please ask a question related to restaurant operations!",
    "lineage": null,
    "assumptions": null,
    "recommended_dashboard": null
}

Respond in JSON format:
{
    "sql": "the SQL query",
    "explanation": "brief explanation of what the query does",
    "lineage": "end-to-end pipeline trace formatted with newlines between each stage: Source System → S3 Raw Landing → Glue ETL → Redshift → Dashboard Aggregation",
    "assumptions": "any assumptions made about the question",
    "recommended_dashboard": "name of the most relevant dashboard tab (or null if not applicable)"
}"""

    user_message = f"""Context from knowledge base:
{context}

User question: {question}

Generate a SQL query to answer this question. Include data lineage explanation."""

    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 4096,
            'system': system_prompt,
            'messages': [{'role': 'user', 'content': user_message}]
        })
    )

    result = json.loads(response['body'].read())
    text = result['content'][0]['text']

    # Parse JSON from response — find the first { and use raw_decode for robust parsing
    brace_idx = text.find('{')
    if brace_idx >= 0:
        decoder = json.JSONDecoder()
        parsed, _ = decoder.raw_decode(text, brace_idx)
        if parsed.get('sql'):
            parsed['sql'] = fix_generated_sql(parsed['sql'])
        return parsed
    return {"sql": text, "explanation": "", "lineage": "", "assumptions": ""}


def fix_generated_sql(sql: str) -> str:
    """Fix common LLM SQL mistakes before execution."""
    fixed = sql

    # Fix 1: Surrogate keys used on fact tables (should be natural keys)
    key_fixes = {
        'store_key': 'store_id',
        'item_key': 'item_id',
        'channel_key': 'channel_id',
        'payment_key': 'payment_method_id',
        'customer_key': 'customer_id',
    }
    for surrogate, natural in key_fixes.items():
        # Match fact table aliases (f, ff, fs, fl, sp, i, l, fb, etc.)
        fixed = re.sub(
            r'\b(f[a-z]?|fs|fl|sp|i|l|fb)\.' + surrogate + r'\b',
            r'\1.' + natural,
            fixed
        )

    # Fix 2: fact_financial uses month_key, not date_key
    # Find the alias for fact_financial, then replace alias.date_key with alias.month_key
    fin_alias_match = re.search(r'fact_financial\s+(?:AS\s+)?(\w+)', fixed, re.IGNORECASE)
    if fin_alias_match:
        alias = fin_alias_match.group(1)
        fixed = re.sub(
            r'\b' + re.escape(alias) + r'\.date_key\b',
            alias + '.month_key',
            fixed
        )

    return fixed


def execute_query(sql: str, timeout: int = 120) -> dict:
    """Execute SQL against Redshift and return results"""
    stmt = redshift_data.execute_statement(
        WorkgroupName=WORKGROUP,
        Database=DATABASE,
        Sql=sql
    )
    stmt_id = stmt['Id']

    # Poll for completion
    elapsed = 0
    while elapsed < timeout:
        desc = redshift_data.describe_statement(Id=stmt_id)
        status = desc['Status']
        if status == 'FINISHED':
            break
        elif status == 'FAILED':
            return {'error': desc.get('Error', 'Unknown error'), 'rows': [], 'columns': []}
        time.sleep(1)
        elapsed += 1

    if elapsed >= timeout:
        return {'error': 'Query timed out', 'rows': [], 'columns': []}

    # Get results
    result = redshift_data.get_statement_result(Id=stmt_id)
    columns = [col['name'] for col in result['ColumnMetadata']]

    rows = []
    for record in result['Records']:
        row = {}
        for i, field in enumerate(record):
            for dtype, value in field.items():
                if dtype != 'isNull' and value is not None:
                    row[columns[i]] = value
                    break
            else:
                row[columns[i]] = None
        rows.append(row)

    return {'columns': columns, 'rows': rows, 'error': None}


def format_results(query_result: dict, sql_info: dict) -> str:
    """Format query results with lineage explanation"""
    if query_result.get('error'):
        return f"❌ Query Error: {query_result['error']}\n\nSQL:\n```sql\n{sql_info.get('sql', 'N/A')}\n```"

    rows = query_result['rows']
    columns = query_result['columns']

    if not rows:
        return "No results found for your query."

    # Format as table
    output = []

    # Header
    header = " | ".join(f"{col:>15s}" for col in columns)
    output.append(header)
    output.append("-" * len(header))

    # Data rows (limit to 20)
    for row in rows[:20]:
        values = []
        for col in columns:
            val = row.get(col)
            if val is None:
                values.append(f"{'NULL':>15s}")
            elif isinstance(val, (int, float)):
                values.append(f"{val:>15,.2f}" if isinstance(val, float) else f"{val:>15,}")
            else:
                values.append(f"{str(val):>15s}")
        output.append(" | ".join(values))

    if len(rows) > 20:
        output.append(f"... ({len(rows) - 20} more rows)")

    result_table = "\n".join(output)

    # Build response
    response = f"""📊 **Results** ({len(rows)} rows)

```
{result_table}
```

📝 **What this shows**: {sql_info.get('explanation', 'N/A')}

🔍 **Data Lineage**: {sql_info.get('lineage', 'N/A')}"""

    if sql_info.get('assumptions'):
        response += f"\n\n⚠️ **Assumptions**: {sql_info['assumptions']}"

    return response


def chat(question: str) -> str:
    """Main chat function - processes a business question end-to-end"""
    # Step 1: Retrieve context from KB
    context = retrieve_context(question)

    # Step 2: Generate SQL with lineage
    sql_info = generate_sql(question, context)

    # Step 3: Execute query
    query_result = execute_query(sql_info['sql'])

    # Step 4: Format response
    return format_results(query_result, sql_info)


def main():
    """Interactive chat loop"""
    print("=" * 60)
    print("  ABC Restaurant Group - GenBI Chat Agent")
    print("  Ask business questions about sales, operations,")
    print("  customers, and financial performance.")
    print("  Type 'quit' to exit, 'sql' to see last SQL query.")
    print("=" * 60)
    print()

    last_sql = None

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break
        if question.lower() == 'sql' and last_sql:
            print(f"\nLast SQL:\n```sql\n{last_sql}\n```\n")
            continue

        print("\n🤔 Thinking...\n")

        try:
            # Retrieve context
            context = retrieve_context(question)

            # Generate SQL
            sql_info = generate_sql(question, context)
            last_sql = sql_info.get('sql', '')

            # Execute
            print("⚡ Running query...\n")
            query_result = execute_query(sql_info['sql'])

            # Format and display
            response = format_results(query_result, sql_info)
            print(response)
            print()

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
