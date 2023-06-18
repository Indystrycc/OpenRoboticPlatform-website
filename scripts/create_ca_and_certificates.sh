#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TARGET_DIR="$SCRIPT_DIR/secret"
CERT_DIR_PARAM=${1:-"$SCRIPT_DIR/../prod/nginx/certs"}

if [ ! -d "$TARGET_DIR" ]; then
	mkdir "$TARGET_DIR"
fi

CERT_DIR="$( realpath $CERT_DIR_PARAM )"

pushd "$TARGET_DIR"
echo "Changing directory to $TARGET_DIR"

# Generate CA key and certificate
# openssl genrsa -aes256 -out cakey.pem 2048
# openssl req -new -x509 -config ../cnf/ca.cnf -nodes -days 365000 -key cakey.pem -out cacert.pem
echo "Creating CA. Please remember the password you enter, or you will be unable to sign the server certificate."
openssl req -x509 -newkey rsa:4096 -config ../cnf/ca.cnf -days 365000 -keyout cakey.pem -out cacert.pem

# Prepare index and serial for signing certificates
touch index.txt
echo '01' > serial.txt

# Generate and sign server certificate
echo "Generating server private key and a certificate signing request."
openssl req -newkey rsa:4096 -sha256 -nodes -config ../cnf/server.cnf -keyout privkey.pem -out server.csr # -subj "/CN=orp.localhost" -addext "subjectAltName=DNS:orp.localhost,DNS:localhost,IP:127.0.0.1,IP:::1"
echo "Signing the certificate. Now you'll have to enter the CA password."
openssl ca -config ../cnf/ca.cnf -notext -out cert.pem -infiles server.csr

# Copy the files required by nginx to $CERT_DIR
if [ ! -d "$CERT_DIR" ]; then
	mkdir -p "$CERT_DIR"
fi
cp cacert.pem "$CERT_DIR/chain.pem"
cat cert.pem cacert.pem > "$CERT_DIR/fullchain.pem"
cp privkey.pem "$CERT_DIR/privkey.pem"
echo "Done. Required files have been copied to $CERT_DIR."

popd
