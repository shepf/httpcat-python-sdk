# -*- coding: utf-8 -*-
from httpcat.config import _BLOCK_SIZE

import requests
from urllib3 import encode_multipart_formdata
import os
import tempfile

def upload_file(file_path, upload_token, upload_url, chunk_size=_BLOCK_SIZE):
    with open(file_path, 'rb') as file:
        headers = {'UploadToken': upload_token}
        file_name = os.path.basename(file_path)
        
        # 分块上传
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            
            # 使用 urllib3 的 encode_multipart_formdata 函数编码分块数据
            data, content_type = encode_multipart_formdata([('f1', (file_name, chunk))])
            
            headers['Content-Type'] = content_type
            headers['Content-Length'] = str(len(data))
            
            response = requests.post(upload_url, headers=headers, data=data)
            # 处理上传响应，例如打印进度等
    
    return response


def generate_temp_file(size):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(os.urandom(size))
        temp_file.flush()
        file_path = temp_file.name
    return file_path


if __name__ == '__main__':
    file_size = 1024 * 1024  # 1MB
    temp_file_path = generate_temp_file(file_size)
    print(f'Temporary file path: {temp_file_path}')
    
    upload_token = 'admin_349015:ggjTvfW266vy6KG7zOsqJZCtN3c=:eyJkZWFkbGluZSI6MH0='
    upload_url = 'http://httpcat.cn/api/v1/file/upload'

    response = upload_file(temp_file_path, upload_token, upload_url)
    print(response.text)