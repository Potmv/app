from aiobotocore.session import get_session
from contextlib import asynccontextmanager

from config import settings


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
        return f"https://a7af36d0-4d00-494e-9aee-99f8825af363.selstorage.ru/{encoded_name}"

s3_client = S3Client(
        access_key=settings.ACCESS_KEY,
        secret_key=settings.SECRET_KEY,
        endpoint_url=settings.ENDPOINT_URL,
        bucket_name=settings.BUCKET_NAME,
    )