import requests
import json

db_id = '732149c4f1574f638da780692a2e7d4f'
token = 'secret_MFhgeM2cnADVTdwet09QP6BF40bmLt7ltBlssPk5WK0'
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28"
}

url = 'https://api.notion.com/v1/databases/' + db_id

res = requests.request('GET', url, headers=headers)

print(res.json())
