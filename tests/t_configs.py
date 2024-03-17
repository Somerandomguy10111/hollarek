from hollarek.configs import AWSConfigs
from hollarek.cloud import AWSRegion

if __name__ == "__main__":
    # another_configs = LocalConfigs(config_fpath='abcd')
    # local_confs = LocalConfigs()

    cloud_confs = AWSConfigs(secret_name='lotus_api_keys', region=AWSRegion.EU_NORTH_1.value)
    cloud_confs.get(key='openai_api_key')


    print(cloud_confs.get(key='openai_api_keyy'))

