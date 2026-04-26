from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from app.admin import bp
from app.admin.forms import ActivityForm, GuideForm, TrailForm, AccommodationForm
from app.models import Activity, Guide, Trail, Accommodation, Booking, User, VisitorAnalytics, Review
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_activities = Activity.query.count()
    total_guides = Guide.query.count()
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    # Get visitor analytics for the last 7 days
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    analytics = VisitorAnalytics.query.filter(
        VisitorAnalytics.date >= start_date,
        VisitorAnalytics.date <= end_date
    ).order_by(VisitorAnalytics.date.desc()).all()
    
    # Get data for pie charts
    booking_status_stats = db.session.query(
        Booking.status,
        db.func.count(Booking.id).label('count')
    ).group_by(Booking.status).all()
    
    user_type_stats = {
        'admin_users': User.query.filter_by(is_admin=True).count(),
        'regular_users': User.query.filter_by(is_admin=False).count()
    }
    
    activity_category_stats = db.session.query(
        Activity.category,
        db.func.count(Activity.id).label('count')
    ).group_by(Activity.category).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_bookings=total_bookings,
                         total_activities=total_activities,
                         total_guides=total_guides,
                         recent_bookings=recent_bookings,
                         analytics=analytics,
                         booking_status_stats=booking_status_stats,
                         user_type_stats=user_type_stats,
                         activity_category_stats=activity_category_stats)

# Activity Management
@bp.route('/activities')
@login_required
@admin_required
def manage_activities():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/manage_activities.html', activities=activities)

@bp.route('/activity/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            difficulty=form.difficulty.data,
            duration_hours=form.duration_hours.data,
            max_participants=form.max_participants.data,
            price=form.price.data,
            image_url=form.image_url.data,
            is_active=form.is_active.data
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity created successfully!', 'success')
        return redirect(url_for('admin.manage_activities'))
    
    return render_template('admin/activity_form.html', form=form, title='Create Activity')

@bp.route('/activity/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_activity(id):
    activity = Activity.query.get_or_404(id)
    form = ActivityForm(obj=activity)
    
    if form.validate_on_submit():
        activity.name = form.name.data
        activity.description = form.description.data
        activity.category = form.category.data
        activity.difficulty = form.difficulty.data
        activity.duration_hours = form.duration_hours.data
        activity.max_participants = form.max_participants.data
        activity.price = form.price.data
        activity.image_url = form.image_url.data
        activity.is_active = form.is_active.data
        
        db.session.commit()
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('admin.manage_activities'))
    
    return render_template('admin/activity_form.html', form=form, title='Edit Activity')

@bp.route('/activity/<int:id>/delete')
@login_required
@admin_required
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted successfully!', 'success')
    return redirect(url_for('admin.manage_activities'))

# Guide Management
@bp.route('/guides')
@login_required
@admin_required
def manage_guides():
    page = request.args.get('page', 1, type=int)
    guides = Guide.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/manage_guides.html', guides=guides)

@bp.route('/guide/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_guide():
    form = GuideForm()
    if form.validate_on_submit():
        guide = Guide(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            specialization=form.specialization.data,
            experience_years=form.experience_years.data,
            bio=form.bio.data,
            image_url=form.image_url.data,
            is_available=form.is_available.data
        )
        db.session.add(guide)
        db.session.commit()
        flash('Guide created successfully!', 'success')
        return redirect(url_for('admin.manage_guides'))
    
    return render_template('admin/guide_form.html', form=form, title='Create Guide')

@bp.route('/guide/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_guide(id):
    guide = Guide.query.get_or_404(id)
    form = GuideForm(obj=guide)
    
    if form.validate_on_submit():
        guide.name = form.name.data
        guide.email = form.email.data
        guide.phone = form.phone.data
        guide.specialization = form.specialization.data
        guide.experience_years = form.experience_years.data
        guide.bio = form.bio.data
        guide.image_url = form.image_url.data
        guide.is_available = form.is_available.data
        
        db.session.commit()
        flash('Guide updated successfully!', 'success')
        return redirect(url_for('admin.manage_guides'))
    
    return render_template('admin/guide_form.html', form=form, title='Edit Guide')

@bp.route('/guide/<int:id>/delete')
@login_required
@admin_required
def delete_guide(id):
    guide = Guide.query.get_or_404(id)
    db.session.delete(guide)
    db.session.commit()
    flash('Guide deleted successfully!', 'success')
    return redirect(url_for('admin.manage_guides'))

# Booking Management
@bp.route('/bookings')
@login_required
@admin_required
def manage_bookings():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    user_filter = request.args.get('user', '')
    activity_filter = request.args.get('activity', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Booking.query
    
    if status:
        query = query.filter_by(status=status)
    
    if user_filter:
        query = query.join(User).filter(User.username.contains(user_filter))
    
    if activity_filter:
        query = query.join(Activity).filter(Activity.name.contains(activity_filter))
    
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Booking.booking_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            from datetime import datetime
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Booking.booking_date <= date_to_obj)
        except ValueError:
            pass
    
    bookings = query.order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Get statistics
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
    cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
    
    return render_template('admin/manage_bookings.html', 
                         bookings=bookings, 
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         confirmed_bookings=confirmed_bookings,
                         cancelled_bookings=cancelled_bookings)

@bp.route('/booking/<int:id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_booking_status(id):
    booking = Booking.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        booking.status = new_status
        db.session.commit()
        flash('Booking status updated successfully!', 'success')
    else:
        flash('Invalid status.', 'danger')
    
    return redirect(url_for('admin.manage_bookings'))

@bp.route('/booking/<int:booking_id>/confirm')
@login_required
@admin_required
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'pending':
        booking.status = 'confirmed'
        db.session.commit()
        flash(f'Booking #{booking_id} has been confirmed.', 'success')
    else:
        flash('Only pending bookings can be confirmed.', 'warning')
    return redirect(url_for('admin.manage_bookings'))

@bp.route('/booking/<int:booking_id>/cancel')
@login_required
@admin_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        db.session.commit()
        flash(f'Booking #{booking_id} has been cancelled.', 'success')
    else:
        flash('Only pending or confirmed bookings can be cancelled.', 'warning')
    return redirect(url_for('admin.manage_bookings'))

# User Management
@bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page, per_page=15, error_out=False
    )
    return render_template('admin/manage_users.html', users=users)

@bp.route('/user/<int:id>/toggle_admin')
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user.id != current_user.id:  # Prevent self-admin removal
        user.is_admin = not user.is_admin
        db.session.commit()
        action = 'granted' if user.is_admin else 'revoked'
        flash(f'Admin privileges {action} for {user.username}.', 'success')
    else:
        flash('You cannot modify your own admin status.', 'warning')
    
    return redirect(url_for('admin.manage_users'))

# Recommendation Management
@bp.route('/recommendations')
@login_required
@admin_required
def manage_recommendations():
    # Get recommendation statistics
    total_reviews = Review.query.count()
    total_activities = Activity.query.count()
    total_guides = Guide.query.count()
    
    # Get recent reviews
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    
    # Get activity rating statistics
    activity_ratings = db.session.query(
        Activity.name,
        db.func.avg(Review.rating).label('avg_rating'),
        db.func.count(Review.id).label('review_count')
    ).join(Review).group_by(Activity.id).order_by(db.func.avg(Review.rating).desc()).all()
    
    # Get guide rating statistics  
    guide_ratings = db.session.query(
        Guide.name,
        Guide.specialization,
        Guide.rating,
        Guide.experience_years
    ).order_by(Guide.rating.desc()).limit(10).all()
    
    return render_template('admin/recommendations.html',
                         total_reviews=total_reviews,
                         total_activities=total_activities,
                         total_guides=total_guides,
                         recent_reviews=recent_reviews,
                         activity_ratings=activity_ratings,
                         guide_ratings=guide_ratings)

@bp.route('/recommendations/delete_review/<int:review_id>')
@login_required
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    activity_name = review.activity.name
    db.session.delete(review)
    db.session.commit()
    flash(f'Review for {activity_name} has been deleted.', 'success')
    return redirect(url_for('admin.manage_recommendations'))

@bp.route('/recommendations/clear_all_reviews')
@login_required
@admin_required
def clear_all_reviews():
    # This will delete all reviews from the system
    review_count = Review.query.count()
    if review_count > 0:
        Review.query.delete()
        db.session.commit()
        flash(f'All {review_count} reviews have been deleted from the system.', 'success')
    else:
        flash('No reviews found to delete.', 'info')
    return redirect(url_for('admin.manage_recommendations'))

# Analytics Management
@bp.route('/analytics')
@login_required
@admin_required
def analytics():
    from datetime import datetime, timedelta
    
    # Get date ranges
    end_date = datetime.now()
    start_date_7_days = end_date - timedelta(days=7)
    start_date_30_days = end_date - timedelta(days=30)
    
    # User analytics
    total_users = User.query.count()
    new_users_7_days = User.query.filter(User.created_at >= start_date_7_days).count()
    new_users_30_days = User.query.filter(User.created_at >= start_date_30_days).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Booking analytics
    total_bookings = Booking.query.count()
    bookings_7_days = Booking.query.filter(Booking.created_at >= start_date_7_days).count()
    bookings_30_days = Booking.query.filter(Booking.created_at >= start_date_30_days).count()
    
    # Revenue analytics
    total_revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0
    revenue_7_days = db.session.query(db.func.sum(Booking.total_price)).filter(Booking.created_at >= start_date_7_days).scalar() or 0
    revenue_30_days = db.session.query(db.func.sum(Booking.total_price)).filter(Booking.created_at >= start_date_30_days).scalar() or 0
    
    # Activity popularity
    activity_stats = db.session.query(
        Activity.name,
        db.func.count(Booking.id).label('booking_count'),
        db.func.sum(Booking.total_price).label('revenue')
    ).join(Booking).group_by(Activity.id).order_by(db.func.count(Booking.id).desc()).limit(10).all()
    
    # Booking status breakdown
    booking_status_stats = db.session.query(
        Booking.status,
        db.func.count(Booking.id).label('count')
    ).group_by(Booking.status).all()
    
    # Daily bookings for last 30 days
    daily_bookings = []
    for i in range(30):
        date = end_date - timedelta(days=i)
        count = Booking.query.filter(
            Booking.created_at >= date.date(),
            Booking.created_at < (date + timedelta(days=1)).date()
        ).count()
        daily_bookings.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    daily_bookings.reverse()
    
    # Monthly revenue for last 12 months
    monthly_revenue = []
    for i in range(12):
        month_start = end_date.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        revenue = db.session.query(db.func.sum(Booking.total_price)).filter(
            Booking.created_at >= month_start,
            Booking.created_at <= month_end
        ).scalar() or 0
        monthly_revenue.append({
            'month': month_start.strftime('%Y-%m'),
            'revenue': float(revenue)
        })
    monthly_revenue.reverse()
    
    return render_template('admin/analytics.html',
                         total_users=total_users,
                         new_users_7_days=new_users_7_days,
                         new_users_30_days=new_users_30_days,
                         admin_users=admin_users,
                         total_bookings=total_bookings,
                         bookings_7_days=bookings_7_days,
                         bookings_30_days=bookings_30_days,
                         total_revenue=total_revenue,
                         revenue_7_days=revenue_7_days,
                         revenue_30_days=revenue_30_days,
                         activity_stats=activity_stats,
                         booking_status_stats=booking_status_stats,
                         daily_bookings=daily_bookings,
                         monthly_revenue=monthly_revenue)
