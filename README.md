I'm a student at Gunadarma University. I have never done this before. I mainly work on game modding, reverse engineering, and other tech-related tasks.
Flask is used because it's easier to set up and run, and it's beginner-friendly, and also I had no time to create something new and complex.

-*mfarrellr*

# Simple Web-based CRUD

Development of a Web-based CRUD Application to Meet GUCC Requirements.

Code written in Python 3.11.11 with a conda environment. Please ensure everything is set up correctly, as Python can be quite tricky at times.
## Run Locally
Ensure that the crud database is created in your database management system (DBMS)

```bash
  CREATE DATABASE crud;
```

Once the database crud has been created, proceed to import the provided SQL file into the database.

Clone the project

```bash
  git clone https://github.com/ftdaily/simple-webbased-crud
```

Go to the project directory

```bash
  cd simple-webbased-crud
```

Install dependencies

```bash
  pip install -r requirement.txt
```

Start the server

```bash
  python main.py
```

If you encounter a problem such as `module not found`, it might be due to using a different version of Python or a different global environment.

Please make sure you use correct environment or use virtual environment.

Conda environment
```bash
    conda create --name .myEnv 
```

Make sure you had the conda environment created
```bash
    conda info --envs
```

Activate the environment
```bash
    conda activate .myEnv
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

