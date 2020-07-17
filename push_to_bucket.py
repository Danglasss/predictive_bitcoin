import boto3
import boto.s3
import sys
from boto.s3.key import Key
import botocore


class push_to_bucket:

	def __init__(self):
		self.access_id  = "AKIAJSM5ZFBMAPKFU3YA"
		self.access_key = "lCwtmC4055RXT+PnAZAh3mf/hPumbv6pqbgW14AE" 
		
		self.s3     = boto3.resource('s3',
				aws_access_key_id=self.access_id,
					aws_secret_access_key=self.access_key)
		self.client = boto3.client('s3',
				aws_access_key_id=self.access_id,
					aws_secret_access_key=self.access_key)
	
	def create_bucket(self, bucket):
		try :
			self.client.create_bucket(
				ACL='public-read-write',
    			Bucket=bucket,
    			CreateBucketConfiguration={
        		'LocationConstraint': 'eu-west-3',
    			},
			)
		except botocore.exceptions.ClientError as e:
			print(e.response)
			exit(1)

	def push_to_bucket(self, bucket, filename):
		try :
			self.s3.Bucket(bucket).upload_file(filename, filename)
		except botocore.exceptions.ClientError as e:
			print(e.response)
			exit(1)

	def download_filebucket(self, bucket, filename):
		try:
			self.s3.Bucket(bucket).download_file(filename, filename)
		except botocore.exceptions.ClientError as e:
			print(e.response)
			exit(1)
	
	def del_bucket(self, bucket, filename):
		self.s3.Object(bucket, filename).delete()
