from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db
import enum

class ListingType(enum.Enum):
    ITEM = "item"
    SERVICE = "service"

class ListingStatus(enum.Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Listing(db.Model):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(ListingType), nullable=False)
    category = Column(String(50), nullable=False)
    condition = Column(String(50))  # For items
    estimated_value = Column(Float)
    is_free = Column(Boolean, default=False)
    willing_to_trade = Column(Boolean, default=True)
    trade_preferences = Column(Text)
    location = Column(String(100), nullable=False)
    status = Column(Enum(ListingStatus), default=ListingStatus.AVAILABLE)
    
    # Image paths stored as comma-separated string
    images = Column(String(500))
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='listings')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type.value,
            'category': self.category,
            'condition': self.condition,
            'estimated_value': self.estimated_value,
            'is_free': self.is_free,
            'willing_to_trade': self.willing_to_trade,
            'trade_preferences': self.trade_preferences,
            'location': self.location,
            'status': self.status.value,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'user_id': self.user_id,
            'images': self.images
        }
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type.value,
            'category': self.category,
            'condition': self.condition,
            'estimated_value': self.estimated_value,
            'is_free': self.is_free,
            'willing_to_trade': self.willing_to_trade,
            'trade_preferences': self.trade_preferences,
            'location': self.location,
            'status': self.status.value,
            'images': self.images.split(',') if self.images else [],
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }