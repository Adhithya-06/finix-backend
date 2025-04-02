from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = "transaction"  # Ensure this matches the table name used in SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    

