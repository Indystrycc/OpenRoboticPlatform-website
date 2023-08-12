# syntax=docker/dockerfile:1
FROM node:current-slim as theme

WORKDIR /theme
COPY /theme .

RUN --mount=type=cache,target=/root/.npm npm install

RUN npm run build

FROM nginx:mainline as final

# Copy config files
COPY prod/nginx /etc/nginx

# Prepare static files
COPY --chmod=644 website/static /data/static
COPY --from=theme --chmod=644 /theme/dist/styles.css /data/static/css/theme.css
RUN find /data/static -type f -not -empty -exec sh -c "gzip -c -9 {} > {}.gz" \; && \
    find /data/static -type d -exec chmod 755 "{}" \;

EXPOSE 80 443
