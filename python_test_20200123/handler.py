# coding: utf-8
import json
import logging

# ログの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello(event, context):
    """
    AWS Lambda Handler関数
    @Param event イベントデータ　APIGatewayからのデータ
    @Param content Lambdaのランタイムデータ
    @return APIGatewayのレスポンスデータ
    """
    # イベントデータの表示
    logger.info('headers:' + str(event['headers']))
    logger.info('body:' + str(event['body']))
    # レスポンスbodyを作成
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response