import boto3
from botocore.exceptions import  ConnectionError, ClientError
import logging
import requests

QSREGION = 'eu-west-1'
AWS_ACCOUNT_ID =  '412738038163'
DASHBOARD_ID = '2e385c5c-841a-4bd3-a28f-d8cdc0863c22' # OLD: '550ee793-d4ce-408d-865b-7b25937e0723' # sample dashboard: '24b067dc-a98a-4861-948c-d4304c93a2e4'
QUICKSIGHT_USER_ARN = 'arn:aws:quicksight:us-east-1:412738038163:user/default/barry.walsh'

def create_connection():
    try:
        print('CONNECTING')
        qs = boto3.client('quicksight', region_name=QSREGION) # TODO: Replace with the region in which your quicksight is configured
        return qs
    except  ConnectionError as e:
        print(e)
        logger.error("Error occured in connecting to qs: {}".format(e))
    except  Exception as e:
        print(e)
        logger.error("Unknown error occured: {}".format(e))

def getDashboardURL():
    
    qs = create_connection()
    print('Conn created')
    try:
        response = qs.get_dashboard_embed_url(
            AwsAccountId = AWS_ACCOUNT_ID, # TODO: Replace with your AWS Account ID
            DashboardId = DASHBOARD_ID, # TODO: Replace with your QuickSight Dashboard ID
            Namespace = "default", # TODO: Replace with your QuickSight Dashboard Namespace (if any)
            IdentityType = "QUICKSIGHT",
            UserArn = QUICKSIGHT_USER_ARN # TODO: Replace with your USER ARN which has access to QuickSight
        )
        return response['EmbedUrl']
    except ClientError as e:
        print(e)
        return "Error generating embeddedURL: " + str(e)
    except Exception as er:
        print(er)
    
#getDashboardURL(dashboard_id, "default")
