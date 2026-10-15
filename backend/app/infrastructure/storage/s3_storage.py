import boto3
from botocore.exceptions import ClientError
from typing import List
from app.domain.interfaces.storage_port import StoragePort
from app.domain.entities.document import RawDocument
from app.infrastructure.config.settings import settings
from app.infrastructure.parsers.file_parser import FileParser

class S3StorageAdapter(StoragePort):
    def __init__(self):
        self.bucket_name = settings.S3_BUCKET_NAME
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def save_file(self, filename: str, file_bytes: bytes) -> str:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_bytes
            )
            return f"s3://{self.bucket_name}/{filename}"
        except ClientError as e:
            raise RuntimeError(f"Error al subir '{filename}' a Amazon S3: {str(e)}")

    def load_all_documents(self) -> List[RawDocument]:
        documents: List[RawDocument] = []
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            for obj in response.get("Contents", []):
                key = obj["Key"]
                if FileParser.is_supported(key):
                    s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
                    file_bytes = s3_object["Body"].read()
                    content = FileParser.extract_text(key, file_bytes)
                    documents.append(
                        RawDocument(
                            filename=key,
                            content=content,
                            metadata={"source": key, "storage": f"s3://{self.bucket_name}"}
                        )
                    )
            return documents
        except ClientError as e:
            raise RuntimeError(f"Error leyendo documentos desde Amazon S3: {str(e)}")