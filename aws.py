import boto3

session = boto3.Session(profile_name='pkpredeemingtime')

s3_client = session.client('s3')

dynamodb = session.client('dynamodb', region_name='us-east-1')