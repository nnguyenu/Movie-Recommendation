# Movie-Recommendation

INTRODUCTION
------------

This is my Christmas project. You will put your own rating of some movies (from 0 to 5) and after 6 movies, you can get recommendation about similar movies. To find similar movies, I use [Collaboraive filtering](https://en.wikipedia.org/wiki/Collaborative_filtering) and [KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm). 

The dataset is [MovieLens 100K Dataset](https://grouplens.org/datasets/movielens/100k/) so you can only rate movies before 1998 :(

To use this project, you need to install
+ [Flask SQL-Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
+ [Pandas](https://pandas.pydata.org/)
+ [Scikit-learn](https://scikit-learn.org/stable/)
```
pip3 install virtual env
virtual env
source env/bin/activate
pip3 install flask flask-alchemy
pip3 install pandas
pip3 install scikit-learn
```
Add database:
```
python3
>>> from app import app, db
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```