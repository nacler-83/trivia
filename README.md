# Full Stack Trivia API


## Introduction
This is a trivia game including both a frontend (react) and backend (flaskr). It uses a postgresql database and stores trivia quesitons, answers and categories.


## Getting Started
* Base URL: at present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
* API Keys /Authentication: this version of the application does not require authentication or API keys


## Installation
Backend:
* From the root directory, `cd backend` and create a virtual environment.
* Once your virtual environment is up and running, install dependencies by `pip install -r requirements.txt`
* Create a postgress table like `createdb trivia` and save the table name into `models.py`
* Bootstrap the database with data with `psql trivia < trivia.psql`
* Run `bash launch.sh` to start the backend in development mode. You might need to `chmod -x launch.sh` first.

Frontend:
* From the root directory, `cd frontend`
* Run `npm install` to install dependencies
* Run `npm start` to start the frontend in development mode


## Errors
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return three error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable


## Testing
For backend tests, navigate to backend folder and run `bash run_tests.sh`. You might need to `chmod -x run_tests.sh` first. Otherwise, you can run the following.
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```


## Backend Endpoints

### GET /categories

**General**
Returns the game category id and names.

**Sample Request**
`curl -X GET http://127.0.0.1:5000/categories`

**Sample Response**
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /questions

**General**
* returns paginated questions, num of total questions, and the cateogies
* accepts optional `?page=` parameter, returning question in groups of 10

**Sample Request**
`curl -X GET http://127.0.0.1:5000/questions`

**Sample Response**
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### DELETE /questions/<question_id>

**General**
Deletes a question given a question id

**Sample Request**
`curl -X DELETE http://127.0.0.1:5000/questions/5`

**Sample Response**
```
{
  "success": true
}
```

### POST /questions (without search)

**General**
Allows you to create a new question

**Sample Request**
```
curl --header "Content-Type: application/json" \
  -X POST \
  -d '{
            "question": "What is the meaning of life?",
            "answer": "42",
            "difficulty": 2,
            "category": 4
        }' \
  http://127.0.0.1:5000/questions
```

**Sample Response**
```
{
  "new_question": 27,
  "success": true
}
```

### POST /questions (with search)

**General**
Allows you to search the questions by providing `searchTerm` in body.

**Sample Request**
```
curl --header "Content-Type: application/json" \
  -X POST \
  -d '{
        "searchTerm": "who"
      }' \
  http://127.0.0.1:5000/questions
```

**Sample Response**
```
{
  "current_category": "",
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### GET /categories/<category_id>/questions

**General**
Get all the questions in a given category

**Sample Request**
`curl -X GET http://127.0.0.1:5000/categories/1/questions`

**Sample Response**
```
{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### POST /quizzes

**General**
Play the game. Begin by passing it a category, and then passing the questions the user has already seen.

**Sample Request**
```
curl --header "Content-Type: application/json" \
  -X POST \
  -d '{
        "previous_questions": [16, 17],
        "quiz_category": {
            "type": "Art",
            "id": "2"
        }
      }' \
  http://127.0.0.1:5000/quizzes
```

**Sample Response**
```
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}
```
