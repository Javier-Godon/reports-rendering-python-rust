# CI/CD

## Use Dagger with Python

Using Dagger in a Python project is very straightforward. (I assume that this pipeline is always related to this project; otherwise, I would create an independent Python project for it.)

### Steps:
1. Create a folder `dagger_python`.
2. Create a `main.py` file.
3. Add the necessary dependencies to the `dependencies.txt` of the main project.

### Generating the Image
To generate the image, take into account: [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/#package-requirements).

In this case, since we are using Rust, we must compile this part of the code using `maturin`.

## Configure GitHub with Required Permissions and Environment Variables

![Add Secrets to GitHub](/resources/add_secrets_to_github.png)

![GitHub Token Permissions](/resources/GITHUB_TOKEN_permissions.png)

## Create a Dockerfile

## Create a Dagger Pipeline in `dagger_python/main.py`

## Running the Dagger Pipeline in PyCharm
To run the Dagger pipeline in PyCharm, configure a run with the `.env` file (added to credentials and `.gitignore`).

![Credentials .env](/resources/credentials_env.png)

![PyCharm Run with Environment Variables](/resources/pycharm_run_with_env_variables.png)

you can find all necessary configurations for a fully functional CI/CD in this repository (dagger_python, .github/workflows) and in [Cluster continuous delivery](https://github.com/Javier-Godon/cluster-continuous-delivery)
