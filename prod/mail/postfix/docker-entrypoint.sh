#!/bin/bash

MAIL_HOSTNAME="${MAIL_HOSTNAME:-postfix.orp.testing}"
MAIL_DOMAIN="${MAIL_DOMAIN:-orp.testing}"

# I could disable chroot, but this works too
cp /etc/resolv.conf /var/spool/postfix/etc/resolv.conf

echo "$MAIL_DOMAIN" > /etc/mailname
postconf myhostname=$MAIL_HOSTNAME
host website | awk '/has address/ { print $4 }' > /etc/postfix/mynetworks

exec "$@"
