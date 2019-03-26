"""
This implement a basic assume role provider
and also default aws credentials
"""

import boto3

ROLE_OBJECT_KEYS = ["role_arn", "session_name"]
CREDETIALS_OBJECT_KEYS = ["aws_access_key_id", "aws_secret_key_id"]

class Credentials:

    def __init__(self, config):
        self.config = config
        self._load_credentials()
    
    def _load_credentials(self):
        if all(name in self.config for name in ROLE_OBJECT_KEYS):
            self._assume_role_provider(config)
        elif all(name in self.config for name in CREDETIALS_OBJECT_KEYS):
            self.access_key_id = config["aws_access_key_id"]
            self.secret_key_id = config["aws_secret_key_id"]
            self.session_token = ""
        else:
            print("can't load any credentials for config")
            self.access_key_id = None
            self.secret_key_id = None
            self.session_token = None

    def _assume_role_provider(self, config):
        sts = boto3.client(sts)
        assume_role_object = sts_client.assume_role(
            roleArn=config["role_arn"],
            sessionName=config["session_name"]
        )
        self.access_key_id = assumed_role_object['Credentials']['AccessKeyId']
        self.secret_key_id = assumed_role_object['Credentials']['SecretAccessKey']
        self.session_token = assumed_role_object['Credentials']['SessionToken']

    def get_credentials(self, config):
        if self.access_key_id == None or self.secret_key_id == None:
            raise ValueError("Credentials not found")
        else:
            return (self.access_key_id, self.secret_key_id, self.session_token)