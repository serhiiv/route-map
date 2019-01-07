from app import db
from app.models import Route, Invoice
from datetime import datetime


def invoice_processing(data):
    id = data.get('id', False)
    invoice = Invoice.query.get(id)

    method = data.get('method', False)
    if method == 'update':
        if not invoice:
            invoice = Invoice(id=id)
            invoice.order = 0
            invoice.route_id = None
            
        invoice.date = datetime.strptime(data.get('date'), '%d.%m.%Y')
        invoice.client_nickname = data.get('client_nickname')
        invoice.client_name = data.get('client_name')
        invoice.volume = data.get('volume')
        invoice.lon = data.get('lon')
        invoice.lat = data.get('lat')
        invoice.city = data.get('city')
        invoice.city_lon = data.get('city_lon')
        invoice.city_lat = data.get('city_lat')
        db.session.add(invoice)

    elif method == 'route':
        if not invoice:
            invoice = Invoice(id=id)

        invoice.order = data.get('order', 0)
        invoice.route_id = data.get('route_id', None)
        db.session.add(invoice)

    elif method == 'delete' and invoice:
        db.session.delete(invoice)

    db.session.commit()


def route_processing(data):
    id = data.get('id', False)
    route = Route.query.get(id)

    method = data.get('method', False)
    if method == 'update':
        if not route:
            route = Route(id=id)

        route.date = datetime.strptime(data.get('date'), '%d.%m.%Y')
        route.car = data.get('car')
        route.car_volume = data.get('car_volume')
        db.session.add(route)

        invoices = data.get('invoices', list())
        for invoice in invoices:
            invoice['method'] = 'route'
            invoice['route_id'] = id
            invoice_processing(invoice)

    elif method == 'delete' and route:
        for invoice in route.invoices:
            invoice.order = 0
            invoice.route_id = None
            db.session.add(invoice)

        db.session.delete(route)

    db.session.commit()
