# -*- coding: utf-8 -*-
RS_HOST = 'http://httpcat.cn'
RS_PORT = 8888

# 1024 * 1024表示1MB的字节数，乘以4后即表示4MB的字节数
_BLOCK_SIZE = 1024 * 1024 * 4  # 断点续传分块大小

_config = {
    'default_rs_host': RS_HOST,
    'connection_timeout': 30,  # 链接超时为时间为30s
    'connection_retries': 3,  # 链接重试次数为3次
    'connection_pool': 10,  # 链接池个数为10
}