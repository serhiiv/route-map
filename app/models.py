from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Route(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    invoices = db.relationship('Invoice', backref='route', lazy=True)

    def __repr__(self):
        return f'<Route: {self.id}, Invoices: {self.invoices}>'


class Invoice(db.Model):

    id = db.Column(db.String(15), primary_key=True)
    order = db.Column(db.Integer, nullable=True)
    route_id = db.Column(
        db.String(15), db.ForeignKey('route.id'), nullable=True)

    def __repr__(self):
        return f'<Invoice: {self.id}, Order: {self.order}, Route: {self.route_id}>'
