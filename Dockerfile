# syntax=docker/dockerfile:1
FROM python:3.11-slim as build

# install mysqlclient requirements
RUN \
	--mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y default-libmysqlclient-dev build-essential

# upgrade pip
RUN pip install --upgrade pip

WORKDIR /app

# set-up venv
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv --upgrade-deps $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY requirements.txt ./prod/requirements-prod.txt ./
RUN \
	--mount=type=cache,target=/root/.cache/pip \
	pip install -r requirements-prod.txt


FROM python:3.11-slim as deploy

# install mysqlclient without build-essential (this copy will work only with --no-cache)
COPY --from=build /var/lib/apt/lists /var/lib/apt/lists
RUN \
	--mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y libmariadb3

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# copy the environment from build
COPY --from=build /app .

# copy remaining files
COPY prod/gunicorn.conf.py .
COPY main.py .
COPY website website/

CMD [ "gunicorn" ]
