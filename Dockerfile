# syntax=docker/dockerfile:1
FROM node:current-slim as theme

WORKDIR /theme
COPY /theme .

RUN --mount=type=cache,target=/root/.npm npm install

RUN npm run build

FROM python:3.12-slim as build

# install mysqlclient requirements
RUN \
	--mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y default-libmysqlclient-dev build-essential pkg-config

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


FROM python:3.12-slim as deploy

# install mysqlclient without build-essential
RUN \
	--mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
	rm -f /etc/apt/apt.conf.d/docker-clean; \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
	apt-get update && \
	apt-get install -y libmariadb3

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=main
# copy the environment from build
COPY --from=build /app .

# copy migrations
COPY migrations migrations/

# copy remaining files
COPY prod/gunicorn.conf.py .
COPY main.py .
COPY website website/

# copy the theme and overwrite
COPY --from=theme /theme/dist/styles.css website/static/css/theme.css

CMD [ "/bin/sh", "-c", "flask db upgrade && gunicorn" ]
