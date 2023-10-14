from logging import Logger
from boto3 import client
from botocore.exceptions import ClientError


class S3Storage:
    """
    S3Storage class to handle all the S3 operations
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
        logger: Logger,
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.region = region
        self.s3 = client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )
        self.logger = logger

    def check_bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            self.logger.error(e)
            return False
        return True

    def create_bucket(self):
        try:
            self.s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.region},
            )
        except ClientError as e:
            self.logger.error(e)
            return False
        return True

    def upload_file(self, file, file_name, content_type):
        assert isinstance(content_type, dict)
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                file_name,
                ExtraArgs=content_type,
            )
        except ClientError as e:
            self.logger.error(e)
            return False
        return True

    def delete_file(self, file_name):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
        except ClientError as e:
            self.logger.error(e)
            return False
        return True

    def get_all_items_in_folder(self, folder_path):
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name, Prefix=folder_path
            )
            return response.get("Contents", [])
        except ClientError as e:
            self.logger.error(e)
