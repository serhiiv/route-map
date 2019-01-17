from datetime import date, datetime

from flask import render_template, flash, redirect, url_for, request, abort
from app import app, api

from app.models import Route, Invoice
from app.map import get_map


@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    return response


@app.route('/')
@app.route('/index')
def index():
    day = str(date.today())
    return redirect(url_for('map', day=day))


# @app.route('/')
# @app.route('/text')
# def text():
#     invoices = Invoice.query.all()
#     routes = Route.query.all()
#     return render_template('index.html', config=app.config['SECRET_KEY'],
#                            routes=routes, invoices=invoices)


@app.route('/map/<string:day>')
def map(day):
    try:
        check = datetime.strptime(day, '%Y-%m-%d')
    except ValueError:
        abort(404)

    start = datetime.strptime('2019-01-01', '%Y-%m-%d')
    now = datetime.now()

    if start < check < now:
        iframe = get_map(day)
        return render_template('map.html', iframe=iframe)

    else:
        abort(404)


@app.route('/api', methods=['POST'])
def invoice_sync():
    # request must have JSON-data
    if request.is_json:
        data = request.get_json()
        kind = data.get('kind')
        if kind == 'invoice':
            api.invoice_processing(data)
        if kind == 'route':
            api.route_processing(data)
        return "JSON-data processed"
    else:
        return "415 Unsupported Media Type ;)"
