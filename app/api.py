from app import db
from app.models import Route, Invoice


def invoice_processing(data):
    id = data.get('id', False)
    invoice = Invoice.query.get(id)

    method = data.get('method', False)
    if method == 'update':
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

        db.session.add(route)
        invoices = data.get('invoices', list())
        for invoice in invoices:
            invoice['method'] = method
            invoice['route_id'] = id
            invoice_processing(invoice)

    elif method == 'delete' and route:
        for invoice in route.invoices:
            invoice.order = 0
            invoice.route_id = None
            db.session.add(invoice)

        db.session.delete(route)

    db.session.commit()
