# Демкин Алексей 368096
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
app.app_context().push()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Author = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Books %r>' % self.id


@app.route('/', methods=['POST', 'GET', 'DELETE'])
def index():
    if request.method == "POST":
        Author = request.form['Author']
        Name = request.form['Name']

        book = Books(Author=Author, Name=Name)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/')
        except:
            return "error"
    else:
        return render_template("index.html")


@app.route('/checklist')
def checklist():
    books = Books.query.order_by(Books.Date.desc()).all()
    return render_template("list.html", books=books)


@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Books).delete()
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
