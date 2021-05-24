from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import dynamo

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

Bootstrap(app)

class SearchForm(FlaskForm):
    choices = dynamo.subreddits()
    subreddit = SelectField('Subreddit', choices=choices)
    search = StringField('Search')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        subreddit = form.subreddit.data
        # TODO: fai qualcosa per migliorare la ricerca che non da risultati
        table_contents = dynamo.query_table_by_title(search, subreddit)
        # empty the form field
        form.search.data = ""
    else:
        table_contents = dynamo.default_query()

    return render_template('index.html', form=form, table_contents=table_contents)

app.run(debug=True)