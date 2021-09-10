# Define environment of running makefile. [DEV_TESTING, DEV_LOCAL]
# Default: DEV_LOCAL
ENVIRONMENT ?= DEV_LOCAL

stop-docker-containers:
# Free up memory and cpu in the k8 node
	docker-compose --ansi never -f ci-cd/integration/docker-compose.testing.yaml down

build-docker-image:
ifeq ($(ENVIRONMENT),DEV_TESTING)
# On dev-testing, build with no-cache so all pip packages will be reinstalled then bring containers up
	docker-compose -f ci-cd/integration/docker-compose.testing.yaml build \
		--no-cache --force-rm
	docker-compose --ansi never -f ci-cd/integration/docker-compose.testing.yaml up \
		--detach
else
# On dev-local, bring containers up and apply only code changes without reinstalling pip packages
	docker-compose -f ci-cd/integration/docker-compose.local.yaml up \
		--remove-orphans --build --detach --force-recreate
endif

run-tests:
ifeq ($(ENVIRONMENT),DEV_TESTING)
	docker-compose --ansi never -f ci-cd/integration/docker-compose.testing.yaml \
		run fastapi-base-test-dev .venv/bin/pytest \
		tests/ \
		--color=no
else
	docker-compose --ansi never -f ci-cd/integration/docker-compose.local.yaml \
		run fastapi-base-test-dev .venv/bin/pytest \
		tests/ \
		-x -vv -s
endif

build-and-test: build-docker-image run-tests stop-docker-containers

# cmd: Clean up
clean: clean-pyc clean-images
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
clean-images:
	docker system prune --force
