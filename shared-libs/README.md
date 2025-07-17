# Shared Libraries

## Modules

* **commons-shared-libs/**
  
  Contains reusable libraries shared across services:

  * `client-connectors`: Handles client communication logic.
  * `observability`: Provides logging, metrics, and tracing tools.
  * `service-management`: Manages service lifecycle and configurations.

* **peristence-shared-libs/**

  Provides persistence logic for different databases:

  * `cassandra_persistence`: Integration with Cassandra DB.
  * `mongo_persistence`: Integration with MongoDB.
  * `postgres_persistence`: Integration with PostgreSQL.


## Makefile Target

Each module have the following buld targets for initializing the environment, build, test and publishing the library to local `devpi` python repository. The project use poetry as a package manager.

| Target          | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| `help`          | 📖 Lists all available make commands with descriptions.                      |
| `repo.config`   | 🧰 Configures Poetry to use the local PyPI repository.                       |
| `init.python`   | 🧰 Sets up the Python environment using `poetry` and the latest Python 3.12. |
| `init`          | 🧰 Generic alias for initializing the environment.                           |
| `build`         | 🏗️ Builds the Python source distribution using Poetry.                      |
| `clean`         | 🧹 Deletes temp files, cache, build artifacts, and more.                     |
| `format.python` | 🎨 Formats code using [Ruff](https://docs.astral.sh/ruff/).                  |
| `lint.python`   | 🔍 Lints code using Ruff and MyPy for static analysis.                       |
| `test`          | ✅ Runs all tests using Pytest and shows coverage.                            |
| `publish`       | 🚀 Publishes package to the local PyPI repo using Poetry.                    |

