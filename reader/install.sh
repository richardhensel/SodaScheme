#! /bin/bash

apt install i2c-tools
apt install libnfc5 libnfc-bin libnfc-examples

cp libnfc.conf /etc/nfc/

cp nfc_reader.py /home/pi
cp nfc_reader.service /etc/systemd/system/
