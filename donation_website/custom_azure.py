from storages.backends.azure_storage import AzureStorage

class StaticAzureStorage(AzureStorage):
    account_name = 'donationwebsite'
    account_key = 'gkmaTeJx6vcgRlX781yuk+JNmlspG3q2gB7kr/R/Arnhpr/FLV+Rx2gbcrLnX4BiShF+X9zyWiRpmt1pruK6lA=='
    azure_container = 'django-app-donation-static'
    expiration_secs = None

class MediaAzureStorage(AzureStorage):
    account_name = 'donationwebsite'
    account_key = 'gkmaTeJx6vcgRlX781yuk+JNmlspG3q2gB7kr/R/Arnhpr/FLV+Rx2gbcrLnX4BiShF+X9zyWiRpmt1pruK6lA=='
    azure_container = 'django-app-donation-media'
    expiration_secs = None
