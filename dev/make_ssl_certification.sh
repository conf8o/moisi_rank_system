#!/bin/bash

cd web/nginx/ssl

sudo touch server.key
sudo chmod 766 server.key
openssl genrsa 2048 > server.key

sudo touch server.csr
sudo chmod 766 server.csr
openssl req -new -key server.key > server.csr

sudo touch server.crt
sudo chmod 766 server.crt
sudo openssl x509 -days 3650 -req -sha256 -signkey server.key < server.csr > server.crt
