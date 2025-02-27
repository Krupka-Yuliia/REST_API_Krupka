from flask import Blueprint, jsonify, abort, request
from typing import Union, Dict
from marshmallow import ValidationError

from .models import Book, books
from .schemas import BookSchema

main = Blueprint("main", __name__)


def make_response(data: Union[Dict, Book], status_code=200):
    return jsonify(data), status_code


def get_book_by_id(book_id: str) -> Union[Book, None]:
    for book in books:
        if book.id == book_id:
            return book


@main.route("/", methods=["GET"])
def index():
    return make_response({"description": "Hello! This is the main page."})


@main.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    try:
        validated_book_data = BookSchema().load(data)
        book = Book(**validated_book_data)
    except ValidationError as e:
        return make_response({'errors': e.messages}, 422)
    books.append(book)
    return make_response(book, 201)


@main.route("/books", methods=["GET"])
def get_books():
    return make_response({"books": books})


@main.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book_by_id(book_id)
    return make_response(book) if book else abort(404, description=f"Book with id {book_id} not found")


@main.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        abort(404, description=f"Book with id {book_id} not found")
    books.remove(book)
    return {}, 204
