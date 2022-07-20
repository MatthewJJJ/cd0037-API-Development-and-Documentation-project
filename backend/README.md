# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### API Reference

`Base URL for now is http://127.0.0.1:5000/`

## Get Categories

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a key, `categories`, that contains an object of `id: category_string` key: value pairs, and a key of status which will have a value of success (if the request was successful).

# Request Response:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "status": "success"
}
```

## Get Questions

`GET '/questions?page=${integer}'`

- Fetches a set of questions, a total number of questions, all categories, and current category string.
- Request Arguments: page -> integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, current category string, and key of status which will have a value of success (if request was successful)

# Request Response:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "status": "success"
}
```

## Get Set of Questions for Category

`GET '/categories/${id}/questions'`

- Fetches questions for a category specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, current category string, and key of status which will have a value of success (if the request was successful).

# Request Response:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History",
  "status": "success"
}
```

## Delete Question

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: the removed question data in the removed_question key and a status key which will be success if the request is successful.

# Request Response:

```json
{
  "removed_question": {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  "status": "success"
}
```

## Run Quiz

`POST '/quizzes'`

- Sends a post request in order to get the next question

# Request Body:

```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": "current category"
}
```

# Request Response:

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  },
  "status": "success"
}
```

## Add Question

`POST '/questions'`

- Sends a post request in order to add a new question

# Request Body:

```json
{
  "question": "some question",
  "answer": "some answer",
  "difficulty": "3",
  "category": 1
}
```

# Response Body:

```json
{
  "new_question": {
    "answer": "some answer",
    "category": 1,
    "difficulty": 3,
    "id": 27,
    "question": "some question"
  },
  "status": "success"
}
```

## Search Questions

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term

# Request Body:

```json
{
  "searchTerm": "9"
}
```

# Response Body:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```
