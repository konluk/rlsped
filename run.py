from rlsped_app import flask_app

if __name__ == '__main__':
    flask_app.app.run(debug=True)


"""
import sys

# add your project directory to the sys.path
project_home = r'C:\projects\rlsped\rlsped_app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application  # noqa
"""