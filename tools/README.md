# Tools - Development Support scripts and tools

This folder contains helper tools and utilities to support local development, testing, and automation workflows.

#### Structure

```
tools/
├── localpypi/     # Setup for running a local PyPI server using Docker
│   ├── Makefile   # Make targets for starting, uploading, and managing packages
│   └── README.md  # Usage instructions for local PyPI
└── scripts/       # Generic reusable scripts (e.g., setup, CI helpers, etc.)
```

#### Usage

* Use `localpypi/` to simulate publishing Python packages locally for testing.
* Use `scripts/` to add Bash/Python utility scripts for automation, project scafollding.

.
