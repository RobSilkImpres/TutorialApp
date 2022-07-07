from flask import Flask, render_template
from werkzeug.exceptions import abort
from website import create_app

# EB looks for an 'application' callable by default.
application = create_app()
app = application

# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()