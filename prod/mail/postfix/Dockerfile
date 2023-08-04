# syntax=docker/dockerfile:1
FROM debian:stable-slim

RUN \
	--mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y postfix bind9-host

COPY main.cf /etc/postfix/main.cf
COPY docker-entrypoint.sh /

EXPOSE 25

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "postfix", "start-fg" ]
