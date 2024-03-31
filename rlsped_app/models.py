from rlsped_app.flask_app import db
from sqlalchemy import Sequence


class Transport(db.Model):
    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)

    client_id = db.Column(db.String(100), unique=False, nullable=False)

    zip_from = db.Column(db.String(50), unique=False, nullable=False)
    location_from = db.Column(db.String(500), unique=False, nullable=False)
    lat_from = db.Column(db.Numeric(precision=25, scale=20), unique=False, nullable=False)
    lon_from = db.Column(db.Numeric(precision=25, scale=20), unique=False, nullable=False)

    zip_to = db.Column(db.String(50), unique=False, nullable=False)
    location_to = db.Column(db.String(500), unique=False, nullable=False)
    lat_to = db.Column(db.Numeric(precision=25, scale=20), unique=False, nullable=False)
    lon_to = db.Column(db.Numeric(precision=25, scale=20), unique=False, nullable=False)

    created_date = db.Column(db.DateTime, unique=False, nullable=False)
