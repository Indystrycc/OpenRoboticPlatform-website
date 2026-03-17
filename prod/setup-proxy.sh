#!/usr/bin/env bash

NGINX_CONF_DIR="${NGINX_CONF_DIR:-/etc/nginx}"
# Relative to NGINX_CONF_DIR
SITES_ENABLED_SUBDIR="${SITES_ENABLED_SUBDIR:-sites-enabled}"

print_usage() {
    echo "usage: $0 [--install [-f|--force]][-h|--help]

Generate proxy configuration files for nginx and installs them.

Options:
    -h, --help          show this message and exit
    --instal            install files without interactive confirmation prompt. The script will try using sudo, so you may need to enter your password.
    -f, --force         allow overwriting existing files (including ffdhe2048.txt)

Env var overrides:
    NGINX_CONF_DIR          /etc/nginx is assumed
    SITES_ENABLED_SUBDIR    subdirectory of NGINX_CONF_DIR which contains files that are included automatically. Defaults to sites-enabled, but some installations use vhosts.d or have only conf.d
"
    exit $1
}

ARGLIST=$(getopt -o hf --long help,install,force -n "$0" -- "$@")
if [ $? != 0 ]; then
    exit $?;
fi
eval set -- "$ARGLIST"

SHOULD_INSTALL=
OVERWRITE_FILES=

while true; do
    case "$1" in
        -h|--help) print_usage 0 ;;
        --install) SHOULD_INSTALL=1; shift ;;
        -f|--force) OVERWRITE_FILES=1; shift ;;
        --) shift; break ;;
        *) echo "Unknown option $1"; print_usage 1 ;;
    esac
done

# Execute everything from the script directory or paths will break :)
SCRIPT_DIR="$(realpath "$(dirname "$0")")"
pushd "$SCRIPT_DIR" > /dev/null

# Load the variables used for substitution from config.env
if [ ! -f config.env ]; then
    echo "Please create config.env based on config_example.env with the necessary changes."
    popd > /dev/null
    exit 1
fi
source config.env

if [[ ! ( -v FULLCHAIN_PATH && -v PRIVKEY_PATH ) ]]; then
    echo "FULLCHAIN_PATH and PRIVKEY_PATH are new required configuration variables. Please add them to config.env."
    popd > /dev/null
    exit 1
fi

SITES_ENABLED_PATH="$NGINX_CONF_DIR/$SITES_ENABLED_SUBDIR"
if [ ! -d "$SITES_ENABLED_PATH" ]; then
    echo "$SITES_ENABLED_SUBDIR/ does not exist inside $NGINX_CONF_DIR/. If your NGINX installation does not have a sites-enabled.d/ or similar directory, please create it and make sure that *.conf files from this directory are included in the 'http' block."
    popd > /dev/null
    exit 1
fi

FULLCHAIN_PATH="$(realpath "$FULLCHAIN_PATH")"
PRIVKEY_PATH="$(realpath "$PRIVKEY_PATH")"
REPO_ROOT=$(realpath "$SCRIPT_DIR/../")

DOMAIN="$DOMAIN" FULLCHAIN_PATH="$FULLCHAIN_PATH" PRIVKEY_PATH="$PRIVKEY_PATH" REPO_ROOT="$REPO_ROOT" envsubst '$DOMAIN$FULLCHAIN_PATH$PRIVKEY_PATH$REPO_ROOT' < nginx/orp.conf.template > nginx/conf/orp.conf

echo "To install configuration files please run the following commands (and make sure that you have permissions to access relevant files and directories):
cp -i $SCRIPT_DIR/nginx/conf/ffdhe2048.txt $NGINX_CONF_DIR/
ln -s $SCRIPT_DIR/nginx/conf/includes/*.conf $NGINX_CONF_DIR/includes/
ln -s $SCRIPT_DIR/nginx/conf/orp.conf $NGINX_CONF_DIR/$SITES_ENABLED_SUBDIR/"

RETRYING=0

prompt_retry() {
    if [[ "$RETRYING" -eq 0 ]]; then
        RETRYING=1
        echo "Operation failed, retrying with sudo"
    fi
}

# This will try again with sudo if the user rejects, but this script will probably be run just once, so it doesn't have to be perfect
install_copy_file() {
    if [[ "$1" -eq 1 ]]; then CMD="cp"; else CMD="cp -i"; fi
    $CMD "$2" "$3"
    if [[ $? -ne 0 ]]; then
        prompt_retry
        sudo $CMD "$2" "$3"
    fi
}

install_symlink() {
    if [[ "$1" -eq 1 ]]; then CMD="ln -sf"; else CMD="ln -si"; fi
    $CMD "$2" "$3"
    if [[ $? -ne 0 ]]; then
        prompt_retry
        sudo $CMD "$2" "$3"
    fi
}

install_files() {
    echo "Installing configuration files"
    mkdir -p "$NGINX_CONF_DIR/includes/"
    if [[ $? -ne 0 ]]; then
        prompt_retry
        sudo mkdir -p "$NGINX_CONF_DIR/includes/"
    fi
    install_copy_file "$OVERWRITE_FILES" "$SCRIPT_DIR/nginx/conf/ffdhe2048.txt" "$NGINX_CONF_DIR/"
    install_symlink "$OVERWRITE_FILES" "$SCRIPT_DIR/nginx/conf/includes/orp_ssl_common.conf" "$NGINX_CONF_DIR/includes/"
    install_symlink "$OVERWRITE_FILES" "$SCRIPT_DIR/nginx/conf/orp.conf" "$NGINX_CONF_DIR/$SITES_ENABLED_SUBDIR/"
}

if [[ "$SHOULD_INSTALL" -eq 1 ]]; then
    install_files
else
    read -p "Do you want to do this automatically? [y/N]"
    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        install_files
    fi
fi

popd > /dev/null
