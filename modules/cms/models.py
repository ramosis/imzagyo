from shared.extensions import db
from datetime import datetime

class CMSPost(db.Model):
    """Global News and Blog content management system."""
    __tablename__ = 'cms_posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='Haber') # Haber, Blog, Duyuru
    is_published = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'author': self.author,
            'image_url': self.image_url,
            'category': self.category,
            'is_published': self.is_published,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
