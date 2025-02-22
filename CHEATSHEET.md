to initialize a rust project cargo new <project-name>
In this case is recommended to use maturin; 
maturin new -b pyo3 <project-name>
This will give me the needed configurations.
To keep my python project untouched I am going to extract all components outside of this folder to my project, so src will be at the same level of app, and cargo.toml and pyproject.toml will be at the root of my project
And then delete the created folder (project-name) that at this point shold be empty
once my code is finished we have to build the Rust module: execute this command from the root of the project
maturin develop

this: 
- Builds the Rust module
- Install it as a Python package in your virtual environment
- Makes it available for import inside your app modules