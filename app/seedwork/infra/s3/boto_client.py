from dataclasses import dataclass
from uuid import UUID
from typing import Annotated, Any

from botocore.exceptions import ClientError
from fastapi import UploadFile

from seedwork.domain.value_objects.content_types import MediaType
from seedwork.infra.s3.base import (
    AsyncS3ClientProtocol,
    S3DeleteObjectResponse,
    S3GetObjectResponse,
    S3PutObjectResponse,
    S3ListObjectsV2Response,
    S3UploadFileObjResponse,
)
from seedwork.infra.s3.exceptions import ContentNotExistException


@dataclass
class BotoClient:
    client: AsyncS3ClientProtocol

    async def get_content(
        self,
        content_uid: UUID,
        bucket_name: str,
    ) -> S3GetObjectResponse:
        try:
            response: dict = await self.client.get_object(
                Bucket=bucket_name,
                Key=str(content_uid),
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                raise ContentNotExistException(content_uid=content_uid)
            else:
                raise

        return self._map_get_object(response)

    async def put_content(
        self,
        content_uid: UUID,
        bucket_name: str,
        body: bytes,
        content_type: MediaType,
    ) -> S3PutObjectResponse:
        response: dict = await self.client.put_object(
            Bucket=bucket_name,
            Key=str(content_uid),
            Body=body,
            ContentType=content_type.value,
        )
        return self._map_put_object(response)

    async def upload_fileobj(
        self,
        content_uid: UUID,
        bucket_name: str,
        fileobj: UploadFile,
        content_type: MediaType,
    ) -> S3UploadFileObjResponse:
        await self.client.upload_fileobj(
            Fileobj=fileobj,
            Bucket=bucket_name,
            Key=str(content_uid),
            ExtraArgs={"ContentType": content_type.value},
        )
        return S3UploadFileObjResponse()

    async def delete_content(self, content_uid: UUID, bucket_name: str) -> S3DeleteObjectResponse:
        try:
            response: dict = await self.client.delete_object(
                Bucket=bucket_name,
                Key=str(content_uid),
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                raise ContentNotExistException(content_uid=content_uid)
            else:
                raise
        return self._map_delete_object(response)

    async def list_contents(self, prefix: str, bucket_name: str) -> S3ListObjectsV2Response:
        response: dict = await self.client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
        )
        return self._map_list_objects(response)

    async def generate_presigned_url(
        self,
        client_method: str,
        params: dict[str, Any],
        expires: int = 3600,
        http_method: str | None = None,
    ) -> Annotated[str, "s3 url for download file"]:
        url: str = await (
            self.client.generate_presigned_url(
                ClientMethod=client_method,
                Params=params,
                ExpiresIn=expires,
                HttpMethod=http_method,
            )
        )
        return url

    @staticmethod
    def _map_get_object(data: dict) -> S3GetObjectResponse:
        return S3GetObjectResponse(
            body=data["Body"],
            content_length=data.get("ContentLength"),
            content_type=data.get("ContentType"),
            etag=data.get("ETag"),
            last_modified=data.get("LastModified"),
            metadata=data.get("Metadata"),
            version_id=data.get("VersionId"),
            storage_class=data.get("StorageClass"),
            server_side_encryption=data.get("ServerSideEncryption"),
        )

    @staticmethod
    def _map_put_object(data: dict) -> S3PutObjectResponse:
        return S3PutObjectResponse(
            etag=data.get("ETag"),
            version_id=data.get("VersionId"),
            server_side_encryption=data.get("ServerSideEncryption"),
        )

    @staticmethod
    def _map_delete_object(data: dict) -> S3DeleteObjectResponse:
        return S3DeleteObjectResponse(
            delete_marker=data.get("DeleteMarker"),
            version_id=data.get("VersionId"),
            request_charged=data.get("RequestCharged"),
        )

    @staticmethod
    def _map_list_objects(data: dict) -> S3ListObjectsV2Response:
        return S3ListObjectsV2Response(
            contents=data.get("Contents"),
            common_prefixes=data.get("CommonPrefixes"),
            delimiter=data.get("Delimiter"),
            encoding_type=data.get("EncodingType"),
            is_truncated=data.get("IsTruncated"),
            key_count=data.get("KeyCount"),
            max_keys=data.get("MaxKeys"),
            name=data.get("Name"),
            next_continuation_token=data.get("NextContinuationToken"),
            prefix=data.get("Prefix"),
            start_after=data.get("StartAfter"),
        )
