from app import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id}: {self.name} on {self.date} at {self.time}>'