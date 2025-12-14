"""S3 client implementation."""
from dataclasses import dataclass
from http import HTTPStatus
from logging import getLogger
from typing import Union, IO, AsyncGenerator, Dict, Optional
from uuid import uuid4, UUID

from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError

from seedwork.domain.value_objects.content_types import ContentType
from seedwork.domain.value_objects.s3 import Bucket


logger = getLogger(__name__)


@dataclass
class S3AiobotoClient:
    """Async S3 client with lifecycle management.

    This client provides a clean interface for working with S3-compatible storage services.
    It handles connection lifecycle, provides methods for common operations, and includes
    error handling and connection management.
    """
    client: AioBaseClient

    async def upload(
        self,
        file: Union[bytes, IO],
        key: Optional[str] = None,
        bucket: Optional[str] = None
    ) -> str:
        """Upload a file to S3.

        Args:
            file: File content as bytes or file-like object
            key: Object key (optional, will generate UUID if not provided)
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            Object key
        """
        key = key or str(uuid4())
        await self.client.put_object(Bucket=bucket, Key=key, Body=file)
        return key

    async def download_chunks(
        self,
        key: str,
        bucket: Optional[str] = None,
        chunk_size: int = 1024
    ) -> AsyncGenerator[bytes, None]:
        """Download a file from S3 in chunks.

        Args:
            key: Object key
            bucket: Bucket name (optional, uses default if not provided)
            chunk_size: Size of chunks to yield

        Yields:
            File chunks as bytes
        """
        response = await self.client.get_object(Bucket=bucket, Key=key)
        while True:
            data = await response['Body'].read(chunk_size)
            if not data:
                break
            yield data

    async def download(
        self,
        key: str,
        bucket: Optional[str] = None
    ) -> bytes:
        """Download a file from S3.

        Args:
            key: Object key
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            File content as bytes
        """
        data = b''
        async for chunk in self.download_chunks(key, bucket=bucket):
            data += chunk
        return data

    async def delete(
        self,
        key: str,
        bucket: Optional[str] = None
    ) -> None:
        """Delete an object from S3.

        Args:
            key: Object key
            bucket: Bucket name (optional, uses default if not provided)
        """
        return await self.client.delete_object(Bucket=bucket, Key=key)

    async def generate_upload_url(
        self,
        key: str,
        expiration: int = 3600,
        bucket: Optional[str] = None
    ) -> str:
        """Generate a presigned URL for uploading.

        Args:
            key: Object key
            expiration: URL expiration time in seconds
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            Presigned URL for uploading
        """
        return await self.client.generate_presigned_post(
            Bucket=bucket,
            Key=key,
            ExpiresIn=expiration,
        )

    async def generate_download_url(
        self,
        key: str,
        expiration: int = 3600,
        bucket: Optional[str] = None
    ) -> str:
        """Generate a presigned URL for downloading.

        Args:
            key: Object key
            expiration: URL expiration time in seconds
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            Presigned URL for downloading
        """
        return await self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            },
            ExpiresIn=expiration,
        )

    async def upload_stream(
        self,
        file: AsyncGenerator[bytes, None],
        key: UUID,
        bucket: Bucket,
        content_type: ContentType,
    ) -> UUID:
        """Upload a file to S3 in chunks.

        Args:
            file: Async generator yielding file chunks
            key: Object key
            bucket: Bucket name
            content_type: MIME type of the file

        Returns:
            Object key
        """
        key_s: str = str(key)
        bucket_s: str = bucket.value
        content_type_s: str = content_type.value

        response = await self.client.create_multipart_upload(
            Bucket=bucket_s,
            Key=key_s,
            ContentType=content_type_s,
        )
        upload_id = response['UploadId']

        parts = []
        part_number = 1

        try:
            async for chunk in file:
                part_response = await self.client.upload_part(
                    Bucket=bucket_s,
                    Key=key_s,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=chunk
                )

                parts.append({
                    'PartNumber': part_number,
                    'ETag': part_response['ETag']
                })

                part_number += 1

            await self.client.complete_multipart_upload(
                Bucket=bucket_s,
                Key=key_s,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
        except Exception:
            await self.client.abort_multipart_upload(
                Bucket=bucket_s,
                Key=key_s,
                UploadId=upload_id
            )
            raise

        return key

    async def get_metadata(
        self,
        key: str,
        bucket: Optional[str] = None
    ) -> Dict[str, str]:
        """Get object metadata.

        Args:
            key: Object key
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            Object metadata
        """
        return await self.client.head_object(Bucket=bucket, Key=key)

    async def check_exist(
        self,
        key: str,
        bucket: Optional[str] = None
    ) -> bool:
        """Check if object exists.

        Args:
            key: Object key
            bucket: Bucket name (optional, uses default if not provided)

        Returns:
            True if object exists, False otherwise
        """
        try:
            meta = await self.get_metadata(key=key, bucket=bucket)
            return bool(meta)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise

    async def check_connection(self) -> bool:
        """Check if connection is established with S3.

        Returns:
            True if connection is established, False otherwise
        """
        try:
            resp = await self.client.list_buckets()
            return resp.get('ResponseMetadata', {}).get('HTTPStatusCode') == HTTPStatus.OK
        except Exception as exc:
            logger.error(exc)
        return False 