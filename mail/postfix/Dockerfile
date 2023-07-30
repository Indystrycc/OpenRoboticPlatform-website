# syntax=docker/dockerfile:1
FROM debian:stable-slim

RUN \
	--mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && \
	apt-get install -y postfix

# TODO configure postfix
COPY main.cf /etc/postfix/main.cf

COPY docker-entrypoint.sh /

EXPOSE 25

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "postfix", "start-fg" ]
