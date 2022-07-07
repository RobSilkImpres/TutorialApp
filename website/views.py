from flask import Blueprint, render_template, request, flash
from datetime import date

views = Blueprint('views', __name__)

@views.route('/')
def home():
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
        elif dob > date.today():
            flash('Date of birth must be earlier than the current date.', category='warning')
        else:
            #add user to db
            flash('Contact has been added.', category='success')
    return render_template('addContact.html')