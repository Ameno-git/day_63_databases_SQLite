from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

all_books = []


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(80), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


db.create_all()



@app.route('/')
def home():
    all_books = Library.query.all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Library(title=request.form["book_name"], author = request.form["book_author"], rating= request.form["book_rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit", methods = ["GET","POST"])
def edit():
    book_id = request.args.get('id')
    if request.method == "POST":
        new_rating=request.form["new_rating"]
        book=Library.query.get(book_id)
        book.rating=new_rating
        db.session.commit()
        return redirect(url_for("home"))
    book_to_edit=Library.query.get(book_id)
    return render_template("edit_rating.html",book=book_to_edit)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book=Library.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)



