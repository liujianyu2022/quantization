# import requests
# try:
#     response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
#     print("成功 = ", response.status_code)
# except requests.exceptions.RequestException as e:
#     print("错误:", e)


import os
import requests

# 禁用代理
# os.environ['NO_PROXY'] = 'en.wikipedia.org'

try:
    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    print("Status Code:", response.status_code)
except requests.exceptions.RequestException as e:
    print("错误:", e)
