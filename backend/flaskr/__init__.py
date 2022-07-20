import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        return "Hello from the Udacity quiz question API!"

    @app.route('/categories')
    def get_categories():
        results = Category.query.all()
        response_dict = {}
        for element in results:
            new_element = { element.id: element.type }
            response_dict.update(new_element)
    
        return jsonify({
            'categories': response_dict,
            'status': 'success'
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        results = Question.query.all()
        questions = [question.format() for question in results]

        return jsonify({
            'questions': questions[start:end],
            'totalQuestions': len(questions),
            'categories': '',
            'currentCategory': '',
            'status': 'success'
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()

        return jsonify({
            'status': 'success'
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=["POST"])
    def search_questions():
        data = request.get_json()

        if 'searchTerm' in data.keys():
            print("searching questions...")
            results = Question.query.filter(Question.question.like("%"+data['searchTerm']+"%")).all()
            questions = [question.format() for question in results]

            return jsonify({
                'questions': questions,
                'totalQuestions': len(questions),
                'currentCategory': '',
                'status': 'success'
            })
        else:
            print("creating new question...")
            new_question = Question(
                question=data['question'],
                answer=data['answer'],
                difficulty=data['difficulty'],
                category=data['category']
                )
            new_question.insert()

            return jsonify({
                'status': 'success'
            })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:cat_id>/questions', methods=["GET"])
    def get_questions_by_cat(cat_id):
        category = Category.query.filter_by(id=cat_id).all()

        results = Question.query.filter_by(category=cat_id).all()
        questions = [question.format() for question in results]
        
        return jsonify({
            'questions': questions,
            'totalQuestions': '',
            'currentCategory': category[0].type,
            'status': 'success'
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=["POST"])
    def get_quizzes():
        return jsonify({
            'status': 'success'
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

