#!/bin/bash

# Include common and specific makefiles
include makefiles/common/environment.mk
include makefiles/common/package.mk
include makefiles/specific.mk

# Default target
.PHONY: help


help:
	@echo "Makefile"
	@echo "Available targets:"

	@targets=$$(grep -hE '^[a-zA-Z][a-zA-Z_-]*:' \
		makefiles/common/environment.mk \
		makefiles/common/package.mk \
		makefiles/specific.mk | awk -F':' '{print $$1}' | sort | uniq); \
	\
	max_length=$$(echo "$$targets" | awk '{ if (length > max) max = length } END { print max }'); \
	\
	echo "$$targets" | while read -r target; do \
		desc=$$(grep -hB1 "^$$target:" \
			makefiles/common/environment.mk \
			makefiles/common/package.mk \
			makefiles/specific.mk | head -n1 | sed 's/#//'); \
		printf "  %-*s  %s\n" $$max_length "$$target" "$$desc"; \
	done; \
	\
	printf "  %-*s  %s\n" $$max_length "help" " Show this help message"

	
