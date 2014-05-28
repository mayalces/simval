import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# initialization
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    DEBUG = True,
)

# controllers
@app.route("/")
def index():
	error = None
	return render_template('index.html', error=error)


# launch
if __name__ == "__main__":
    app.run()
