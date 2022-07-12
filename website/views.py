from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import date
from .entity import Entity
from .persistance import PersistanceManager
views = Blueprint('views', __name__)

@views.route('/')
def home():
    '''persist = PersistanceManager()
    contacts = persist.runSelectStatement('SELECT * FROM CONTACTS')
    persist.info("Printing out results")
    persist.info(str(contacts))'''
    return render_template('index.html')

@views.route('/addContact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = request.form.get('dob')

        if not firstName :
            flash('First name is required.', category='warning')
        elif not lastName:
            flash('Last name is required.', category='warning')
        #elif dob > date.today():
            #flash('Date of birth must be earlier than the current date.', category='warning')
        else:
            newContact = Entity(firstName=firstName, lastName=lastName)
            newContact.info("Commit started")
            newContact.commit()
            newContact.info("Commit done")
            flash('Contact has been added.', category='success')
            return redirect(url_for('views.home'))

    return render_template('addContact.html')