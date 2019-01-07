from flask import render_template, flash, redirect, url_for, request
from app import app, api
from app.models import Route, Invoice


@app.route('/')
@app.route('/index')
def index():
    invoices = Invoice.query.all()
    routes = Route.query.all()
    return render_template('index.html', config=app.config['SECRET_KEY'],
                           routes=routes, invoices=invoices)


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
