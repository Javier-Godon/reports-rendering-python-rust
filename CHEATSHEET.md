## Initializing a Rust Project

To initialize a Rust project, use:

```sh
cargo new <project-name>
```

In this case, it is recommended to use `maturin`:

```sh
maturin new -b pyo3 <project-name>
```

This will generate the necessary configurations.

## Project Structure Adjustment

To keep the Python project structure untouched, extract all components outside of the created folder into your existing project. Specifically:

- Move `src` to the same level as `app`.
- Place `Cargo.toml` and `pyproject.toml` at the root of your project.
- Delete the now-empty `<project-name>` folder.

## Building the Rust Module

Once the Rust code is finished, build the Rust module by executing the following command from the root of the project:

```sh
maturin develop
```

This command:

- Builds the Rust module.
- Installs it as a Python package in your virtual environment.
- Makes it available for import inside your app modules.

