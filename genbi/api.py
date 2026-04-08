"""
GenBI Chat API - Flask server for the dashboard chat interface
Serves the chat endpoint and QuickSight embed URL generation
"""

import json
import time
import threading
import boto3
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from agent import retrieve_context, generate_sql, execute_query

app = Flask(__name__, static_folder='../embed', static_url_path='/embed')
CORS(app)

# Redshift warm-up client
redshift_data = boto3.client('redshift-data', region_name='us-east-1')
WORKGROUP = 'demo-sales-related'
RS_DATABASE = 'dev'

# QuickSight config
QS_ACCOUNT_ID = '530977327410'
QS_REGION = 'us-east-1'
QS_USER_ARN = 'arn:aws:quicksight:us-east-1:530977327410:user/default/Admin/danshek-Isengard'
QS_DASHBOARDS = {
    'executive': 'genbi-exec-dashboard',
    'sales': 'genbi-sales-dashboard',
    'operations': 'genbi-ops-dashboard',
    'customer': 'genbi-cust-dashboard',
    'financial': 'genbi-fin-dashboard',
}
qs_client = boto3.client('quicksight', region_name=QS_REGION)


@app.route('/api/warmup', methods=['POST'])
def warmup():
    """Warm up Redshift Serverless with a lightweight query (called on dashboard load)"""
    def _warm():
        try:
            stmt = redshift_data.execute_statement(
                WorkgroupName=WORKGROUP, Database=RS_DATABASE, Sql='SELECT 1'
            )
            # Don't wait for result — just triggering the wake-up
        except Exception:
            pass
    threading.Thread(target=_warm, daemon=True).start()
    return jsonify({'status': 'warming'})


@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages with SSE progress streaming"""
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    def generate():
        t0 = time.time()

        def send_event(event_type, payload):
            return f"data: {json.dumps({'type': event_type, **payload})}\n\n"

        try:
            # Step 1: KB Retrieval
            yield send_event('status', {'step': 1, 'message': 'Searching knowledge base...', 'elapsed': 0})
            context = retrieve_context(question)
            t1 = time.time()
            yield send_event('status', {'step': 1, 'message': 'Knowledge base search complete', 'elapsed': round(t1 - t0, 1), 'done': True})

            # Step 2: SQL Generation
            yield send_event('status', {'step': 2, 'message': 'Generating SQL with Bedrock LLM...', 'elapsed': round(t1 - t0, 1)})
            sql_info = generate_sql(question, context)
            t2 = time.time()
            yield send_event('status', {'step': 2, 'message': 'SQL generated', 'elapsed': round(t2 - t0, 1), 'done': True})

            # Step 3: Redshift Execution
            yield send_event('status', {'step': 3, 'message': 'Querying Redshift...', 'elapsed': round(t2 - t0, 1)})
            query_result = execute_query(sql_info['sql'])
            t3 = time.time()
            yield send_event('status', {'step': 3, 'message': 'Query complete', 'elapsed': round(t3 - t0, 1), 'done': True})

            # Final result
            response = {
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
            }
            yield send_event('result', response)

        except Exception as e:
            yield send_event('error', {'error': str(e)})

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@app.route('/api/quicksight/embed-url', methods=['GET'])
def get_embed_url():
    """Generate QuickSight embed URL for a dashboard"""
    dashboard_key = request.args.get('dashboard', 'executive')
    dashboard_id = QS_DASHBOARDS.get(dashboard_key)

    if not dashboard_id:
        return jsonify({'error': f'Unknown dashboard: {dashboard_key}'}), 400

    try:
        response = qs_client.generate_embed_url_for_registered_user(
            AwsAccountId=QS_ACCOUNT_ID,
            UserArn=QS_USER_ARN,
            SessionLifetimeInMinutes=600,
            AllowedDomains=[
                'https://d1k3nghlesd8gk.cloudfront.net',
                'http://localhost:5001'
            ],
            ExperienceConfiguration={
                'Dashboard': {
                    'InitialDashboardId': dashboard_id
                }
            }
        )
        return jsonify({
            'embedUrl': response['EmbedUrl'],
            'dashboardId': dashboard_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quicksight/dashboards', methods=['GET'])
def list_dashboards():
    """List available dashboards"""
    return jsonify({'dashboards': [
        {'key': k, 'id': v, 'name': k.replace('-', ' ').title()}
        for k, v in QS_DASHBOARDS.items()
    ]})


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'GenBI Chat Agent'})


@app.route('/')
def serve_app():
    """Serve the embedded dashboard app"""
    return send_from_directory('../embed', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
