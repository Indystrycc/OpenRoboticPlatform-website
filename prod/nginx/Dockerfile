# syntax=docker/dockerfile:1
FROM nginx:mainline as final

# Copy config files
COPY prod/nginx /etc/nginx

# Prepare static files
COPY --chmod=644 website/static /data/static
RUN find /data/static -type f -not -empty -exec sh -c "gzip -c -9 {} > {}.gz" \; && \
    find /data/static -type d -exec chmod 755 "{}" \;

EXPOSE 80 443
