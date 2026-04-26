from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from database import db
from app.booking import bp
from app.booking.forms import BookingForm, ReviewForm
from app.models import Activity, Guide, Booking, Review, VisitorAnalytics
from datetime import datetime, date

@bp.route('/create/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def create_booking(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    
    form = BookingForm()
    form.activity_id.data = activity_id
    
    # Populate activity choices
    activities = Activity.query.filter_by(is_active=True).all()
    form.activity_id.choices = [(a.id, a.name) for a in activities]
    
    # Populate guide choices
    guides = Guide.query.filter_by(is_available=True).all()
    form.guide_id.choices = [(g.id, f"{g.name} - {g.specialization}") for g in guides]
    
    if form.validate_on_submit():
        # Calculate total price
        total_price = activity.price * form.number_of_participants.data
        
        # Create booking
        booking = Booking(
            user_id=current_user.id,
            activity_id=activity_id,
            guide_id=form.guide_id.data,
            booking_date=form.booking_date.data,
            number_of_participants=form.number_of_participants.data,
            total_price=total_price,
            special_requests=form.special_requests.data
        )
        
        db.session.add(booking)
        
        # Update analytics
        today = date.today()
        analytics = VisitorAnalytics.query.filter_by(date=today).first()
        if analytics:
            analytics.bookings_made += 1
        else:
            analytics = VisitorAnalytics(date=today, bookings_made=1)
            db.session.add(analytics)
        
        db.session.commit()
        
        flash('Your booking has been created successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('booking/create_booking.html', 
                         form=form, 
                         activity=activity)

@bp.route('/manage')
@login_required
def manage_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('booking/manage_bookings.html', bookings=bookings)

@bp.route('/cancel/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('You can only cancel your own bookings.', 'danger')
        return redirect(url_for('booking.manage_bookings'))
    
    if booking.status in ['confirmed', 'pending']:
        booking.status = 'cancelled'
        db.session.commit()
        flash('Your booking has been cancelled.', 'info')
    else:
        flash('This booking cannot be cancelled.', 'warning')
    
    return redirect(url_for('booking.manage_bookings'))

@bp.route('/review/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def create_review(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    
    # Check if user has completed a booking for this activity
    has_booked = Booking.query.filter_by(
        user_id=current_user.id, 
        activity_id=activity_id, 
        status='completed'
    ).first()
    
    if not has_booked:
        flash('You can only review activities you have completed.', 'warning')
        return redirect(url_for('main.activity_detail', id=activity_id))
    
    # Check if user has already reviewed this activity
    existing_review = Review.query.filter_by(
        user_id=current_user.id, 
        activity_id=activity_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this activity.', 'info')
        return redirect(url_for('main.activity_detail', id=activity_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            activity_id=activity_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Your review has been submitted successfully!', 'success')
        return redirect(url_for('main.activity_detail', id=activity_id))
    
    return render_template('booking/create_review.html', 
                         form=form, 
                         activity=activity)
