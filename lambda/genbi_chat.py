"""
GenBI Chat Lambda - Text-2-SQL with Data Lineage Awareness
Packages the agent logic for AWS Lambda + API Gateway deployment.
"""

import json
import time
import re
import boto3

# AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
redshift_data = boto3.client('redshift-data', region_name='us-east-1')

# Configuration
KB_ID = "MYUSWRTES8"
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
WORKGROUP = "demo-sales-related"
DATABASE = "dev"
SCHEMA = "genbi_mart"

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}


def lambda_handler(event, context):
    """Lambda entry point for API Gateway proxy integration"""
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}

    try:
        body = json.loads(event.get('body', '{}'))
        question = body.get('question', '').strip()

        if not question:
            return response(400, {'error': 'No question provided'})

        t0 = time.time()

        # Step 1: Retrieve context from KB
        kb_context = retrieve_context(question)
        t1 = time.time()

        # Step 2: Generate SQL with lineage
        sql_info = generate_sql(question, kb_context)
        t2 = time.time()

        # Handle off-topic questions (no SQL generated)
        if not sql_info.get('sql'):
            return response(200, {
                'question': question,
                'sql': None,
                'explanation': sql_info.get('explanation', ''),
                'lineage': sql_info.get('lineage'),
                'assumptions': sql_info.get('assumptions'),
                'recommended_dashboard': sql_info.get('recommended_dashboard'),
                'columns': [],
                'rows': [],
                'error': None,
                'row_count': 0,
                'timing': {
                    'kb_retrieval': round(t1 - t0, 1),
                    'sql_generation': round(t2 - t1, 1),
                    'query_execution': 0,
                    'total': round(t2 - t0, 1)
                }
            })

        # Step 3: Execute query
        query_result = execute_query(sql_info['sql'])
        t3 = time.time()

        return response(200, {
            'question': question,
            'sql': sql_info.get('sql', ''),
            'explanation': sql_info.get('explanation', ''),
            'lineage': sql_info.get('lineage', ''),
            'assumptions': sql_info.get('assumptions', ''),
            'recommended_dashboard': sql_info.get('recommended_dashboard'),
            'columns': query_result.get('columns', []),
            'rows': query_result.get('rows', []),
            'error': query_result.get('error'),
            'row_count': len(query_result.get('rows', [])),
            'timing': {
                'kb_retrieval': round(t1 - t0, 1),
                'sql_generation': round(t2 - t1, 1),
                'query_execution': round(t3 - t2, 1),
                'total': round(t3 - t0, 1)
            }
        })

    except Exception as e:
        return response(500, {'error': str(e)})


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body, default=str)
    }


def retrieve_context(question, num_results=5):
    """Retrieve relevant context from Bedrock Knowledge Base"""
    resp = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={'text': question},
        retrievalConfiguration={
            'vectorSearchConfiguration': {'numberOfResults': num_results}
        }
    )
    contexts = []
    for result in resp.get('retrievalResults', []):
        text = result.get('content', {}).get('text', '')
        if text:
            contexts.append(text)
    return "\n\n---\n\n".join(contexts)


def generate_sql(question, context):
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

"Source System: [system name] ([description]) →\\n\\nS3 Raw Landing:\\n[s3 path 1] ([file description]) AND\\n[s3 path 2] ([file description]) →\\n\\nGlue ETL ([job name]): [transformation description] →\\n\\nRedshift [schema.table]:\\n[row count] rows, grain = [one row per what] →\\n\\nDashboard Aggregation:\\n[aggregation function and why]"

TOPIC GUARDRAILS:
You are ONLY allowed to answer questions related to restaurant operations and dashboard analytics.
Allowed topics include: restaurant sales, revenue, orders, menu items, inventory, labor/staffing,
service performance, customer feedback/satisfaction, loyalty programs, equipment maintenance,
financial P&L, and dashboard navigation.

If the user asks about anything unrelated to restaurant operations, do NOT generate SQL.
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
    "lineage": "end-to-end pipeline trace formatted with newlines between each stage",
    "assumptions": "any assumptions made about the question",
    "recommended_dashboard": "name of the most relevant dashboard tab (or null if not applicable)"
}"""

    user_message = f"""Context from knowledge base:
{context}

User question: {question}

Generate a SQL query to answer this question. Include data lineage explanation."""

    resp = bedrock_runtime.invoke_model(
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

    result = json.loads(resp['body'].read())
    text = result['content'][0]['text']

    brace_idx = text.find('{')
    if brace_idx >= 0:
        decoder = json.JSONDecoder()
        parsed, _ = decoder.raw_decode(text, brace_idx)
        if parsed.get('sql'):
            parsed['sql'] = fix_generated_sql(parsed['sql'])
        return parsed
    return {"sql": text, "explanation": "", "lineage": "", "assumptions": ""}


def fix_generated_sql(sql):
    """Fix common LLM SQL mistakes before execution."""
    fixed = sql
    key_fixes = {
        'store_key': 'store_id',
        'item_key': 'item_id',
        'channel_key': 'channel_id',
        'payment_key': 'payment_method_id',
        'customer_key': 'customer_id',
    }
    for surrogate, natural in key_fixes.items():
        fixed = re.sub(
            r'\b(f[a-z]?|fs|fl|sp|i|l|fb)\.' + surrogate + r'\b',
            r'\1.' + natural,
            fixed
        )
    fin_alias_match = re.search(r'fact_financial\s+(?:AS\s+)?(\w+)', fixed, re.IGNORECASE)
    if fin_alias_match:
        alias = fin_alias_match.group(1)
        fixed = re.sub(
            r'\b' + re.escape(alias) + r'\.date_key\b',
            alias + '.month_key',
            fixed
        )
    return fixed


def execute_query(sql, timeout=60):
    """Execute SQL against Redshift and return results"""
    stmt = redshift_data.execute_statement(
        WorkgroupName=WORKGROUP,
        Database=DATABASE,
        Sql=sql
    )
    stmt_id = stmt['Id']

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
