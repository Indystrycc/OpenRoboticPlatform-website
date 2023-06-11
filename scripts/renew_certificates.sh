#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TARGET_DIR="$SCRIPT_DIR/secret"
CERT_DIR_PARAM="${1:-"$SCRIPT_DIR/../prod/nginx/certs"}"
echo "$CERT_DIR_PARAM"

if [ ! -d "$TARGET_DIR" ]; then
	echo "\"secret\" directory doesn't exist. A CA must exist before new certificates are generated. Please use create_ca_and_certificates.sh instead."
	exit 1
fi
CERT_DIR="$( realpath $CERT_DIR_PARAM )"
pushd "$TARGET_DIR"

if [ ! -f "cacert.pem" ] || [ ! -f "cakey.pem" ] || [ ! -f "index.txt" ] || [ ! -f "serial.txt" ]; then
	echo "One of the required CA files (cacert.pem, cakey.pem, index.txt or serial.txt) doesn't exist."
	echo "Please use create_ca_and_certificates.sh to create a new CA and certificates."
	popd
	exit 1
fi

# Generate and sign server certificate
echo "Generating server private key and a certificate signing request."
# openssl req -newkey rsa:4096 -sha256 -nodes -keyout privkey.pem -out server.csr -subj "/CN=orp.localhost" -addext "subjectAltName=DNS:orp.localhost,DNS:localhost,IP:127.0.0.1,IP:::1"
openssl req -newkey rsa:4096 -sha256 -nodes -config ../cnf/server.cnf -keyout privkey.pem -out server.csr
echo "Signing the certificate. Now you'll have to enter the CA password."
openssl ca -config ../cnf/ca.cnf -notext -out cert.pem -infiles server.csr

# Copy the files required by nginx to $CERT_DIR
cp cacert.pem "$CERT_DIR/chain.pem"
cat cert.pem cacert.pem > "$CERT_DIR/fullchain.pem"
cp privkey.pem "$CERT_DIR/privkey.pem"
echo "Done. Required files have been copied to $CERT_DIR."

popd
