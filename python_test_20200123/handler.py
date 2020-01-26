# coding: utf-8
"""
AWS Lambdaで実行するPythonコード

def hello(event,content) : Lambdaのhandler関数
def put(id,name) : DynamoDBにレコードを登録する関数
def query(id,name) : DynamoDBからレコードを検索する関数
def scan() : DynamoDBからレコードを全件取得する関数

class UnAuthorizationError(Exception) : 認証失敗の独自Exceptionクラス
    def __init__(self, code, messages) :  コンストラクタ
    def __str__(self) : 文字列変換メソッド
"""
import json
import logging
import boto3
import base64

# ログの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDBオブジェクトの作成
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TableName1')


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
    logger.info('event:' + str(event))

    # 認証情報の取得
    authoriztion = str(event['headers']['Authorization'])
    # 独自認証。失敗した場合はExceptionを発生させ、カスタムレスポンスコード401を返す。
    if authoriztion != 'test':
        raise UnAuthorizationError(401,"errorMessage")

    # body部の取得
    body = json.loads(json.dumps(event['body']))
    id = body['id']
    type = body['type']
    name = body['name']

    logger.info('headers:' + str(id))
    logger.info('body:' + str(name))
    logger.info('type:' + str(type))

    # DynamoDBにレコードの登録
    put(id, type, name)
    # DynamoDBから全件取得
    result = scan()

    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response

def get(event, context):
    """
    AWS Lambda Handler関数
    @Param event イベントデータ　APIGatewayからのデータ
    @Param content Lambdaのランタイムデータ
    @return APIGatewayのレスポンスデータ
    """
    # イベントデータの表示
    logger.info('headers:' + str(event['headers']))
    logger.info('body:' + str(event['body']))
    logger.info('query:' + str(event['query']))

    # 認証情報の取得
    authoriztion = str(event['headers']['Authorization'])
    # 独自認証。失敗した場合はExceptionを発生させ、カスタムレスポンスコード401を返す。
    if authoriztion != 'test':
        raise UnAuthorizationError(401,"errorMessage")

    # body部の取得
    query = event['query']
    id = query['id']
    type = query['type']

    logger.info('headers:' + str(id))
    logger.info('type:' + str(type))

    # DynamoDBから取得
    result = query(id, type)

    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response


def put(id, type, name):
    """
    DynamoDBにレコードを登録する関数
    @Param id ハッシュキー
    @Param name レンジキー
    """
    table.put_item(
        Item = {
            "id" : id,
            "type" : type,
            "name" : name,
        }
    )


def query(id, type):
    """
    DynamoDBから検索する関数
    @Param id ハッシュキー
    @Param name レンジキー
    @return 検索結果
    """
    result = table.get_item(
        Key = {
            'id' : id,
            'type' : type,
        }
    )
    return result


def scan():
    """
    DynamoDBから全件検索する関数
    @return 検索結果
    """
    result = table.scan()
    return result


class UnAuthorizationError(Exception):
    """
    認証失敗の独自Exceptionクラス
    @extends Exceptionクラスを継承
    """
    def __init__(self, code, data):
        """
        コンストラクタ
        @Param code レスポンスコード
        @Param data レスポンスデータ
        """
        self.code = code
        self.data = data

    def __str__(self):
        """
        文字列変換メソッド
        """
        response = {
            'status': 'HTTP/1.1 401 Unauthorized',
            'statusCode': self.code,
            'headers': {
                'Date': '2018/07/26 18:27:30',
                'Content-Type': 'application/octet-stream',
                'Accept-Charset': 'UTF8'
            },
            'body': {
                'result': self.code,
                'data': self.data
            }
        }
        return json.dumps(response)