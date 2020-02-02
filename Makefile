# Makefile that has tasks to support the following
# - Build docker image
# - Push docker image to registry

PROJECT_NAME=sidious
VERSION="0.0.1"
IMAGE="ahardt013/${PROJECT_NAME}:${VERSION}"
IMAGE_LATEST="ahardt013/${PROJECT_NAME}:latest"
TOKEN = ${DISCORD_TOKEN}

default: build


build:
	@echo ? Building docker image for ${PROJECT_NAME}.
	@docker build -t ${IMAGE_LATEST} .


publish: build
	@echo ? Pushing docker image to docker hub.
	@docker tag ${IMAGE_LATEST} ${IMAGE}
	@docker push ${IMAGE}
	@docker push ${IMAGE_LATEST}


dev: build
	@echo ? Running docker container locally.
	@docker run --rm -it -d -e DISCORD_TOKEN=${TOKEN} ${IMAGE_LATEST}
