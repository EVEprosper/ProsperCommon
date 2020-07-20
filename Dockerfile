ARG PARENT_DOCKER_IMAGE
FROM $PARENT_DOCKER_IMAGE

ARG VERSION 
ARG PROJECT_NAME=prosper-common
ARG PYTHON_VERSION=3.8.1
ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PATH="/opt/pyenv/shims:/opt/pyenv/bin:$PATH" \
    PYENV_ROOT="/opt/pyenv" \
    PYENV_SHELL="bash" \
    DEV_DIR="/opt/prosper"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		make \
		build-essential \
		libssl-dev \
		zlib1g-dev \
		libbz2-dev \
		libreadline-dev \
		libsqlite3-dev \
		wget \
		curl \
		llvm \
		libncurses5-dev \
		libncursesw5-dev \
		xz-utils \
		tk-dev \
		libffi-dev \
		liblzma-dev \
		python-openssl \
		git \
	&& apt-get install -y --reinstall ca-certificates \
	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

## Install pyenv: 
## https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/ 
RUN git clone https://github.com/pyenv/pyenv.git /opt/pyenv \
	&& pyenv install $PYTHON_VERSION \
	&& pyenv install 3.7.8 \
	&& pyenv install 3.6.11 

COPY . $DEV_DIR/$PROJECT_NAME
WORKDIR $DEV_DIR/$PROJECT_NAME
RUN pyenv local $PYTHON_VERSION 3.7.8 3.6.11
RUN pip3 install .[dev]