# 🐍 Learn Python by Doing

This is a personal monorepo to explore, experiment, and build reusable libraries and tools while learning Python through real-world patterns and projects.


## 📁 Folder Structure

```

.
├── notes/                  # Learning notes, sketches, and experiments
├── shared-libs/           # Reusable libraries
│   ├── connector/         # HTTP and WebSocket clients with extensions
│   └── observability/     # Logging, metrics, and tracing wrappers
├── tools/                 # Development and automation tools
│   ├── localpypi/         # Docker-based local PyPI server setup
│   └── scripts/           # Misc utility scripts (setup, testing, CI, etc.)

```


## 🚀 Getting Started

Each component is self-contained with its own README.

- [`tools/localpypi`](tools/localpypi/README.md) – Run your own PyPI registry.
- [`shared-libs/connector`](shared-libs/connector/) – Custom HTTP/WebSocket clients.
- [`shared-libs/observability`](shared-libs/observability/) – Unified observability layer.


> ⚠️ **Disclaimer**  
> This repository is for **personal learning and reference** only. The code and utilities here are **not production-ready**. Using any part of this in production will likely require **additional validation, improvements, and testing**.
