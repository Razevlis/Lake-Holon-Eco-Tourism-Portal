from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from database import db
from app.main import bp
from app.models import Activity, Guide, Trail, Accommodation, Booking, Review, VisitorAnalytics
from datetime import datetime, date
import json

@bp.route('/')
def index():
    # Get featured activities
    featured_activities = Activity.query.filter_by(is_active=True).limit(6).all()
    
    # Get popular trails
    popular_trails = Trail.query.filter_by(is_active=True).limit(4).all()
    
    # Get available guides
    available_guides = Guide.query.filter_by(is_available=True).limit(4).all()
    
    # Track visitor analytics
    today = date.today()
    analytics = VisitorAnalytics.query.filter_by(date=today).first()
    if analytics:
        analytics.page_views += 1
    else:
        analytics = VisitorAnalytics(date=today, page_views=1)
        db.session.add(analytics)
    db.session.commit()
    
    return render_template('main/index.html', 
                         featured_activities=featured_activities,
                         popular_trails=popular_trails,
                         available_guides=available_guides)

@bp.route('/activities')
def activities():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    
    query = Activity.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    activities = query.paginate(
        page=page, per_page=9, error_out=False
    )
    
    categories = db.session.query(Activity.category).distinct().all()
    difficulties = ['easy', 'moderate', 'hard']
    
    return render_template('main/activities.html', 
                         activities=activities,
                         categories=categories,
                         difficulties=difficulties,
                         current_category=category,
                         current_difficulty=difficulty)

@bp.route('/activity/<int:id>')
def activity_detail(id):
    activity = Activity.query.get_or_404(id)
    reviews = Review.query.filter_by(activity_id=id).order_by(Review.created_at.desc()).limit(10).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    return render_template('main/activity_detail.html', 
                         activity=activity, 
                         reviews=reviews,
                         avg_rating=avg_rating)

@bp.route('/trails')
def trails():
    page = request.args.get('page', 1, type=int)
    difficulty = request.args.get('difficulty', '')
    
    query = Trail.query.filter_by(is_active=True)
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    trails = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    difficulties = ['easy', 'moderate', 'hard']
    
    return render_template('main/trails.html', 
                         trails=trails,
                         difficulties=difficulties,
                         current_difficulty=difficulty)

@bp.route('/trail/<int:id>')
def trail_detail(id):
    trail = Trail.query.get_or_404(id)
    return render_template('main/trail_detail.html', trail=trail)

@bp.route('/guides')
def guides():
    page = request.args.get('page', 1, type=int)
    specialization = request.args.get('specialization', '')
    
    query = Guide.query.filter_by(is_available=True)
    
    if specialization:
        query = query.filter(Guide.specialization.ilike(f'%{specialization}%'))
    
    guides = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    specializations = db.session.query(Guide.specialization).distinct().all()
    
    return render_template('main/guides.html', 
                         guides=guides,
                         specializations=specializations,
                         current_specialization=specialization)

@bp.route('/guide/<int:id>')
def guide_detail(id):
    guide = Guide.query.get_or_404(id)
    return render_template('main/guide_detail.html', guide=guide)

@bp.route('/accommodations')
def accommodations():
    page = request.args.get('page', 1, type=int)
    accommodation_type = request.args.get('type', '')
    
    query = Accommodation.query.filter_by(is_available=True)
    
    if accommodation_type:
        query = query.filter_by(type=accommodation_type)
    
    accommodations = query.paginate(
        page=page, per_page=9, error_out=False
    )
    
    types = ['hotel', 'camping', 'lodge', 'guesthouse']
    
    return render_template('main/accommodations.html', 
                         accommodations=accommodations,
                         types=types,
                         current_type=accommodation_type)

@bp.route('/accommodation/<int:id>')
def accommodation_detail(id):
    accommodation = Accommodation.query.get_or_404(id)
    return render_template('main/accommodation_detail.html', accommodation=accommodation)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's bookings
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    # Get recent bookings (last 3)
    recent_bookings = user_bookings[:3]
    
    # Get recent reviews (last 3)
    recent_reviews = user_reviews[:3]
    
    # Get upcoming bookings (confirmed and pending)
    from datetime import datetime
    upcoming_bookings = [b for b in user_bookings if b.status in ['confirmed', 'pending'] and b.booking_date >= datetime.now()]
    
    return render_template('main/dashboard.html', 
                         user_bookings=user_bookings,
                         user_reviews=user_reviews,
                         recent_bookings=recent_bookings,
                         recent_reviews=recent_reviews,
                         upcoming_bookings=upcoming_bookings)

@bp.route('/profile')
@login_required
def profile():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    return render_template('main/profile.html', 
                         bookings=user_bookings,
                         reviews=user_reviews)
