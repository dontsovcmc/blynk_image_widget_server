
Настройка TLS
=============

Настроим защищенную передачу данных файлов.
Создадим Центр сертификации и сгенерируем ключ/сертификат для сервера.
В Ватериус запишем сертификат Центра сертификации. Он подтвердит, что сервер тот, за кого себя выдает.

openssl genrsa -out ca_key.pem 2048
openssl req -x509 -new -nodes -key ca_key.pem -days 8000 -out ca_cer.pem -subj '/CN=192.168.1.10/C=RU/ST=Moscow/L=Moscow/O=Your company/OU=Your community'
openssl genrsa -out server_key.pem 2048

# Замените 192.168.1.10 на свой домен или IP адрес сервера (!). Именно его и подтверждает сертификат.
openssl req -out server_req.csr -key server_key.pem -new -subj '/CN=192.168.1.10/C=RU/ST=Moscow/L=Moscow/O=Your company/OU=Your community'
# в windows другие / надо указывать: openssl req -out server_req.csr -key server_key.pem -new -subj '//CN=192.168.1.10\C=RU\ST=Moscow\L=Moscow\O=Your company\OU=Your community'

openssl x509 -req -in server_req.csr -out server_cer.pem -sha256 -CAcreateserial -days 8000 -CA ca_cer.pem -CAkey ca_key.pem


ca_key.pem - ключ вашего Центра сертификации. Храним в сейфе.
ca_cer.pem - публичный X.509 сертификат Центра сертификации для генерации ключей сервера, служит и для проверки публичного ключа сервера.
server_key.pem - приватный ключ сервера. Только на сервере.
server_cer.pem - публичный ключ сервера. Может быть передан клиентам.

В клиента записываем ca_cer.pem. Теперь клиент может по передавать данные зашифровано, убеждаясь, что сервер настоящий.
Сертификат имеет срок годности и требует обновления.

Просмотреть содержимое сертификата:
openssl x509 -in ca_cer.pem -text