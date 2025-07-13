# Local PyPI Setup with `devpi`

 **Local PyPI server** using [Devpi](https://github.com/devpi/devpi), running in a Docker container. This server acts like a private PyPI repository for:

* **Hosting your own packages**
* **Proxying public PyPI for caching**
* **Isolated dev/test publishing workflows**

## ⚙️ Workflow Summary

1. **Run Devpi Server**:

   ```bash
   make run
   ```

2. **Initialize Devpi (user, index)**:

   ```bash
   make init
   ```

3. **Login to Devpi**:

   ```bash
   make login
   ```

4. **Build Package with Poetry**:

   ```bash
   make build
   ```

5. **Upload Package with Twine**:

   ```bash
   make upload
   ```

## 📦 Poetry Configuration to Use Devpi

Add the Devpi repository to your `pyproject.toml` like this:

```toml
[tool.poetry]
name = "your-package"
version = "0.1.0"
...

[[tool.poetry.source]]
name = "devpi"
url = "http://localhost:3141/myuser/dev"
default = false
```

Then install with:

```bash
poetry install --source devpi
```

To publish via **Poetry directly**, also add your credentials to Poetry config:

```bash
poetry config http-basic.devpi myuser secret
poetry publish --build -r devpi
```


### 🔁 Summary Table

| Step       | Command                                    | Description            |
| ---------- | ------------------------------------------ | ---------------------- |
| Run server | `make run`                                 | Starts Devpi in Docker |
| Init index | `make init`                                | Sets up user and index |
| Login      | `make login`                               | Logs in to Devpi       |
| Build      | `make build`                               | Builds Python package  |
| Upload     | `make upload` or `poetry publish -r devpi` | Uploads to Devpi       |
