from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import extract
import model


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

with app.app_context():
    db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    imdb_link = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    rate = db.Column(db.Integer, nullable=True)
    release_date = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_content,url,release_date,movie_id = extract.read_items(request.form['content'])
        movie_rate = request.form['rate']
        if movie_content == "No movie found" or movie_rate == None or movie_rate < 0 or movie_rate > 5:
            return redirect('/')
        new_movie = Movie(content=movie_content,rate=movie_rate,imdb_link=url,release_date=release_date,movie_id=movie_id)
        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        movies_list = Movie.query.order_by(Movie.date_created).all()
        return render_template('index.html',movies_list = movies_list)

@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = Movie.query.get_or_404(id)
    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that movie'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Movie.query.get_or_404(id)
    if request.method == 'POST':
        movie_content,url,release_date,movie_id = extract.read_items(request.form['content'])
        movie_rate = request.form['rate']
        if movie_content == "No movie found" or movie_rate == None:
            return redirect('/update/<int:id>')
        else:
            movie.content = movie_content
            movie.rate = movie_rate
            movie.imdb_link = url
            movie.release_date = release_date
            movie.movie_id = movie_id
            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue updating your movie'
    else:
        return render_template('update.html', movie=movie)

@app.route('/analyze')
def analyze():
    movies_list = Movie.query.order_by(Movie.date_created).all()
    movie_id_list = [_.movie_id for _ in movies_list]
    movie_rate_list = [_.rate for _ in movies_list]

    rec_movie_id = model.predict(movie_id_list,movie_rate_list)
    rec_movie_list = []
    for i in rec_movie_id:
        movie_content,url,release_date,movie_id = extract.read_items_id(i)
        new_movie = Movie(content=movie_content,imdb_link=url,release_date=release_date,movie_id=movie_id)
        rec_movie_list.append(new_movie)
    return render_template('analyze.html', movies_list = movies_list, rec_movie_list = rec_movie_list)
if __name__ == '__main__':
    app.run(debug=True)