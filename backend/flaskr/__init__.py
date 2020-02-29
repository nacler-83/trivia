#  --------------------------------------------------------------------------#
#  Imports
#  --------------------------------------------------------------------------#

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

#  --------------------------------------------------------------------------#
#  Helpers
#  --------------------------------------------------------------------------#

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    # helper to paginate the questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question for question in selection]
    current_selection = questions[start:end]

    return current_selection


def convert_categories(categories):
    # helper to convert categories to a dictionary
    categories_dictionary = {}
    for category in categories:
        categories_dictionary[category.id] = category.type

    return categories_dictionary

#  --------------------------------------------------------------------------#
#  APP Setup & Routes
#  --------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #  setup CORS
    #  ----------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-All-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    #  ROUTE: get all the categories
    #  ----------------------------------------------------------------
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.all()
        categories_dictionary = convert_categories(categories)

        if (len(categories_dictionary) == 0):
            abort(404)

        result = {
            'success': True,
            'categories': categories_dictionary
        }

        return jsonify(result)

    #  ROUTE: get all the questions including pagination handling
    #  ----------------------------------------------------------------
    @app.route('/questions', methods=['GET'])
    def get_questions():

        selection = list(map(Question.format, Question.query.all()))
        current_selection = paginate_questions(request, selection)
        categories = Category.query.all()
        categories_dictionary = convert_categories(categories)

        if ((len(current_selection) == 0) or (len(categories_dictionary) == 0)):
            abort(404)

        result = {
            'success': True,
            'questions': current_selection,
            'total_questions': len(selection),
            'current_category': '',
            'categories': categories_dictionary
        }

        return jsonify(result)

    #  ROUTE: delete a question using question ID
    #  ----------------------------------------------------------------
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()

            result = {
                'success': True
            }

            return jsonify(result)

        except(Exception):
            abort(404)

    #  ROUTE: post a new question or search questions
    #  ----------------------------------------------------------------
    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()
        search = body.get('searchTerm', None)
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        try:

            if search:

                selection = list(map(Question.format, Question.query.filter(
                            Question.question.ilike('%{}%'.format(search)))))
                current_selection = paginate_questions(request, selection)
                result = {
                    'success': True,
                    'questions': current_selection,
                    'total_questions': len(selection),
                    'current_category': ''
                }

                return jsonify(result)

            else:

                new_question = Question(question=question,
                                        answer=answer,
                                        difficulty=difficulty,
                                        category=category)
                new_question.insert()

                result = {
                    'success': True,
                    'new_question': new_question.id
                }

                return jsonify(result)

        except(Exception):
            abort(422)

    #  ROUTE: get all the questions by category
    #  ----------------------------------------------------------------
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        selection = list(map(Question.format, Question.query.filter(
                    Question.category == category_id).all()))
        current_selection = paginate_questions(request, selection)

        if (len(selection) == 0):
            abort(404)

        result = {
            'success': True,
            'questions': current_selection,
            'total_questions': len(selection)
        }

        return jsonify(result)

    #  ROUTE: post to play the game
    #  ----------------------------------------------------------------
    @app.route('/quizzes', methods=['POST'])
    def play_game():

        body = request.get_json()
        previous = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        category = int(category['id'])

        # if the user selected all categories, query for all questions
        if (category == 0):
            selection = Question.query.all()
        # otherwise get only the quesitons for the given category
        else:
            selection = Question.query.filter(
                        Question.category == category).all()

        # if no results come back in the query, send back result
        if (len(selection) == 0):
            abort(404)

        # get only the questions from selection that are not in previous
        current_selection = [question.format() for question in selection if question.id not in previous]

        try:
            # while there are still questions left
            while len(current_selection) > 0:
                # grab a random question from the current selection
                question = random.choice(current_selection)

                result = {
                    'success': True,
                    'question': question
                }

                return jsonify(result)

            # when there are no questions left
            result = {
                'success': True,
                'question': None
            }

            return jsonify(result)

        except(Exception):
            abort(404)

    #  ERROR: 404 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    #  ERROR: 422 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    #  ERROR: 400 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    #  ERROR: 405 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app
