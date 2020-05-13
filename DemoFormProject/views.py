"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DemoFormProject import app
from DemoFormProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from DemoFormProject.Models.Forms import plot_to_img

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from DemoFormProject.Models.Forms import ExpandForm
from DemoFormProject.Models.Forms import CollapseForm

from DemoFormProject.Models.QueryFormStructure import QueryFormStructure 
from DemoFormProject.Models.QueryFormStructure import LoginFormStructure 
from DemoFormProject.Models.QueryFormStructure import UserRegistrationFormStructure 

from DemoFormProject.Models.Forms import plot_to_img
from DemoFormProject.Models.Forms import get_country_choices

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/data')
def data():

    print("Data")

    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My data page.',
    )

@app.route('/data/countries' , methods = ['GET' , 'POST'])
def countries():

    print("Countries")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/countries.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')

        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
  

    return render_template(
        'countries.html',
        title='Countries',
        year=datetime.now().year,
        message='Countries dataset page.',
        img_countries = '/static/pics/countries.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/Query', methods=['GET', 'POST'])
def Query():
        
        form = QueryFormStructure(request.form) #פקודה האומרת לתוכנה לקבל מהמשתמש נתונים
        chart = '' #מגדיר טבלה ריקה

        df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/Cscore.csv')) # קורא את הקובץ עם הציון
        form.Countries.choices = get_country_choices() #מגדיר לתוכנה אפשרויות למשתנים
        country_list = form.Countries.data #נותן את הרשימה למשתמש

        
        if (request.method == 'POST'):
            df = df[['Country', 'Score']] #מוריד את כל שאר העמודות
            #df = df.set_index('Country') #נותן אינדקס לעמודה

            for country in country_list:
                Countries = form.Countries.data
                df2 = df[df['Country'].isin (Countries)]
                df2 = df2.set_index('Country')
                #df[country] = df2['Score']


            #יוצר גרף
            fig = plt.figure()
            ax = fig.add_subplot(111)
            df2.plot(ax = ax , kind = 'bar')
            chart = plot_to_img(fig)


        
        #מחזיר למשתמש גרף
        return render_template(
        'query.html', 
         form = form,
         chart = chart,
         title='Query by the user',
         year=datetime.now().year,
         message='This page will use the web forms to get user input'
                    )

         
# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thank you for registering new user - '+ form.FirstName.data + " " + form.LastName.data )

        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )



@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\capitals.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        title='This is Data Set 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


