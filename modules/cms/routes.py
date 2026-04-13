from flask import request, jsonify
from shared.extensions import db
from . import cms_bp
from .models import CMSPost
from modules.auth.decorators import login_required
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

@cms_bp.route('/posts', methods=['GET'])
def get_posts():
    category = request.args.get('category')
    query = CMSPost.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
        
    posts = query.order_by(CMSPost.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200

@cms_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
        
    slug = slugify(data['title'])
    # Ensure unique slug
    base_slug = slug
    counter = 1
    while CMSPost.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    new_post = CMSPost(
        title=data['title'],
        slug=slug,
        content=data['content'],
        author=data.get('author', 'Yönetici'),
        image_url=data.get('image_url'),
        category=data.get('category', 'Haber'),
        is_published=data.get('is_published', True)
    )
    
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@cms_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = CMSPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200
