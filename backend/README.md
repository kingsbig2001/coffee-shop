# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
## Endpoints
### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: `curl http://127.0.0.1:5000/categories`
- Response:
    ```
    {
    "drinks": [
        {
        "id": 1,
        "recipe": [
            {
            "color": "red",
            "parts": 1
            }
        ],
        "title": "Zobo"
        }
    ],
    "success": true
    }

    ```
### GET /drinks-detail
- General:
    - Same with /drinks route plus an additional name parameter on the returned drinks' recipe object
    - Requires a `get:drinks-detail` permission
- Sample: `curl http://127.0.0.1:5000/drinks-detail`
- Response:
    ```
    {
    "drinks": [
        {
        "id": 1,
        "recipe": [
            {
            "color": "red",
            "name": "zobo leaf",
            "parts": 1
            }
        ],
        "title": "Zobo"
        }
    ],
    "success": true
    }
    ```

### POST /drinks
- General:
    - This route is used to create a new drink
    - Requires a `post:drinks` permission
    - Request Arguments: 
        ```
        {
        "title": "Akamu Juice",
        "recipe": {
            "color": "white",
            "name": "pap",
            "parts": 1
        }
        }
        ```
- Response:
    ```
    {
    "drinks": [
        {
        "id": 1,
        "recipe": [
            {
            "color": "white",
            "name": "pap",
            "parts": 1
            }
        ],
        "title": "Akamu Juice"
        }
    ],
    "success": true
    }
    ```

### PATCH /drinks/1
- General:
    - This route is used to modify a drink
    - Requires a `patch:drinks` permission
    - Request Arguments: 
        ```
        {
        "title": "Akamu Juice",
        "recipe": {
            "color": "red",
            "name": "pap",
            "parts": 1
        }
        }
        ```
- Response:
    ```
    {
    "drinks": [
        {
        "id": 1,
        "recipe": [
            {
            "color": "red",
            "name": "pap",
            "parts": 1
            }
        ],
        "title": "Akamu Juice"
        }
    ],
    "success": true
    }
    ```

### DELETE /drinks/1
- General:
    - This route is used to delete a drink from the drink database
    - Requires a `delete:drinks` permission
    - Request Arguments: None      
- Response:
    ```
    {
    "delete": 1,
    "success": true
    }
    ```

## Tasks

- Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).


