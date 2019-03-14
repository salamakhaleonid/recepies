# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask_login import login_user, logout_user, login_required,current_user


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

@app.context_processor
def inject_user():
    ingridients_number = Ingredient.query.count()
    cousine_number = Cousine.query.count()
    recepies_number = Dish.query.count()
    user_number = User.query.count()
    return dict(ingredients=ingridients_number,cousine=cousine_number,recepies=recepies_number,users=user_number)



@app.route("/base", methods=['GET', 'POST'])
def base():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            # print user
            if password == user.password:
            # if bcrypt.check_password_hash(user.password, password):
                print ("user logged")
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('index'))
            else:
                return redirect(url_for('register'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/")
def index():
    cousine_list = Cousine.query.all()
    return render_template('index.html', cousine_list=cousine_list)

@app.route('/cousine/<int:cousine_id>')
def dishes_in_cousine(cousine_id=None):
    if cousine_id and cousine_id <= Cousine.query.count():
        return render_template('dishes.html', dishes_list=Dish.query.filter_by(cousine_id=cousine_id))
    return redirect('/')

@app.route('/dishes/<int:dish_id>')
def dish_description(dish_id=None):
    # print dish_id
    if dish_id and dish_id <= Dish.query.count():
        dish = Dish.query.get(dish_id)
        # print(dish)
        # print(dish.dish_name)
        print(dish.preparation.decode('unicode'))
        # print dish.preparation.encode('utf-8')
        return render_template('dish.html', dish=dish)
    return redirect('/')


@app.route('/add_dish', methods=['GET', 'POST'])
@login_required
def add_dish():
    return render_template('add_dish.html')

@app.route('/add_cousine', methods=['GET', 'POST'])
@login_required
def add_cousine():
    return render_template('add_cousine.html')



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)



