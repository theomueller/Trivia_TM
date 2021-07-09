import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "triviadb_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the answer of all questions ?',
            'answer': '42',
            'category': '1',
            'difficulty': '5'}       

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual((data['current_categorie']),0)
        self.assertTrue((data['categories']))
        self.assertTrue(len(data['categories']))

    ## added test_get_paginated_questions failure scenario
    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_404_send_get_categories_with_wrongID(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
        
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        pass

    def test_400_create_bad_question(self):
        res = self.client().post('/questions', json={"answer":"toto"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_question(self):
        questionFirst = Question.query.first()
        strDel="/questions/{}"
        res = self.client().delete(strDel.format(questionFirst.id))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    
    def test_422_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1000).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)

    def test_400_post_bad_search_question(self):
        res = self.client().post('/questions', json={'search':'the'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') 


############ Quizzes 
    def test_405_quizzes(self):
        res = self.client().get('/quizzes')
        self.assertEqual(res.status_code, 405)

    def test_get_next_question_quizzes(self):
        res = self.client().post('quizzes',json={'previous_questions':"", "quiz_category":{"id":"1"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_wrong_next_question_quizzes(self):
        res = self.client().post('quizzes',json={"quiz_category":"1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found") 

        ############ Added after review:
        '''
        test_get_paginated_questions failure scenario : done
        test_create_new_question failure scenario: done
        test_get_next_question_quizzes failure scenario: dome
        test_422_delete_book success scenario: done
        test_400_post_bad_search_question success scenario : done
        test_405_quizzes success scenario: done '''



    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()