
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
	location = 'static'
	file_overwrite = True

class MediaStorage(S3BotoStorage):
	location = 'media'
	file_overwrite = False

class CachedStaticS3BotoStorage(StaticStorage):
    """
    S3 static storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedStaticS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super(CachedStaticS3BotoStorage, self).save(name, self.local_storage._open(name))
        return name

