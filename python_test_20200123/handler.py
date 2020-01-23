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
    # 認証情報の取得
    authoriztion = str(event['headers']['Authorization'])
    # 独自認証。失敗した場合はExceptionを発生させ、カスタムレスポンスコード401を返す。
    if authoriztion != 'test':
        raise UnAuthorizationError(401,"errorMessage")
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


class UnAuthorizationError(Exception):
    """
    認証失敗の独自Exceptionクラス
    @extends Exceptionクラスを継承
    """
    def __init__(self, code, messages):
        """
        コンストラクタ
        @Param code レスポンスコード
        @Param data レスポンスデータ
        """
        self.code = code
        self.messages = messages

    def __str__(self):
        """
        文字列変換メソッド
        """
        response = {
            'status': 'HTTP/1.1 401 Unauthorized',
            'statusCode': self.code,
            'headers': {
                'Content-Type': 'application/octet-stream',
                'Accept-Charset': 'UTF-8'
            },
            'body': {
                'errorMessage': self.messages
            }
        }
        return json.dumps(response)