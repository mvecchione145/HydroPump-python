"""Backend represents the storage and management of the instruction."""
from .base import Backend, SupportedFileExtensions, InstructionType  # noqa
from .file_system import FileSystemBackend
from .aws import AWSBucketBackend


BACKENDS = {
    "base": Backend,
    "file_system": FileSystemBackend,
    "aws_bucket": AWSBucketBackend,
}
