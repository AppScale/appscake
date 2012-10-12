#!/bin/sh
BASE_PATH=$(cd "$(dirname "$0")"; pwd)
KEY_FILE=$BASE_PATH/pk-appscake.pem
CERT_FILE=$BASE_PATH/cert-appscake.pem
openssl genrsa -out ${KEY_FILE} 1024
(
echo "US"
echo "California"
echo "Santa Barbara"
echo "UC Santa Barbara"
echo "Dept. of Computer Science"
echo "AppsCake"
echo "appscale_community@googlegroups.com"
echo
echo
)|
openssl req -new -x509 -nodes -days 365 -out ${CERT_FILE} -key ${KEY_FILE}