from aiobotocore.session import get_session
from contextlib import asynccontextmanager

class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config, verify=False) as client:
            yield client

    async def upload_bytes(self, file_bytes: bytes, object_name: str, content_type: str = None):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_bytes,
                ContentType=content_type
            )
        from urllib.parse import quote

        encoded_name = quote(object_name, safe="")
        return f"{self.config['endpoint_url']}/{self.bucket_name}/{encoded_name}"