from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime, date
from .entity import Entity
from .persistance import PersistanceManager
views = Blueprint('views', __name__)

@views.route('/')
def home():
    contact = Entity.create()
    result = contact.read()
    return render_template('index.html', contacts=result)

@views.route('/addContact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
        arg = {
            "firstName" : firstName,
            "lastName" : lastName,
            "dob" : dob
        }
    
        if not firstName :
            flash('First name is required.', category='warning')
        elif not lastName:
            flash('Last name is required.', category='warning')
        #elif dob > date.today():
            #flash('Date of birth must be earlier than the current date.', category='warning')
        else:
            newContact = Entity.create(arg)
            newContact.info("Commit started")
            newContact.commit()
            newContact.info("Commit done")
            flash('Contact has been added.', category='success')
            return redirect(url_for('views.home'))

    return render_template('addContact.html')

@views.route('/<str:contact_id>')
def post(contact_id):
    this = Entity()
    contact = this.read("id = " + contact_id)
    if contact:
        return render_template('contact.html', contact=contact)
    else:
        flash('Contact ' + contact_id + ' not found.', category='warning')
        return redirect(url_for('views.home'))