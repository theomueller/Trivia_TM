import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
    page = request.args.get('page',1,type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current_questions = [question.format() for question in selection[start:end]]
  
    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categoriesDB = Category.query.order_by(Category.type).all()
    categories = {category.id: category.type for category in categoriesDB}

    if len(categories) == 0:
      abort(404)

    return jsonify({
        'success': True,
        'categories': categories,
        'total_categories': len(categories)
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  -> DONE
  '''
  @app.route('/questions')
  def retrieve_questions():
    categoriesDB = Category.query.order_by(Category.id).all()
    categories = {category.id: category.type for category in categoriesDB}

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request,selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_categorie': 0,
        'categories': categories,
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  -> DONE (an improvement will be to trigger the refresh or to use a state to update the page)
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'] )
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.category).all()
      current_questions = paginate_questions(request,selection)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all())})

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab. 
  -> DONE (It will good to get a feedback displayed to the user that it was successull) 
  '''
  @app.route('/questions',methods=['POST'])
  def post_question():
    body = request.get_json()
    search = body.get('searchTerm', None)
    # if not search in the body -> Create 
    if not search:
      new_question  = body.get('question', None)
      new_answer = body.get('answer',None)
      new_category = body.get('category',None)
      new_difficulty = body.get('difficulty',None)

      # add a test to avoid creating empty questions
      if new_question is None or new_answer is None or new_category is None or  new_difficulty is None:
        abort(400)

      try:
          question = Question(
          question = new_question,
          answer = new_answer,
          category = new_category,
          difficulty = new_difficulty
          )
          question.insert()

          categoriesDB = Category.query.order_by(Category.id).all()
          categories = {category.id: category.type for category in categoriesDB}

          selection = Question.query.order_by(Question.category).all()
          current_questions = paginate_questions(request,selection)

          return jsonify({
            'success': True,
            'id': question.id,
            'total_questions': len(selection),
            #'current_categorie': 0,
            #'categories': categories,
          })

      except:
          abort(422)

          '''
          @TODO: 
          Create a POST endpoint to get questions based on a search term. 
          It should return any questions for whom the search term 
          is a substring of the question. 

          TEST: Search by any phrase. The questions list will update to include 
          only question that include that string within their question. 
          Try using the word "title" to start. 
          '''
    else:
          #@app.route("/questions", methods=['POST'])
          #def search_question():
          #  body = request.get_json()
      try:
        search = body.get('searchTerm', None)
        if search:
            selection = Question.query.filter(Question.question.ilike(f'%{search}%'))\
              .order_by(Question.category).all()
            if len(selection) == 0:
                return jsonify({
                  'success': False,
                  'questions': [],
                })
            else:
                questions = paginate_questions(request, selection)
                return jsonify({
                'success': True,
                'questions':questions,
                })
      except:
        abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<category_id>/questions")
  def get_category(category_id):
    selection = Question.query.filter(Question.category == category_id).order_by(Question.difficulty).all()
    questions = paginate_questions(request, selection)

    if len(questions) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions":questions,
      "total_questions": len(questions),
      "current_category":category_id
      })



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=["POST"])
  def play_quizz():
      
      body = request.get_json()
      try:  
        previous_questions = body['previous_questions']
        quiz_category_id = body['quiz_category']['id']
        # test if the user selects "All"
        if quiz_category_id == 0: 
          questions = Question.query.order_by(Question.id).all()
        else: 
          questions = Question.query.filter(Question.category == quiz_category_id).order_by(Question.id).all()
        
        # need to test questions againt previous_questions
        if len(questions) > len(previous_questions):
          question = questions[len(previous_questions)]
          return jsonify({
            'success': True,
            'question': question.format(),
            'total_questions': len(questions)})
        else:
          return jsonify({
            'success': False,
            'question': None,
          })
        
      except:
        abort(404)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  ''' 
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
      
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

 

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "INTERNAL SERVER ERROR"
      }), 500

  return app

    