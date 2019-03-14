# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import csv
# from flask_bcrypt import Bcrypt


app = Flask(__name__,static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "super secret key"

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return  self.username

class Cousine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cousine_name = db.Column(db.Text, unique=True, nullable=False)
    image_id = db.Column(db.Integer)

    def __repr__(self):
        return  self.cousine_name

ingredients = db.Table('ingredients',
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.Text, nullable=False)
    preparation = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.Integer)
    cousine_id = db.Column(db.Integer, db.ForeignKey('cousine.id'), nullable=False)
    cousine = db.relationship('Cousine', backref=db.backref('dishes', lazy=True))
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
                                  backref=db.backref('dishes', lazy=True))

    def __repr__(self):
        return  self.dish_name


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.ingredient_name

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()




def create_db():
    db.create_all()
    me = User(username='admin', password='pass', email='admin@example.com')
    db.session.add(me)
    # french_cousine = Cousine(cousine_name="French cousine",image_id=0)
    # db.session.add(french_cousine)
    with open('ingedients.csv',encoding='utf-8') as sourse:
        reader = csv.DictReader(sourse)
        for ingredient in reader:
            ingredient = dict(ingredient)
            ingredient['ingredientName'] = ingredient['ingredientName']#.encode('utf-8')
            print(ingredient['ingredientName'])
            ingredient1 = Ingredient(id=int(ingredient['idIngredient']),
                                     ingredient_name=ingredient['ingredientName'])
            db.session.add(ingredient1)
    db.session.commit()
    with open('dishes.csv',encoding='utf-8') as sourse:
        reader = csv.DictReader(sourse)

        for dish in reader:
            dish = dict(dish)
            dish['dishName'] = (dish['dishName'])#.encode('utf-8')
            dish['Preparation'] = (dish['Preparation'])#.encode('utf-8')
            # print dish['Preparation']
            dish1 = Dish(id=int(dish['idDish']), dish_name=dish['dishName'], preparation=dish['Preparation'],
                            image_id=dish['idImage'], cousine_id=dish['IdCousine'])
            for element in dish['Ingredients'].split(" "):
                ing = Ingredient.query.filter_by(id=int(element)).one()
                # print ing.ingredient_name
                dish1.ingredients.append(ing)
            # print dish1.dish_name
            db.session.add(dish1)
    db.session.commit()
    with open('cousine.csv',encoding='utf-8') as sourse:
        reader = csv.DictReader(sourse)
        for cousine in reader:
            cousine = dict(cousine)
            cousine['cousineName'] = cousine['cousineName']#.encode('utf-8')
            cousine1 = Cousine(id=int(cousine['id']),
                                     cousine_name=cousine['cousineName'],image_id=cousine['idImage'])
            db.session.add(cousine1)
    db.session.commit()
    print (me.email)
    for ing in Ingredient.query.all():
        for element in ing.dishes:
            print (element.dish_name)
    for dish in Dish.query.all():
        print(dish)
        print("Strava: "+dish.dish_name)
        print(dish.preparation)
        for element in dish.ingredients:
            print (element.ingredient_name)

if __name__ == '__main__':
    create_db()