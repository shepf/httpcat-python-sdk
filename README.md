# httpcat-sdk
## Introduction
The "httpcat-sdk" is a Python client SDK designed to be used in conjunction with the ["HttpCat" server-side project](https://github.com/shepf/httpcat-release). 
It provides a set of convenient functionalities and interfaces for communicating with the "HttpCat" service.


Httpcat SDK for Python allows you to easily upload and download your httpcat service files.


## Install
pip install
```bash
$ pip install httpcat-sdk
```

Check if the installation was successful:
```bash
(venv) [root@dev ~]# python
Python 3.8.12 (default, Aug  6 2023, 18:06:17)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import httpcat
>>> httpcat.__version__
'0.0.1'
>>>
```

## Usage
```
from httpcat.services.storage.uploader import upload_file

# file_path = '/path/to/file'
file_path = '/root/aaa.txt'
upload_token = 'admin_349015:ggjTvfW266vy6KG7zOsqJZCtN3c=:eyJkZWFkbGluZSI6MH0='
upload_url = 'http://httpcat.cn/api/v1/file/upload'

response = upload_file(file_path, upload_token, upload_url)
print(response.text)
```

Based on your deployment of httpcat, modify the upload_token and upload_url information. 
The upload_token is obtained from the token management interface of the httpcat service.



Normal output result:
```bash
>>> print(response.text)
{"errorCode":0,"msg":"success","data":"upload successful!"}
```

