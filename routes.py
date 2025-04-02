import os
from flask import Blueprint, request, jsonify
from models import db, Transaction

transaction_routes = Blueprint('transaction_routes', __name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):  
    os.makedirs(UPLOAD_FOLDER)

# Home Route
@transaction_routes.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Finix API 🚀'})

# Add a new transaction
@transaction_routes.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging

        if not data or 'date' not in data or 'category' not in data or 'amount' not in data:
            return jsonify({'error': 'Missing required fields', 'received': data}), 400

        new_transaction = Transaction(
            date=data['date'],
            category=data['category'],
            amount=data['amount']
        )
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction added successfully'}), 201

    except Exception as e:
        print(f"❌ ERROR: {e}")  # Debugging
        return jsonify({'error': str(e)}), 500

# Retrieve all transactions
@transaction_routes.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()

    transactions_list = [{
        'id': t.id,
        'date': t.date,
        'category': t.category,
        'amount': t.amount
    } for t in transactions]

    return jsonify(transactions_list), 200

# Delete a transaction
@transaction_routes.route('/delete_transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        db.session.delete(transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction deleted successfully'}), 200

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'error': str(e)}), 500

# Upload bank statement
@transaction_routes.route('/upload_statement', methods=['POST'])
def upload_statement():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file.save(f"uploads/{file.filename}")
    return jsonify({'message': f'File {file.filename} uploaded successfully'}), 200

# Update a transaction
@transaction_routes.route('/update_transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        data = request.get_json()
        transaction.date = data.get('date', transaction.date)
        transaction.category = data.get('category', transaction.category)
        transaction.amount = data.get('amount', transaction.amount)

        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'}), 200

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'error': str(e)}), 500
