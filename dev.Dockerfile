# syntax=docker/dockerfile:1
FROM node:current-slim as theme

WORKDIR /theme
COPY /theme .

RUN --mount=type=cache,target=/root/.npm npm install

RUN npm run build

FROM python:3.11-slim as build

# install mysqlclient requirements
RUN \
	--mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
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
COPY requirements.txt .
RUN \
	--mount=type=cache,target=/root/.cache/pip \
	pip install -r requirements.txt


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
COPY main.py .
COPY website website/

# copy the theme and overwrite
COPY --from=theme /theme/dist/styles.css website/static/css/theme.css

EXPOSE 5004
CMD [ "flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5004", "--debug" ]
