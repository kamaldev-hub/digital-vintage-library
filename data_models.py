from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    books = db.relationship('Book', back_populates='author', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Author {self.name}>'


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.String(13), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', back_populates='books')
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Book {self.title}>'
