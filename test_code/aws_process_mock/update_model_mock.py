from unittest import mock
import json, os
from io import StringIO

# mocked_update_modelの動作を再現
def mocked_update_model():
    return 1

def boto3_resource(*args, **kwargs):
    class MockBucket:
        def Bucket(*args, **kwargs):
            class MockUploadFile:
                def upload_file(*args, **kwargs):
                    return
            if args[0] == os.environ['BUCKET_NAME']:
                return MockUploadFile
            return None
    if args[0] == "s3":
        return MockBucket
    return None
