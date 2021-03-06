from app import db


class Route(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    invoices = db.relationship('Invoice', backref='route', lazy=True)
    route_datetime = db.Column(db.DateTime)
    car = db.Column(db.Unicode(50))
    car_volume = db.Column(db.Float)
    car_volume_opt = db.Column(db.Float)
    volume = db.Column(db.Float)
    points = db.Column(db.PickleType)
    manadger_waypoint_order = db.Column(db.PickleType)
    manadger_polyline = db.Column(db.PickleType)
    manadger_popup = db.Column(db.Text)
    manadger_distance = db.Column(db.Float)
    google_waypoint_order = db.Column(db.PickleType)
    google_polyline = db.Column(db.PickleType)
    google_popup = db.Column(db.Text)
    google_distance = db.Column(db.Float)

    def invoices_by_order(self):
        out = [''] * len(self.invoices)
        for invoice in self.invoices:
            out[invoice.order - 1] = invoice
        return out

    def __repr__(self):
        return f'<Route: {self.id[:10]} from {self.route_datetime}>'


class Invoice(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    order = db.Column(db.Integer)
    manadger = db.Column(db.Unicode(250))
    invoice_datetime = db.Column(db.DateTime)
    route_datetime = db.Column(db.DateTime)
    client_nickname = db.Column(db.Unicode(32))
    client_name = db.Column(db.Unicode(250))
    volume = db.Column(db.Float, default=0)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    city = db.Column(db.Unicode(40))
    city_lon = db.Column(db.Float)
    city_lat = db.Column(db.Float)
    route_id = db.Column(
        db.String(15), db.ForeignKey('route.id'), nullable=True)

    def __repr__(self):
        return f'<Invoice: {self.id[:10]} from {self.invoice_datetime}>'
