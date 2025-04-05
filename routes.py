from flask import Blueprint
from controllers.user_controller import create_user, get_user, update_user, delete_user, get_user_listings
from controllers.listing_controller import create_listing, get_listing, update_listing, delete_listing, get_listings
from controllers.transaction_controller import create_transaction, get_transaction, update_transaction_status, get_user_transactions, get_listing_transactions

def init_routes(app):
    # User routes
    app.add_url_rule('/api/users', view_func=create_user, methods=['POST'])
    app.add_url_rule('/api/users/<int:user_id>', view_func=get_user, methods=['GET'])
    app.add_url_rule('/api/users/<int:user_id>', view_func=update_user, methods=['PUT'])
    app.add_url_rule('/api/users/<int:user_id>', view_func=delete_user, methods=['DELETE'])
    app.add_url_rule('/api/users/<int:user_id>/listings', view_func=get_user_listings, methods=['GET'])
    
    # Listing routes
    app.add_url_rule('/api/listings', view_func=create_listing, methods=['POST'])
    app.add_url_rule('/api/listings', view_func=get_listings, methods=['GET'])
    app.add_url_rule('/api/listings/<int:listing_id>', view_func=get_listing, methods=['GET'])
    app.add_url_rule('/api/listings/<int:listing_id>', view_func=update_listing, methods=['PUT'])
    app.add_url_rule('/api/listings/<int:listing_id>', view_func=delete_listing, methods=['DELETE'])
    
    # Transaction routes
    app.add_url_rule('/api/transactions', view_func=create_transaction, methods=['POST'])
    app.add_url_rule('/api/transactions/<int:transaction_id>', view_func=get_transaction, methods=['GET'])
    app.add_url_rule('/api/transactions/<int:transaction_id>/status', view_func=update_transaction_status, methods=['PUT'])
    app.add_url_rule('/api/users/<int:user_id>/transactions', view_func=get_user_transactions, methods=['GET'])
    app.add_url_rule('/api/listings/<int:listing_id>/transactions', view_func=get_listing_transactions, methods=['GET'])