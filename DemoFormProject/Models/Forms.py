#-------------------------------------------------------------------------------
#אימפורטים להרשמה וכניסה

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#אימפורטים אחרים
import pandas as pd
from os import path
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#אימפורטים לפעולה שהופכת מידע לתמונה

import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#אימפורטים למידע שחייבים להכניס

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
            #פקודה המאפשרת לexpand לפעול

class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

            #פקודה המאפשרת לcollapse לפעול

class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
            #פקודה ההופכת את המידע לגרף

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
            #מגדיר את האפשרויות בחירה בקוורי

def get_country_choices(): 
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\Data\\Cscore.csv")) #קורא את הקובץ 
    s = df_short_state.set_index('Country')
    df1 = df_short_state.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))
    return m
#-------------------------------------------------------------------------------


