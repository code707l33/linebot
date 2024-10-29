import json

with open('secret.json') as fp:
    secret_data = json.load(fp)

access_token = secret_data['access_token']
secret = secret_data['secret']

print(access_token, secret)
