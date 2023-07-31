#!/bin/bash

MAIL_DOMAIN="${MAIL_DOMAIN:-orp.testing}"
DKIM_SECTOR="${DKIM_SECTOR:-mail}"

KEY_DIR="/etc/opendkim/keys/$MAIL_DOMAIN"
KEY_PATH="$KEY_DIR/$DKIM_SECTOR.private"

mkdir -p "$KEY_DIR"

if [ ! -f "$KEY_PATH" ]; then
    pushd "$KEY_DIR"
    opendkim-genkey -vvv -s "$DKIM_SECTOR" -d "$MAIL_DOMAIN"
    chown opendkim:opendkim "$KEY_PATH"
    echo "#####################################################"
    echo "            Add this DKIM key to your DNS            "
    cat "$DKIM_SECTOR.txt"
    echo "#####################################################"
    popd
fi

echo "$DKIM_SECTOR._domainkey.$MAIL_DOMAIN $MAIL_DOMAIN:$DKIM_SECTOR:$KEY_PATH" > /etc/opendkim/KeyTable
echo "*@$MAIL_DOMAIN $DKIM_SECTOR._domainkey.$MAIL_DOMAIN" > /etc/opendkim/SigningTable

/usr/bin/syslog2stdout /dev/log & exec "$@"
