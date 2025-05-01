from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models import db, Book
from schemas import BookSchema

book_schema = BookSchema()


class BookListResource(Resource):
    def post(self):
        """
        Add new book
        ---
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Book'
        responses:
          201:
            description: Book created
        """
        try:
            data = book_schema.load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        new_book = Book(**data)
        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201

    def get(self):
        """
        Get all books
        ---
        responses:
          200:
            description: List of books
            schema:
              $ref: '#/definitions/Book'
        """
        books = Book.query.all()
        return book_schema.dump(books, many=True), 200


class BookResource(Resource):
    def get(self, book_id):
        """
        Get book by id
        ---
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          200:
            description: Book
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Book not found
        """
        book = db.get_or_404(Book, book_id)
        return book_schema.dump(book), 200

    def delete(self, book_id):
        """
        Delete book by id
        ---
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          204:
            description: Book deleted
          404:
            description: Book not found
        """
        book = db.get_or_404(Book, book_id)
        db.session.delete(book)
        db.session.commit()
        return {}, 204
