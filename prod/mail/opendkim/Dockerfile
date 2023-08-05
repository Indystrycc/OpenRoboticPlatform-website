# syntax=docker/dockerfile:1
FROM debian:stable-slim as builder

RUN \
	--mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	apt-get update && \
	apt-get install --no-install-recommends -y libc6-dev gcc ca-certificates wget unzip

RUN wget https://github.com/ossobv/syslog2stdout/archive/142793f15169fa01c0e1249fbb0d71516e328e65.zip -O source.zip && \
    unzip source.zip && \
    mv syslog2stdout-142793f15169fa01c0e1249fbb0d71516e328e65 syslog2stdout && \
    cd syslog2stdout && \
    cc -O3 -o syslog2stdout syslog2stdout.c


FROM debian:stable-slim as deploy

RUN \
	--mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y opendkim opendkim-tools openssl bind9-host

COPY --from=builder /syslog2stdout/syslog2stdout /usr/bin/syslog2stdout
COPY opendkim/ /etc/opendkim/
COPY opendkim.conf /etc/
COPY docker-entrypoint.sh /

EXPOSE 12301

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "opendkim", "-f" ]
