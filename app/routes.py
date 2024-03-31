from flask import render_template, request, jsonify
from app import app, db
from flask import session, redirect
from functools import wraps

from app.config import app_config
from app.geo_tools import GeoTools
from .models import Transport

import datetime

geo = GeoTools()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        print(session)
        if 'user' not in session:
            print("not logged, redirect")
            return redirect("login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return redirect("transports")


@app.route('/transports')
@login_required
def transports():
    return render_template('transports.html')


@app.route('/findClient')
@login_required
def find_client():
    return render_template('findClient.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        if user_name == app_config.USERNAME and password == app_config.PASSWORD:
            session['user'] = user_name
            return redirect("transports")
        else:
            return jsonify({'error': "Invalid username or password"}), 401
    return render_template('login.html')


@app.route('/api/addTransport', methods=['POST'])
def add_transport():
    try:
        client_id = request.form.get('client_id')
        zip_from = request.form.get('zip_from')
        zip_to = request.form.get('zip_to')

        lat_from, lon_from, location_from = geo.get_location_info(zip_from)
        lat_to, lon_to, location_to = geo.get_location_info(zip_to)

        created_date = datetime.datetime.now()

        new_transport = Transport(
            client_id=client_id,
            zip_from=zip_from,
            location_from=location_from,
            lat_from=lat_from,
            lon_from=lon_from,
            zip_to=zip_to,
            location_to=location_to,
            lat_to=lat_to,
            lon_to=lon_to,
            created_date=created_date
        )

        db.session.add(new_transport)
        db.session.commit()

        return jsonify({'message': 'Transport created successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/getTransports', methods=['GET'])
def get_transports():
    db_transports = Transport.query.order_by(Transport.id.desc()).all()
    transport_list = []
    for transport in db_transports:
        info_from = f'<b>{transport.zip_from.replace(" ", "")}</b>- {transport.location_from} ({str(int(transport.lat_from))}, {str(int(transport.lon_from))})'
        info_to = f'<b>{transport.zip_to.replace(" ", "")}</b>- {transport.location_to} ({str(int(transport.lat_to))}, {str(int(transport.lon_to))})'
        transport_dict = {
            'id': transport.id,
            'client_id': transport.client_id,
            'info_from': info_from,
            'info_to': info_to,
            'created_date': transport.created_date.strftime('%d.%m.%Y %H:%M:%S')
        }
        transport_list.append(transport_dict)
    return jsonify(transport_list)


# Define the route for the delete API
@app.route('/api/deleteTransport', methods=['POST'])
def delete_transport():
    transport_id = request.form.get('transport_id')
    transport = Transport.query.get(transport_id)
    if transport:
        db.session.delete(transport)
        db.session.commit()
        return jsonify({'message': 'Transport deleted successfully'}), 200
    else:
        return jsonify({'error': 'Transport not found'}), 404


@app.route('/api/findClients', methods=['POST'])
def find_clients():
    search_zip = request.form.get('searchzip')
    lat_search, lon_search, location_search = geo.get_location_info(search_zip)

    db_transports = Transport.query.all()
    clients = []

    for transport in db_transports:
        distance_between_zip = geo.haversine(lat_search, lon_search, transport.lat_from, transport.lon_from)
        info_from = f'<b>{transport.zip_from.replace(" ", "")}</b>- {transport.location_from} ({str(int(transport.lat_from))}, {str(int(transport.lon_from))})'
        info_to = f'<b>{transport.zip_to.replace(" ", "")}</b>- {transport.location_to} ({str(int(transport.lat_to))}, {str(int(transport.lon_to))})'

        transport_dict = {
            'distance': int(distance_between_zip),
            'client_id': transport.client_id,
            'info_from': info_from,
            'info_to': info_to,
        }
        clients.append(transport_dict)

    clients = sorted(clients, key=lambda x: x['distance'])

    return jsonify({"location_search":location_search, "clients":clients})