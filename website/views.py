from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    render_template('index.html')

@views.route('/addContact')
def add_contact():
    render_template('addContact.html')