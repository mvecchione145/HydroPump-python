from ..instruction import Instruction, Template  # noqa
from .base import Backend, SupportedFileExtensions


class AWSBucketBackend(Backend):
    """
    Backend implementation for AWS blob storage.
    """

    def __init__(
        self,
        file_extension: SupportedFileExtensions,
        root_bucket_name: str,
    ) -> None:
        """TODO: implement

        Args:
            file_extension (SupportedFileExtensions): _description_
            root_bucket_name (str): _description_
        """
        self.root_bucket_name = root_bucket_name
