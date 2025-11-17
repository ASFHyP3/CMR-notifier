# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2]

### Fixed
- `build-and-deploy.yml` GitHub Action workflow now specifies the deployment maturity from the computed version number, not the `github.ref`. 

## [0.1.1]

### Fixed
- `build-and-deploy.yml` GitHub Action workflow now runs on a new tag event instead of on pushes to main after the New Tag Version workflow is finished.

## [0.1.0]

### Added
- A Sentinel-1 SLC and Sentinel-1 Burst notification topic
