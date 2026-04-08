"""
GenBI QuickSight Embed URL Lambda
Generates anonymous embed URLs for QuickSight dashboard tabs.
Uses generate_embed_url_for_anonymous_user so external visitors
can view dashboards without any AWS / QuickSight sign-in.
"""

import json
import boto3

QS_ACCOUNT_ID = '530977327410'
QS_REGION = 'us-east-1'
QS_NAMESPACE = 'default'          # QuickSight namespace for anonymous sessions
QS_DASHBOARDS = {
    'executive': 'genbi-exec-dashboard',
    'sales': 'genbi-sales-dashboard',
    'operations': 'genbi-ops-dashboard',
    'customer': 'genbi-cust-dashboard',
    'financial': 'genbi-fin-dashboard',
}

qs_client = boto3.client('quicksight', region_name=QS_REGION)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET,OPTIONS'
}


def lambda_handler(event, context):
    """Lambda entry point for API Gateway proxy integration"""
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}

    try:
        params = event.get('queryStringParameters') or {}
        dashboard_key = params.get('dashboard', 'executive')
        dashboard_id = QS_DASHBOARDS.get(dashboard_key)

        if not dashboard_id:
            return {
                'statusCode': 400,
                'headers': CORS_HEADERS,
                'body': json.dumps({'error': f'Unknown dashboard: {dashboard_key}'})
            }

        dashboard_arn = (
            f'arn:aws:quicksight:{QS_REGION}:{QS_ACCOUNT_ID}'
            f':dashboard/{dashboard_id}'
        )

        response = qs_client.generate_embed_url_for_anonymous_user(
            AwsAccountId=QS_ACCOUNT_ID,
            Namespace=QS_NAMESPACE,
            SessionLifetimeInMinutes=600,
            AllowedDomains=[
                'https://d1k3nghlesd8gk.cloudfront.net',
                'http://localhost:5001'
            ],
            AuthorizedResourceArns=[dashboard_arn],
            ExperienceConfiguration={
                'Dashboard': {
                    'InitialDashboardId': dashboard_id
                }
            }
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'embedUrl': response['EmbedUrl'],
                'dashboardId': dashboard_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }
