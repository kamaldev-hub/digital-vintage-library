import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "library.sqlite")}'

db.init_app(app)


@app.route('/')
def home():
    keyword = request.args.get('keyword')
    sort_by = request.args.get('sort_by', 'title')

    if keyword:
        search = f"%{keyword}%"
        books = Book.query.filter(Book.title.like(search)).order_by(Book.title).all()
    else:
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()
        else:
            books = Book.query.order_by(Book.title).all()

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        new_author = Author(name=name, birth_date=birth_date)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        publication_year = int(request.form['publication_year'])
        isbn = request.form['isbn']
        rating = int(request.form['rating'])
        author_id = int(request.form['author_id'])
        new_book = Book(title=title, publication_year=publication_year, isbn=isbn, author_id=author_id, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/author/<int:author_id>')
def author_detail(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)


if __name__ == '__main__':
    app.run(debug=True)
