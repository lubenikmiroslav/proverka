from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from models import db, Person
from wtforms import SelectField, FloatField, SubmitField, IntegerField, StringField
import os

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db.init_app(app)

# WTForm for adding a new person
class PersonForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    vyska = FloatField('Vyska (m)', validators=[DataRequired(), NumberRange(min=0, max=2.99, message="Vyska must be a valid number up to 2.99")])
    vaha = FloatField('Vaha (kg)', validators=[DataRequired(), NumberRange(min=0, max=199, message="Vaha must be a valid number up to 199")])
    submit = SubmitField('Add Person')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()
    if not Person.query.first():
        db.session.add_all([
            Person(name='Bertik', vyska=1.65, vaha=55),
            Person(name='Pepicek', vyska=1.80, vaha=75),
            Person(name='Anicka', vyska=1.75, vaha=85)
        ])
        db.session.commit()

@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    form.name.choices = [(person.name, person.name) for person in Person.query.all()]
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, vyska=form.vyska.data, vaha=form.vaha.data, id=form.id.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

    # Create the database file if it doesn't exist

    db_path = '/home/student/sitee/ukolSite/site.db'
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            if not Person.query.first():
                db.session.add_all([
                    Person(name='Bertik', vyska=1.65, vaha=55),
                    Person(name='Pepicek', vyska=1.80, vaha=75),
                    Person(name='Anicka', vyska=1.75, vaha=85)
                ])
                db.session.commit()