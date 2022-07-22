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
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:2717@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

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

    delete_id = ''
    
    def test_cat_endpoints(self):
        get_cat_res = self.client().get('/categories')
        get_cat_res = json.loads(get_cat_res.data)

        expected_cat_dictionary = {"1":"Science","2":"Art","3":"Geography","4": "History","5": "Entertainment","6":"Sports"}
        
        self.assertEqual(str(get_cat_res['categories']), str(expected_cat_dictionary))
        self.assertEqual(get_cat_res['status'], 'success')

    def test_cat_endpoint_attempted_search_failure_404_error(self):
        get_cat_res = self.client().get('/categories:Science')
        get_cat_res = json.loads(get_cat_res.data)

        self.assertEqual(get_cat_res['error'], 404)
        self.assertEqual(get_cat_res['message'], 'endpoint not found')
        self.assertEqual(get_cat_res['status'], 'error')

    def test_get_questions(self):
        get_questions_res = self.client().get('/questions?page=1')
        get_questions_res = json.loads(get_questions_res.data)

        self.assertEqual(get_questions_res['totalQuestions'], 19)
        self.assertEqual(len(get_questions_res['questions']), 10)
        self.assertEqual(get_questions_res['status'], 'success')

    def test_get_questions_404_error(self):
        get_questions_res = self.client().get('/questions?page=5000')
        get_questions_res = json.loads(get_questions_res.data)

        self.assertEqual(get_questions_res['error'], 404)
        self.assertEqual(get_questions_res['message'], 'endpoint not found')
        self.assertEqual(get_questions_res['status'], 'error')

    def test_get_questions_by_cat(self):
        get_questions_by_cat_res = self.client().get('/categories/1/questions')
        get_questions_by_cat_res = json.loads(get_questions_by_cat_res.data)

        self.assertEqual(get_questions_by_cat_res['totalQuestions'], 3)
        self.assertEqual(len(get_questions_by_cat_res['questions']), 3)
        self.assertEqual(get_questions_by_cat_res['status'], 'success')
        self.assertEqual(get_questions_by_cat_res['currentCategory'], 'Science')

    def test_get_questions_by_cat_404_error(self):
        get_questions_by_cat_res = self.client().get('/categories/2500/questions')
        get_questions_by_cat_res = json.loads(get_questions_by_cat_res.data)

        self.assertEqual(get_questions_by_cat_res['error'], 404)
        self.assertEqual(get_questions_by_cat_res['message'], 'endpoint not found')
        self.assertEqual(get_questions_by_cat_res['status'], 'error')

    def test_add_and_delete_question(self):
        new_question = Question(question='test_question',answer='answer',difficulty='3',category=1)
        post_question_res = self.client().post('/questions', json=new_question.format())
        post_question_res = json.loads(post_question_res.data)

        get_questions_res = self.client().get('/questions?page=1')
        get_questions_res = json.loads(get_questions_res.data)

        self.assertEqual(get_questions_res['totalQuestions'], 20)
        self.assertEqual(post_question_res['status'], 'success')

        delete_question_res = self.client().delete(f"/questions/{post_question_res['new_question']['id']}")
        delete_question_res = json.loads(delete_question_res.data)

        get_questions_res = self.client().get('/questions?page=1')
        get_questions_res = json.loads(get_questions_res.data)

        self.assertEqual(get_questions_res['totalQuestions'], 19)
        self.assertEqual(delete_question_res['status'], 'success')

    def test_add_question_400_error(self):
        post_question_res = self.client().post('/questions', json={})
        post_question_res = json.loads(post_question_res.data)

        self.assertEqual(post_question_res['error'], 400)
        self.assertEqual(post_question_res['message'], 'recieved bad request... request not processed...')
        self.assertEqual(post_question_res['status'], 'error')

    def test_delete_question_500_error(self):
        delete_question_res = self.client().delete(f"/questions/2500")
        delete_question_res = json.loads(delete_question_res.data)

        self.assertEqual(delete_question_res['error'], 500)
        self.assertEqual(delete_question_res['message'], 'internal server error... request not processed')
        self.assertEqual(delete_question_res['status'], 'error')

    def test_run_quiz(self):
        run_quiz_res = self.client().post('/quizzes', json={"previous_questions": [4],"quiz_category": "Entertainment"})
        run_quiz_res = json.loads(run_quiz_res.data)
        
        self.assertEqual(run_quiz_res['status'], 'success')
        self.assertEqual(run_quiz_res['quiz_category'], 'Entertainment')

    def test_run_quiz_422_error(self):
        run_quiz_res = self.client().post('/quizzes', json={"previous_questions": [4],"quiz_category": "Nothing"})
        run_quiz_res = json.loads(run_quiz_res.data)
        
        self.assertEqual(run_quiz_res['error'], 422)
        self.assertEqual(run_quiz_res['message'], 'unprocessable entity detected... entity not processed')
        self.assertEqual(run_quiz_res['status'], 'error')

    def test_search_questions(self):
        search_question_res = self.client().post('/questions', json={"searchTerm":"1996"})
        search_question_res = json.loads(search_question_res.data)

        self.assertEqual(search_question_res['totalQuestions'], 1)

    def test_search_questions_400_error(self):
        search_question_res = self.client().post('/questions', json={"searchTermi":"1996"})
        search_question_res = json.loads(search_question_res.data)

        self.assertEqual(search_question_res['error'], 400)
        self.assertEqual(search_question_res['message'], 'recieved bad request... request not processed...')
        self.assertEqual(search_question_res['status'], 'error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()