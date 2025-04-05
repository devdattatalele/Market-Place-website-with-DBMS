from flask import jsonify, request
from datetime import datetime
from app import db
from models.transaction import Transaction, TransactionStatus
from models.listing import Listing, ListingStatus
from models.user import User

def create_transaction():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['listing_id', 'sender_id', 'receiver_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if listing exists and is available
    listing = Listing.query.get(data['listing_id'])
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    if listing.status != ListingStatus.AVAILABLE:
        return jsonify({'error': 'Listing is not available'}), 400
    
    # Check if users exist
    sender = User.query.get(data['sender_id'])
    receiver = User.query.get(data['receiver_id'])
    if not sender or not receiver:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new transaction
    transaction = Transaction(
        listing_id=data['listing_id'],
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        notes=data.get('notes')
    )
    
    # Update listing status
    listing.status = ListingStatus.PENDING
    
    try:
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify(transaction.to_dict())

def update_transaction_status(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    try:
        new_status = TransactionStatus(data['status'])
    except ValueError:
        return jsonify({'error': 'Invalid transaction status'}), 400
    
    # Update transaction status
    transaction.status = new_status
    
    # Update listing status based on transaction status
    if new_status == TransactionStatus.COMPLETED:
        transaction.completed_at = datetime.utcnow()
        transaction.listing.status = ListingStatus.COMPLETED
    elif new_status == TransactionStatus.CANCELLED:
        transaction.listing.status = ListingStatus.AVAILABLE
    
    try:
        db.session.commit()
        return jsonify(transaction.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_user_transactions(user_id):
    # Get transactions where user is either sender or receiver
    transactions = Transaction.query.filter(
        (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
    ).order_by(Transaction.created_at.desc()).all()
    
    return jsonify([transaction.to_dict() for transaction in transactions])

def get_listing_transactions(listing_id):
    transactions = Transaction.query.filter_by(listing_id=listing_id)\
        .order_by(Transaction.created_at.desc()).all()
    return jsonify([transaction.to_dict() for transaction in transactions])