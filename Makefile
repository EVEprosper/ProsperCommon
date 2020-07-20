describe-parse = $(word $2,$(subst -, ,$1))

VERSION=$(call describe-parse,$(shell git describe),1)
PARENT_DOCKER_IMAGE=ubuntu:xenial

DOCKER_GROUP = 'eveprosper'
PROJECT_NAME = 'prosper-common'
DOCKER_IMAGE_NAME = ${DOCKER_GROUP}/${PROJECT_NAME}:${VERSION}

dummy:
	@echo ${VERSION}
.PHONY: clean
clean:
	@rm -rf .venv
	@rm -rf dist
	@rm -rf .tox
	@touch Dockerfile
	@touch setup.py
	@rm -f docker-build

docker-build: Dockerfile setup.py
	@docker build \
		--build-arg PARENT_DOCKER_IMAGE=${PARENT_DOCKER_IMAGE} \
		--build-arg PROJECT_NAME=${PROJECT_NAME} \
		--tag ${DOCKER_IMAGE_NAME} \
		-f Dockerfile \
		.

	@touch $@

test: docker-build
	@docker run --rm -it \
		${DOCKER_IMAGE_NAME} \
		tox ${TOX_ARGS}

run: docker-build
	@docker run --rm -it \
		${DOCKER_IMAGE_NAME} \
		/bin/bash

BLACK_DEFAULTS=-l 100 --check
black: docker-build
	@docker run --rm -it \
		${DOCKER_IMAGE_NAME} \
		black ${BLACK_DEFAULTS} .
