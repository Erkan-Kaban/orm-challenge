from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

# creates an instance of flask named app
app = Flask(__name__)

## DB CONNECTION AREA
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://tomato:123@127.0.0.1:5432/ripe_tomatoes_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
#print(db.__dict__) this checks to see if you have configured your config correctly.

# CLI COMMANDS AREA

# Defining a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
  db.create_all()
  print("Tables created")

# @app.cli.command('seed')
# def seed_db():
#   movies = Movies(
#     title = 'Top Gun',
#     genre = 'Action',
#     length = 60,
#     year_released = 

#   )

@app.cli.command('seed')
def seed_db():
  movies = [
    Movie(
      title = 'Top Gun',
      genre = 'Action',
      length = 120,
      year_released = 1986
    ),
    Movie(
      title = 'Entergalactica',
      genre = 'Romance',
      length = 120,
      year_released = 2022
      )
  ]

  actors = [
    Actor(
      first_name = 'Will',
      last_name = 'Smith',
      gender = 'Male',
      country = 'USA',
      dob = date(1968, 9, 25).isoformat()
    ),
    Actor(
      first_name = 'Chris',
      last_name = 'Hemmsworth',
      gender = 'Male',
      country = 'Australia',
      dob = date(1983, 8, 11).isoformat()
      ),
    Actor(
      first_name = 'Samuel',
      last_name = 'Jackson',
      gender = 'Male',
      country = 'USA',
      dob = date(1948, 12, 21).isoformat()
      ),
    Actor(
      first_name = 'Tom',
      last_name = 'Hanks',
      gender = 'Male',
      country = 'USA',
      dob = date(1956, 9, 9).isoformat()
      )
  ]

  db.session.add_all(movies)
  db.session.add_all(actors)
  db.session.commit()
  print('Tables seeded')

@app.cli.command('drop')
def drop_db():
  db.drop_all()
  print("Tables dropped")


# MODELS AREA
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    length = db.Column(db.Integer)
    year_released = db.Column(db.Integer)

class Actor(db.Model):
  __tablename__ = 'actors'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  gender = db.Column(db.String)
  country = db.Column(db.String)
  dob = db.Column(db.Date)

# SCHEMAS AREA
class MovieSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'genre', 'length', 'year_released')
    
class ActorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name', 'last_name', 'gender', 'country', 'dob')


# ROUTING AREA
@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.route("/movies/")
def movies():
  # select * from movies;
  stmt = db.select(Movie)
  movies = db.session.scalars(stmt)
  return MovieSchema(many=True).dump(movies)

@app.route("/actors/")
def actors():
  # select * from movies;
  stmt = db.select(Actor)
  actors = db.session.scalars(stmt)
  return ActorSchema(many=True).dump(actors)

  

