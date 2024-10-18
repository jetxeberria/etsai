# Makefile file to host common package management targets

PDM := pdm

# Plan the release of a new version
plan-release:
	@read -p "Enter the new version (e.g., 1.0.0): " new_version; \
	$(PDM) version $${new_version}

# Build a release candidate for validation
build-rc:
	@$(PDM) version --pre-release
	@$(PDM) build
	@echo "Release candidate built and version updated."

# Build a final release
build-release:
	@$(PDM) version --finalize
	@$(PDM) build
	@echo "Release finalized and version updated."

# Reset the version planning
reset-version:
	@$(PDM) version --reset
	@echo "Version planning reset."


