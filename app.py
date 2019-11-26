# -*- coding: utf-8 -*-
from __future__ import print_function  # для единого кода Python2, Python3
__author__ = 'dontsov'

import os
import sys
import argparse
from werkzeug import serving
from flask import Flask, request, send_file
import random
import string
import time

try:
    if sys.version_info >= (3, 0):
        import ssl
    else:
        #pip install backports.ssl
        #2.7.12-2.7.16 на Mac Flask с TLS дает исключение при подключении.
        import backports.ssl as ssl
except ImportError:
    print ('for using SSL, install package')


app = Flask(__name__)


def random_name(size, chars=string.digits+string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))


# Будем хранить ссылки на предыдущий файл, чтобы удалить его
# storage[blynk_token] = "previous_photo_url"
storage = {}


# директория где размещены файлы. окончание с /
image_folder = ''

# публичная ссылка на файл без имени файла. окончание с /
public_url = ''


@app.route('/images', methods = ["POST"])
def send_images():
    t = time.time()

    blynk_token = request.headers.get('Blynk-Token')
    app.logger.info('POST data len %d' % len(request.data))
    
    #need to unique url for refresh blynk widget
    fname = blynk_token + '_' + random_name(8) + '.jpg'
    
    with open(image_folder + fname, 'wb') as fh:
        fh.write(request.data)
        app.logger.info('File %s saved' % fname)
    
    # Удаляем предыдущий файл
    try:
        os.unlink(image_folder + storage[blynk_token])
    except Exception as err:
        pass

    storage[blynk_token] = fname

    app.logger.debug('Receive and save time {} s'.format(time.time() - t)) 
    url = public_url + fname
    
    app.logger.info('Public url: ' + url)
    return url


@app.route('/images/<fname>', methods = ["GET"])
def images(fname):
    app.logger.info('get image:' + fname)
    try:
        return send_file(image_folder + fname, attachment_filename=fname)
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    """
    Пример вызова скрипта:
    
    HTTP сервер
    python server.py --host 192.168.1.10 --port 10000

    HTTPS сервер
    сгенерируйте свои ключи и положите в папку certs. запишите в клиента ca_cer.pem.
    
    python server.py --host 192.168.1.10 --port 10000 --tls
    """
    parser = argparse.ArgumentParser(description='Blynk image server TLS example')
    parser.add_argument('--host', help='Ip address')
    parser.add_argument('--port', type=int, default=6000, help='Port')  # in Mac, Linux use sudo for port < 1000
    parser.add_argument('--cacert', default='certs/ca_cer.pem', help='CA certificate file')
    parser.add_argument('--key', default='certs/server_key.pem', help='Private key')
    parser.add_argument('--cert', default='certs/server_cer.pem', help='Certificate file')
    parser.add_argument('--tls', action='store_true', help='Use HTTPS TLS 1.2')
    parser.add_argument('--images', default='', help='Full path to images folder')
    parser.add_argument('--debug', default=True, help='turn on logger')
    args = parser.parse_args()

    app.debug = args.debug
    app.logger.info(args)

    if args.tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        #context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(args.cacert)
        context.load_cert_chain(args.cert, args.key)
    else:
        context = None

    image_folder = args.images
    public_url = 'http://' + args.host + ':' + str(args.port) + '/images/'
    serving.run_simple(args.host, args.port, app, ssl_context=context)

