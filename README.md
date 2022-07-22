# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

### API Reference

### Starting the API

1. First, intialize the python virtual environment: `python -m virtualenv env`
2. Second, activate the python virtual environment: `source env/Scripts/activate`
3. Third, install the project dependencies: `pip install -r requirements.txt`
4. Finally, run the project: `FLASK_APP=flaskr FLASK_DEBUG=true flask run`

**Note: You can override any of the DB settings by specifying a DB_HOST, DB_USER, DB_PASSWORD, or DB_NAME in the run command.**

`Base URL for now is http://127.0.0.1:5000/`

Hit http://127.0.0.1:5000/ to see the message `Hello from the Udacity quiz question API!` to confirm the API is running correctly.

#### Get Categories

`GET '/categories'`

- Gets and object of categories in which the keys are the ids and the value is the category
- Request Arguments: None
- Returns: An object with a key, `categories`, that contains an object of `id: category_string` key: value pairs, and a key of status which will have a value of success (if the request was successful).

###### Request Response:

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

#### Get Questions

`GET '/questions?page=${integer}'`

- Gets a set of questions on a page, a total number of questions, all categories, and current category string.
- Request Arguments: page -> integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, current category string, and key of status which will have a value of success (if request was successful)

##### Request Response:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Test Question",
      "answer": "Test Answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 19,
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

#### Get Set of Questions for Category

`GET '/categories/${id}/questions'`

- Gets a list of questions corresponding to a category specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, current category string, and key of status which will have a value of success (if the request was successful).

##### Request Response:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Test Question",
      "answer": "Test Answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 19,
  "currentCategory": "History",
  "status": "success"
}
```

#### Delete Question

`DELETE '/questions/${id}'`

- Deletes a question using the question's id
- Request Arguments: id - integer
- Returns: the removed question data in the removed_question key and a status key which will be success if the request is successful.

##### Request Response:

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

#### Run Quiz

`POST '/quizzes'`

- Sends a post request in order to get the next question

##### Request Body:

```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": "current category"
}
```

##### Request Response:

```json
{
  "question": {
    "id": 1,
    "question": "Test Question",
    "answer": "Test Answer",
    "difficulty": 5,
    "category": 4
  },
  "status": "success"
}
```

#### Add Question

`POST '/questions'`

- Sends a post request in order to add a new question

##### Request Body:

```json
{
  "question": "Test Question",
  "answer": "Test Answer",
  "difficulty": "3",
  "category": 1
}
```

###### Response Body:

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

#### Search Questions

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term

##### Request Body:

```json
{
  "searchTerm": "9"
}
```

##### Response Body:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Test Question",
      "answer": "Test Answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 19,
  "currentCategory": "Entertainment"
}
```

#### Handling Errors

An error will respond with the following format:

```json
{
  "error": ###,
  "message": "description of the error",
  "status": "error"
}
```
