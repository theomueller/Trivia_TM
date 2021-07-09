

********************************************
****      Project Basic TRIVIA APP      ****
********************************************


# Description
Based on the UDACITY project, this version of the trivia app enables the user to play the game, but there is still a lot of possible improvements

That's where you come in! Help the community to improve this version of the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. 

What the application does:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

What the application would need:

1. Add an additional question field such as rating and make all corresponding updates (db, api endpoints, add question form, etc.)
2. Add users to the DB and track their game scores
3. Add capability to create new categories.

# Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines. Please refer to the corresponding internet pages to get these packages installed. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

# Install DB
... from Readme Back End

To run the application run the following commands from the backend folder : 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

if you have issue concering npm installation try
```
 npm audit fix --force
```
By default, the frontend will run on localhost:3000. 

### UNIT TESTS
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb triviadb_test
createdb triviadb_test
psql triviadb_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

Ergebnisse:
```
........
............
----------------------------------------------------------------------
Ran 12 tests in 0.429s
OK
```

###  API REFERENCE
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed 
- 422: Unprocessable
- 500: Internal server error 

### Endpoints 
#### GET /questions
- General:
    - Returns the list of categoies, the list of questions, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

`curl http://127.0.0.1:5000/questions`
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
  "current_categorie": 0, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
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
    }
  ], 
  "success": true, 
  "total_questions": 19
}

```

#### POST /Questions
- General:
    - Creates a new question using the submitted question, category, answer and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"question":"Who created the light bulb", "answer":"Edison", "category":"1","difficulty":"2"}'`
```
{
  "id": 26, 
  "success": true, 
  "total_questions": 22
}
```

#### POST /Questions with Search
- General:
    - Searches for a question based on a search term. 
    Returns any questions for whom the search term is a substring of the question.

- `curl http://127.0.0.1:5000/questions\?page\=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"caged"}'`
```
 {
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "success": true
}
```   
if no question is found, the route will return:
```
{
  "questions": [], 
  "success": false
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question  of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/26`
```
{
  "questions": [
    {
      "answer": "Edison", 
      "category": 1, 
      "difficulty": 2, 
      "id": 25, 
      "question": "Who created the light bulb"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```
#### POST /quizzes/
 - General:
    -  Get questions to play the quiz. 
        This endpoint takes category (be carefull: provide an object category, at least {"id":"xxx"}) and previous question parameters and returns a random questions within the given category, 
        if provided, and that is not one of the previous questions. 

- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":"", "quiz_category":{"id":"1"}}'`
```
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true, 
  "total_questions": 4
  ```


## Authors
Changes from starter done by me: Thibaut Meunier 

## Acknowledgements 
Thanks Coach Carin for the great teaching !
And Thanks to the awesome team at Udacity !
Good lock for all of the students, soon to be full stack extraordinaires! 