from flask import jsonify, request
from app import db
from models.listing import Listing, ListingType, ListingStatus
from models.user import User
import os
import time
from werkzeug.utils import secure_filename

def create_listing():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Validate required fields
    required_fields = ['title', 'description', 'type', 'category', 'location', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Handle image upload
    image_paths = []
    if 'images' in request.files:
        images = request.files.getlist('images')
        for image in images:
            if image and image.filename:
                # Create a secure filename
                filename = secure_filename(image.filename)
                # Create a unique filename with timestamp
                unique_filename = f"{int(time.time())}_{filename}"
                # Save path
                save_path = os.path.join('static/uploads', unique_filename)
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                # Save the file
                image.save(save_path)
                # Add to image paths
                image_paths.append(f"/{save_path}")
    
    # Create new listing
    listing = Listing(
        title=data['title'],
        description=data['description'],
        type=ListingType(data['type']),
        category=data['category'],
        condition=data.get('condition'),
        estimated_value=float(data['estimated_value']) if data.get('estimated_value') else None,
        is_free=bool(data.get('is_free')),
        willing_to_trade=bool(data.get('willing_to_trade')),
        trade_preferences=data.get('trade_preferences'),
        location=data['location'],
        user_id=int(data['user_id']),
        images=','.join(image_paths) if image_paths else None
    )
    
    try:
        db.session.add(listing)
        db.session.commit()
        return jsonify(listing.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    listing_data = listing.to_dict()
    # Add user information to the response
    listing_data['user'] = {
        'username': listing.user.username,
        'location': listing.user.location,
        'id': listing.user.id
    }
    return jsonify(listing_data)

def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        listing.title = data['title']
    if 'description' in data:
        listing.description = data['description']
    if 'category' in data:
        listing.category = data['category']
    if 'condition' in data:
        listing.condition = data['condition']
    if 'estimated_value' in data:
        listing.estimated_value = data['estimated_value']
    if 'is_free' in data:
        listing.is_free = data['is_free']
    if 'willing_to_trade' in data:
        listing.willing_to_trade = data['willing_to_trade']
    if 'trade_preferences' in data:
        listing.trade_preferences = data['trade_preferences']
    if 'location' in data:
        listing.location = data['location']
    if 'status' in data:
        try:
            listing.status = ListingStatus(data['status'])
        except ValueError:
            return jsonify({'error': 'Invalid listing status'}), 400
    if 'images' in data:
        listing.images = ','.join(data['images'])
    
    try:
        db.session.commit()
        return jsonify(listing.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    try:
        # Delete associated images if they exist
        if listing.images:
            image_paths = listing.images.split(',')
            for path in image_paths:
                if path and os.path.exists(path.lstrip('/')):
                    os.remove(path.lstrip('/'))
        
        db.session.delete(listing)
        db.session.commit()
        return jsonify({"message": "Listing deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_listings():
    # Get query parameters for filtering
    category = request.args.get('category')
    listing_type = request.args.get('type')
    location = request.args.get('location')
    is_free = request.args.get('is_free', type=bool)
    
    # Build query
    query = Listing.query
    
    if category:
        query = query.filter_by(category=category)
    if listing_type:
        try:
            query = query.filter_by(type=ListingType(listing_type))
        except ValueError:
            return jsonify({'error': 'Invalid listing type'}), 400
    if location:
        query = query.filter_by(location=location)
    if is_free is not None:
        query = query.filter_by(is_free=is_free)
    
    # Order by most recent
    query = query.order_by(Listing.created_at.desc())
    
    listings = query.all()
    return jsonify([listing.to_dict() for listing in listings])