from storages.backends.azure_storage import AzureStorage

account_name = 'djangoprojectstorage'
key = 'LhKLSxStTbtWrbEWprLRNzQbrbL5JehjE4Cr+dRlIyNH8JX5r4PY5mJKC1Z5OU+4S3A1jzLw/HjNt3usYridCA=='

class AzureMediaStorage(AzureStorage):
    account_name = account_name
    account_key = key
    azure_container = 'media'
    expiration_secs = None