from flask import render_template, flash, redirect, url_for, request

from app import app, db
from app.models import Route, Invoice
from app import api

from app.form import LoginForm


@app.route('/')
@app.route('/index')
def index():
    invoices = Invoice.query.all()
    routes = Route.query.all()
    return render_template('index.html', config=app.config['SECRET_KEY'],
                           routes=routes, invoices=invoices)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
