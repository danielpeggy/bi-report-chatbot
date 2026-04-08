"""
GenBI QuickSight Embed URL Lambda
Generates embed URLs for QuickSight dashboard tabs.
"""

import json
import boto3

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
