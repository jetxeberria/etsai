#!/bin/bash

# Makefile file to host common environment targets

PDM := pdm

.PHONY: clean

# Set up the system (run only once on the system)
setup-system:
	@echo "System setup is complete."

# Initialize the repository (run only once on the repository)
init-repo: init-git-repository setup-repo
	@echo "Repository is initialized."

init-git-repository:
	@echo "Initizalizing the repository..."
	git init

# Set up the repository environment (run each time repo is cloned)
setup-repo:  _create-env
	@echo "Repository environment is set up. Activate it with 'source .venv/bin/activate'."

_create-env: _check-no-env
	@echo "Creating and activating the PDM environment..."
	$(PDM) install

_check-no-env:
	@echo "Checking no environment is activated..."
	@if [ -n "$${VIRTUAL_ENV}" ]; then \
		echo "\nError: Environment is already activated!"; \
		echo "Please deactivate the current environment and try again.\n"; \
		exit 1; \
	fi
	@echo "OK"

# Update the repository environment with remote changes (run each time after pulling changes)
update-repo: _check-env-ok _update-template _update-env
	@echo "Repository environment is updated."

_check-env-ok:
	@echo "Checking if the correct environment is activated..."
	@PROJECT_NAME=$$(basename "$$(pwd)"); \
	ENV_NAME=$$(basename "$$(dirname "$${VIRTUAL_ENV}")"); \
	if [ "$$ENV_NAME" != "$$PROJECT_NAME" ]; then \
		echo "\nError: A different environment is activated ($$ENV_NAME) instead of expected ($$PROJECT_NAME)!"; \
		echo "Please deactivate the current environment, activate the correct environment and try again.\n"; \
		exit 1; \
	fi
	@echo "OK"

_update-template:
	@echo "Updating the Copier template..."
	copier update

_update-env:
	@echo "Updating the local environment with new dependencies..."
	$(PDM) sync

# Clean up the environment
clean:
	@echo "Cleaning up..."
	rm -rf __pypackages__
	rm -rf __pycache__
	rm -rf .pdm-python

# Add new package to the environment.
add-package: _check-env-ok
	@package_name=$${package_name}; \
	if [ -z "$$package_name" ]; then \
		if [ -z "$1"]; then \

		read -p "Enter package name to add: " package_name; \
		else \
			package_name=$1; \
			fi; \
	fi; \
	$(PDM) add $$package_name
	@echo "Package $$package_name added."

# Remove package from the environment.
remove-package: _check-env-ok
	@read -p "Enter package name to remove: " package_name; \
	$(PDM) remove $$package_name
	@echo "Package $$package_name removed."

# Update package in the environment.
update-package: _check-env-ok
	@read -p "Enter package name to update: " package_name; \
	$(PDM) update $$package_name
	@echo "Package $$package_name updated."
