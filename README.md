# GRAIL SOLVER

### Description
GrailSolver is a cutting-edge solver that uses advanced text analysis techniques and optimisation tools to model and solve constraint satisfaction problems.

### Installation
- Clone the GitHub repository.

    - `git clone https://github.com/grail-solver/grail-cp-solver.git` <br>
    - `cd cp_graal_solver`

- Install all packages required findable in requirements.txt file
- > `pip install -r requirements.txt`
- Copy the .env file and setup all required field
- > `cp .env.example .env`
- Update lines about database informations in `env.py` file

### Usage

- Activate your environment if you're using one 
- Start graal solver app
- > `uvicorn main:app --reload`
- Go to http://127.0.0.1:8000/docs for interact with the api without frontend side


### License
All rights reserved.
