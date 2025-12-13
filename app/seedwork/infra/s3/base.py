from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol, runtime_checkable

from aiobotocore.response import StreamingBody

@runtime_checkable
class AsyncS3ClientProtocol(Protocol):
    async def get_object(
        self,
        *,
        Bucket: str,
        Key: str,
    ) -> dict: ...

    async def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        Body: Any,
        ContentType: str | None,
    ) -> dict: ...

    async def upload_fileobj(
        self,
        Fileobj: Any,
        Bucket: str,
        Key: str,
        ExtraArgs: Optional[dict[str, Any]] = ...,
    ) -> None: ...

    async def delete_object(
        self,
        *,
        Bucket: str,
        Key: str,
    ) -> dict: ...

    async def list_objects_v2(
        self,
        *,
        Bucket: str,
        Prefix: str = ...,
    ) -> dict: ...

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: dict[str, Any],
        ExpiresIn: int = 3600,
        HttpMethod: str | None = None,
    ) -> str: ...


@dataclass
class S3GetObjectResponse:
    body: StreamingBody
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Optional[dict[str, str]] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    server_side_encryption: Optional[str] = None


@dataclass
class S3PutObjectResponse:
    etag: Optional[str] = None
    version_id: Optional[str] = None
    server_side_encryption: Optional[str] = None


# New response for upload_fileobj
@dataclass
class S3UploadFileObjResponse:
    status: str = "success"

@dataclass
class S3DeleteObjectResponse:
    delete_marker: Optional[bool] = None
    version_id: Optional[str] = None
    request_charged: Optional[str] = None

@dataclass
class S3ListObjectsV2Response:
    contents: Optional[list[dict]] = None
    common_prefixes: Optional[list[dict]] = None
    delimiter: Optional[str] = None
    encoding_type: Optional[str] = None
    is_truncated: Optional[bool] = None
    key_count: Optional[int] = None
    max_keys: Optional[int] = None
    name: Optional[str] = None
    next_continuation_token: Optional[str] = None
    prefix: Optional[str] = None
    start_after: Optional[str] = None
