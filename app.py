from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import dynamo

#name = "ciao"

#app = Flask(__name__)

#@app.route("/")
#def pagina():
#    return render_template('index.html', name=name)

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

Bootstrap(app)

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = SearchForm()
    message = ""  # AL POSTO DI MESSAGE PREPARA I DATI PER LA TABELLA -- mettici gli ultimi x post
    if form.validate_on_submit():
        search = form.search.data
        # FAI LA QUERY QUA
        table_contents = dynamo.query_table_by_title(search)
        # empty the form field
        form.search.data = ""

    return render_template('index.html', form=form, message=message, table_contents=table_contents)

app.run(debug=True)