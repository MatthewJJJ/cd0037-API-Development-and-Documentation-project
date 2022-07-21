from ast import Break
import os
from unicodedata import category
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

    @app.route('/questions')
    def get_questions():
        cat_results = Category.query.all()
        response_dict = {}
        for element in cat_results:
            new_element = { element.id: element.type }
            response_dict.update(new_element)

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        results = Question.query.all()
        questions = [question.format() for question in results]

        if len(questions[start:end]) == 0:
            abort(404)

        return jsonify({
            'questions': questions[start:end],
            'totalQuestions': len(questions),
            'categories': response_dict,
            'currentCategory': response_dict[questions[start:end].pop()['category']],
            'status': 'success'
        })

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                'removed_question': question.format(),
                'status': 'success'
            })
        except:
            abort(500)

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
            try:
                print("creating new question...")
                new_question = Question(
                    question=data['question'],
                    answer=data['answer'],
                    difficulty=data['difficulty'],
                    category=data['category']
                    )
                new_question.insert()

                return jsonify({
                    'new_question': new_question.format(),
                    'status': 'success'
                })
            except:
                abort(500)

    @app.route('/categories/<int:cat_id>/questions', methods=["GET"])
    def get_questions_by_cat(cat_id):
        category = Category.query.filter_by(id=cat_id).all()

        if len(category) == 0:
            abort(404)

        results = Question.query.filter_by(category=cat_id).all()
        questions = [question.format() for question in results]
            
        return jsonify({
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': category[0].type,
            'status': 'success'
        })

    @app.route('/quizzes', methods=["POST"])
    def get_quizzes():
        data = request.get_json()

        category = Category.query.filter_by(type=data['quiz_category']).all()
        results = Question.query.filter_by(category=category[0].id).filter(Question.id.notin_(data['previous_questions'])).all()

        questions = [question.format() for question in results]

        rand_index = random.randint(0, len(questions) -1)

        return jsonify({
            'question': questions[rand_index],
            'quiz_category': category[0].type,
            'status': 'success'
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'error': 400,
            'message': 'recieved bad request... request not processed...',
            'full_error_message': error
        }), 404

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'error': 404,
            'message': 'endpoint not found'
        }), 404

    @app.errorhandler(422)
    def not_processed(error):
        return jsonify({
            'status': 'error',
            'error': 422,
            'message': 'unprocessable entity detected... entity not processed',
            'full_error_message': error
        }), 404

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'error': 500,
            'message': 'internal server error... request not processed',
            'full_error_message': error
        }), 404

    return app

