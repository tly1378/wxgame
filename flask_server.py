from flask import Flask, send_from_directory, abort, Response
from flask_compress import Compress
import os
import gzip
import io
import logging

app = Flask(__name__)
Compress(app)

# 配置日志
logging.basicConfig(level=logging.DEBUG)

base_path = r'D:\Projects\Wechat\wechat_dev\webgl'

@app.route('/<path:filename>')
def serve_file(filename):
    logging.debug(f'Requested filename: {filename}')
    
    # 使用 os.path.join 并确保路径在 base_path 内
    safe_path = os.path.join(base_path, filename)
    logging.debug(f'Safe path: {safe_path}')
    
    if not os.path.isfile(safe_path):
        logging.warning(f'File not found: {safe_path}')
        return abort(404)
    
    with open(safe_path, 'rb') as f:
        file_data = f.read()

    # 如果文件是 .txt 类型，手动添加压缩支持
    if filename.endswith('.txt'):
        logging.debug(f'Compressing file: {filename}')
        
        compressed_data = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='wb') as gz:
            gz.write(file_data)
        
        compressed_data.seek(0)
        response = Response(compressed_data.read(), content_type='text/plain')
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        
        logging.debug(f'File compressed and response prepared for: {filename}')
    else:
        response = send_from_directory(base_path, filename)
        logging.debug(f'Serving file without compression: {filename}')
    
    return response

if __name__ == '__main__':
    logging.info('Starting Flask server...')
    app.run(host='0.0.0.0', port=8000)
