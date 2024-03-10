import requests
import os


def download_file(download_url, save_path, filename):
    response = requests.get(download_url)

    save_path_with_filename = os.path.join(save_path, filename)
    with open(save_path_with_filename, 'wb') as file:
        file.write(response.content)

    return save_path_with_filename


if __name__ == '__main__':
    # Existing code for file upload

    filename = 'test.md'
    save_path = '.'
    download_url = f'http://httpcat.cn/api/v1/file/download?filename={filename}'

    downloaded_file_path = download_file(download_url, save_path, filename)
    print(f'Downloaded file saved at: {downloaded_file_path}')