from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db
import enum

class TransactionStatus(enum.Enum):
    INITIATED = "initiated"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    listing = relationship('Listing')
    
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender = relationship('User', foreign_keys=[sender_id])
    
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver = relationship('User', foreign_keys=[receiver_id])
    
    status = Column(Enum(TransactionStatus), default=TransactionStatus.INITIATED)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'listing_id': self.listing_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'status': self.status.value,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }