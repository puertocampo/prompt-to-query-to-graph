import boto3
import base64
import io
from datetime import datetime

def upload_image_to_s3(base64_image: str) -> str:
    """
    Base64エンコードされた画像をS3にアップロードし、URLを返す関数

    Args:
        base64_image (str): Base64エンコードされた画像データ

    Returns:
        str: アップロードされた画像のURL
    """
    try:
        # LocalStackのS3クライアントを作成
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='prompt-to-query-to-graph',
            aws_secret_access_key='prompt-to-query-to-graph',
            region_name='ap-northeast-1'
        )

        # バケット名を設定
        bucket_name = 'graph-images'

        # バケットが存在しない場合は作成
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except:
            s3_client.create_bucket(Bucket=bucket_name)

        # Base64デコード
        image_data = base64.b64decode(base64_image)

        # ファイル名を生成（タイムスタンプを使用）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'graph_{timestamp}.png'

        # S3にアップロード
        s3_client.upload_fileobj(
            io.BytesIO(image_data),
            bucket_name,
            file_name,
            ExtraArgs={'ContentType': 'image/png'}
        )

        # URLを生成して返す
        url = f'http://localhost:4566/{bucket_name}/{file_name}'
        return url

    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

if __name__ == "__main__":
    upload_image_to_s3()