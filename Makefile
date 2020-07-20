VERSION=$(shell git describe)
PARENT_DOCKER_IMAGE=ubuntu:xenial

DOCKER_GROUP = 'eveprosper'
PROJECT_NAME = 'prosper-common'
DOCKER_IMAGE_NAME = ${DOCKER_GROUP}/${PROJECT_NAME}:${VERSION}

.PHONY: clean
clean:
	@rm -rf .venv
	@rm -rf dist
	@rm -rf .tox
	@touch Dockerfile
	@touch setup.py

docker-build: Dockerfile setup.py
	@docker build \
		--build-arg PARENT_DOCKER_IMAGE=${PARENT_DOCKER_IMAGE} \
		--tag ${DOCKER_IMAGE_NAME} \
		-f Dockerfile \
		.

	@touch $@

test: docker-build
	@docker run --rm -it \
		${DOCKER_IMAGE_NAME} \
		/bin/bash
