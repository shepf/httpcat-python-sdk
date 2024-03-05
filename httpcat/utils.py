# -*- coding: utf-8 -*-
from hashlib import sha1, new as hashlib_new
from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime
from .compat import b, s

try:
    import zlib

    binascii = zlib
except ImportError:
    zlib = None
    import binascii

_BLOCK_SIZE = 1024 * 1024 * 4


def urlsafe_base64_encode(data):
    """urlsafe的base64编码:

    对提供的数据进行urlsafe的base64编码。规格参考：
    URL安全的Base64编码适用于以URL方式传递Base64编码结果的场景。
    该编码方式的基本过程是先将内容以Base64格式编码为字符串，然后检查该结果字符串，
    将字符串中的加号+换成中划线-，并且将斜杠/换成下划线_。
    详细编码规范请参考[RFC4648](https://www.ietf.org/rfc/rfc4648.txt)标准中的相关描述。

    Args:
        data: 待编码的数据，一般为字符串

    Returns:
        编码后的字符串
    """
    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    """urlsafe的base64解码:

    对提供的urlsafe的base64编码的数据进行解码

    Args:
        data: 待解码的数据，一般为字符串

    Returns:
        解码后的字符串。
    """
    ret = urlsafe_b64decode(s(data))
    return ret


def file_crc32(filePath):
    """计算文件的crc32检验码:

    Args:
        filePath: 待计算校验码的文件路径

    Returns:
        文件内容的crc32校验码。
    """
    crc = 0
    with open(filePath, 'rb') as f:
        for block in _file_iter(f, _BLOCK_SIZE):
            crc = binascii.crc32(block, crc) & 0xFFFFFFFF
    return crc


def io_crc32(io_data):
    result = 0
    for d in io_data:
        result = binascii.crc32(d, result) & 0xFFFFFFFF
    return result


def io_md5(io_data):
    h = hashlib_new('md5')
    for d in io_data:
        h.update(d)
    return h.hexdigest()


def crc32(data):
    """计算输入流的crc32检验码:

    Args:
        data: 待计算校验码的字符流

    Returns:
        输入流的crc32校验码。
    """
    return binascii.crc32(b(data)) & 0xffffffff


def _file_iter(input_stream, size, offset=0):
    """读取输入流:

    Args:
        input_stream: 待读取文件的二进制流
        size:         二进制流的大小

    Raises:
        IOError: 文件流读取失败
    """
    input_stream.seek(offset)
    d = input_stream.read(size)
    while d:
        yield d
        d = input_stream.read(size)
    input_stream.seek(0)


def _sha1(data):
    """单块计算hash:

    Args:
        data: 待计算hash的数据

    Returns:
        输入数据计算的hash值
    """
    h = sha1()
    h.update(data)
    return h.digest()


def etag_stream(input_stream):
    """计算输入流的etag:

    你知道HTTP协议的ETag是干什么的吗？
    https://www.pianshen.com/article/76571224053/

    Args:
        input_stream: 待计算etag的二进制流

    Returns:
        输入流的etag值
    """
    array = [_sha1(block) for block in _file_iter(input_stream, _BLOCK_SIZE)]
    if len(array) == 0:
        array = [_sha1(b'')]
    if len(array) == 1:
        data = array[0]
        prefix = b'\x16'
    else:
        sha1_str = b('').join(array)
        data = _sha1(sha1_str)
        prefix = b'\x96'
    return urlsafe_base64_encode(prefix + data)


def file_md5(filePath):
    """计算文件的md5:
    Args:
        filePath: 待计算md5的文件路径

    Returns:
        输入文件的md5值
    """
    with open(filePath, 'rb') as f:
        return io_md5(f)


def etag(filePath):
    """计算文件的etag:
    纯前端文件名生成算法(七牛ETag算法)示例
    参考URL: https://blog.csdn.net/weixin_33671935/article/details/89613464

    Args:
        filePath: 待计算etag的文件路径

    Returns:
        输入文件的etag值
    """
    with open(filePath, 'rb') as f:
        return etag_stream(f)


def decode_entry(e):
    return (s(urlsafe_base64_decode(e)).split(':') + [None] * 2)[:2]


def rfc_from_timestamp(timestamp):
    """将时间戳转换为HTTP RFC格式

    Args:
        timestamp: 整型Unix时间戳（单位秒）
    """
    last_modified_date = datetime.utcfromtimestamp(timestamp)
    last_modified_str = last_modified_date.strftime(
        '%a, %d %b %Y %H:%M:%S GMT')
    return last_modified_str


def _valid_header_key_char(ch):
    is_token_table = [
        "!", "#", "$", "%", "&", "\\", "*", "+", "-", ".",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "W", "V", "X", "Y", "Z",
        "^", "_", "`",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "|", "~"]
    return 0 <= ord(ch) < 128 and ch in is_token_table


def canonical_mime_header_key(field_name):
    for ch in field_name:
        if not _valid_header_key_char(ch):
            return field_name
    result = ""
    upper = True
    for ch in field_name:
        if upper and "a" <= ch <= "z":
            result += ch.upper()
        elif not upper and "A" <= ch <= "Z":
            result += ch.lower()
        else:
            result += ch
        upper = ch == "-"
    return result
