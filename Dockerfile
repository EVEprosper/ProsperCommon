ARG PARENT_DOCKER_IMAGE
FROM $PARENT_DOCKER_IMAGE

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PATH="/opt/pyenv/shims:/opt/pyenv/bin:$PATH" \
    PYENV_ROOT="/opt/pyenv" \
    PYENV_SHELL="bash"

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
RUN git clone https://github.com/pyenv/pyenv.git /opt/pyenv