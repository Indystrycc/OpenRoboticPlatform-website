# syntax=docker/dockerfile:1
FROM nginx:mainline as final

# 15-local-resolvers.envsh isn't in the published image yet
COPY <<-EOT /docker-entrypoint.d/15-local-resolvers.envsh
#!/bin/sh
# vim:sw=2:ts=2:sts=2:et

set -eu

LC_ALL=C
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

if [ "\${NGINX_ENTRYPOINT_LOCAL_RESOLVERS}" ]; then
  export NGINX_LOCAL_RESOLVERS=$(awk 'BEGIN{ORS=" "} \$1=="nameserver" {print \$2}' /etc/resolv.conf)
fi
EOT
RUN chmod +x /docker-entrypoint.d/15-local-resolvers.envsh

# Copy config files
COPY prod/nginx /etc/nginx

# Prepare static files
COPY --chmod=644 website/static /data/static
RUN find /data/static -type f -not -empty -exec sh -c "gzip -c -9 {} > {}.gz" \; && \
    find /data/static -type d -exec chmod 755 "{}" \;

EXPOSE 80 443
