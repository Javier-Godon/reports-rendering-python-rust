CI/CD
Use dagger python In a python project is very straightforward (I am assuming that this pipeline is always
related with this project, otherwise I will create an independent python project for it)
1. Create folder dagger_python
2. create a main.py
3. add the necessary dependencies to the dependencies.txt of the main project

To generate the image take into account: https://fastapi.tiangolo.com/deployment/docker/#package-requirements
In this case we have to consider that we are using Rust and we have to compile this part of the code using maturin

Configure github with the required permissions and environment variables

![image](./resources/add_secrets_to_github.png)

![image](./resources/GITHUB_TOKEN_permissions.png)

Create a Dockerfile


Create dagger pipeline in dagger_python/main.py

In order to run the dagger pipeline in pycharm configure a run with the .env (added to credentials and .gitignore)

![image](./resources/credentials_env.png)

![image](./resources/pycharm_run_with_env_variables.png)