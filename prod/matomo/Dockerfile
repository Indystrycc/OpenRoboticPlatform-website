# syntax=docker/dockerfile:1
FROM matomo:fpm as final

# Configure php-fpm to listen on a UNIX socket
RUN sed -E -i "s,^listen = (127\.0\.0\.1:)?9000\$,listen = /run/matomo/matomo.sock\nlisten.mode = 0666,gm" /usr/local/etc/php-fpm.d/*
# Override default settings to make it work behind a proxy
RUN sed -i \
    -e "s/^;proxy_client_headers\[\] = HTTP_X_FORWARDED_FOR\$/proxy_client_headers[] = HTTP_X_FORWARDED_FOR/gm" \
    -e "s/^;proxy_host_headers\[\] = HTTP_X_FORWARDED_HOST\$/proxy_host_headers[] = HTTP_X_FORWARDED_HOST/gm" \
    -e "s/^force_ssl = 0\$/force_ssl = 1/gm" \
    /usr/src/matomo/config/global.ini.php
