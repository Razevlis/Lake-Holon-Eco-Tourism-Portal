from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from database import db
from app.recommendations import bp
from app.models import Activity, Guide, Booking, Review, User
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
# import numpy as np
import random

@bp.route('/')
@login_required
def get_recommendations():
    # Get user preferences from query parameters
    preferences = {
        'category': request.args.get('category', ''),
        'difficulty': request.args.get('difficulty', ''),
        'duration': request.args.get('duration', ''),
        'budget': request.args.get('budget', '')
    }
    
    # Get recommendations based on preferences and user history
    recommended_activities = get_activity_recommendations(current_user.id, preferences)
    recommended_guides = get_guide_recommendations(current_user.id, preferences)
    
    return render_template('recommendations/recommendations.html',
                         activities=recommended_activities,
                         guides=recommended_guides,
                         preferences=preferences)

def get_activity_recommendations(user_id, preferences):
    # Get all activities
    activities = Activity.query.filter_by(is_active=True).all()
    
    if not activities:
        return []
    
    # Get user's booking history
    user_bookings = db.session.query(Booking.activity_id).filter_by(user_id=user_id).all()
    booked_activity_ids = [booking[0] for booking in user_bookings]
    
    # Get user's reviews
    user_reviews = Review.query.filter_by(user_id=user_id).all()
    
    # Create activity features
    activity_data = []
    for activity in activities:
        features = {
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'category': activity.category,
            'difficulty': activity.difficulty,
            'duration_hours': activity.duration_hours,
            'price': activity.price,
            'max_participants': activity.max_participants,
            'user_interacted': 1 if activity.id in booked_activity_ids else 0
        }
        
        # Add review score
        activity_reviews = Review.query.filter_by(activity_id=activity.id).all()
        if activity_reviews:
            features['avg_rating'] = sum(r.rating for r in activity_reviews) / len(activity_reviews)
            features['review_count'] = len(activity_reviews)
        else:
            features['avg_rating'] = 0
            features['review_count'] = 0
        
        activity_data.append(features)
    
    # Simple recommendation logic without pandas
    # Apply preference filters
    filtered_activities = []
    for activity in activity_data:
        # Apply category filter
        if preferences.get('category') and activity['category'] != preferences['category']:
            continue
        
        # Apply difficulty filter
        if preferences.get('difficulty') and activity['difficulty'] != preferences['difficulty']:
            continue
        
        # Apply duration filter
        if preferences.get('duration'):
            try:
                max_duration = float(preferences['duration'])
                if activity['duration_hours'] > max_duration:
                    continue
            except ValueError:
                pass
        
        # Apply budget filter
        if preferences.get('budget'):
            try:
                max_budget = float(preferences['budget'])
                if activity['price'] > max_budget:
                    continue
            except ValueError:
                pass
        
        # Calculate recommendation score
        score = 0
        
        # Rating score
        score += activity['avg_rating'] * 0.3
        
        # Review count score
        score += min(activity['review_count'] / 5, 1) * 0.2
        
        # User interaction penalty
        score += activity['user_interacted'] * -0.5
        
        # Add some randomness factor for diversity
        score += random.uniform(0, 0.1)
        
        activity['recommendation_score'] = score
        filtered_activities.append(activity)
        filtered_df = [activity for activity in activity_data if activity['difficulty'] == preferences['difficulty']]
    
    if preferences.get('duration'):
        try:
            max_duration = float(preferences['duration'])
            filtered_activities = [activity for activity in activity_data if activity['duration_hours'] <= max_duration]
        except ValueError:
            pass
    
    if preferences.get('budget'):
        try:
            max_budget = float(preferences['budget'])
            filtered_activities = [activity for activity in activity_data if activity['price'] <= max_budget]
        except ValueError:
            pass
    
    if not filtered_activities:
        return []
    
    # Calculate recommendation scores
    for activity in filtered_activities:
        score = 0
        
        # Rating score
        score += activity['avg_rating'] * 0.3
        
        # Review count score
        score += min(activity['review_count'] / 5, 1) * 0.2
        # Add some randomness for diversity
        score += random.uniform(0, 0.1)
        
        activity['recommendation_score'] = score
    
    # Sort by recommendation score
    filtered_activities.sort(key=lambda x: x['recommendation_score'], reverse=True)
    
    # Get top recommendations
    top_activities = filtered_activities[:6]
    
    # Convert back to Activity objects
    recommended_activities = []
    for data in top_activities:
        activity = Activity.query.get(data['id'])
        if activity:
            activity.recommendation_score = data['recommendation_score']
            recommended_activities.append(activity)
    
    return recommended_activities

def get_guide_recommendations(user_id, preferences):
    # Get all available guides
    guides = Guide.query.filter_by(is_available=True).all()
    
    if not guides:
        return []
    
    # Calculate guide scores
    guide_scores = []
    for guide in guides:
        score = 0
        
        # Experience score
        score += min(guide.experience_years / 20, 1) * 0.3
        
        # Rating score
        score += (guide.rating / 5) * 0.4
        
        # Availability bonus
        if guide.is_available:
            score += 0.2
        
        # Random factor for diversity
        score += random.uniform(0, 0.1)
        
        guide_scores.append((guide, score))
    
    # Sort by score
    guide_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top guides
    return [guide for guide, score in guide_scores[:4]]

@bp.route('/api/recommendations')
@login_required
def api_recommendations():
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    
    # Get activity recommendations
    activities = Activity.query.filter_by(is_active=True)
    
    if category:
        activities = activities.filter_by(category=category)
    if difficulty:
        activities = activities.filter_by(difficulty=difficulty)
    
    activities = activities.limit(5).all()
    
    # Format response
    recommendations = []
    for activity in activities:
        recommendations.append({
            'id': activity.id,
            'name': activity.name,
            'description': activity.description[:100] + '...',
            'price': activity.price,
            'category': activity.category,
            'difficulty': activity.difficulty,
            'duration_hours': activity.duration_hours
        })
    
    return jsonify({'recommendations': recommendations})

@bp.route('/itinerary')
@login_required
def create_itinerary():
    # Get user preferences
    preferences = {
        'days': request.args.get('days', 3, type=int),
        'budget': request.args.get('budget', 500, type=float),
        'group_size': request.args.get('group_size', 2, type=int),
        'interests': request.args.getlist('interests')
    }
    
    # Generate itinerary
    itinerary = generate_itinerary(current_user.id, preferences)
    
    return render_template('recommendations/itinerary.html',
                         itinerary=itinerary,
                         preferences=preferences)

def generate_itinerary(user_id, preferences):
    days = preferences.get('days', 3)
    budget = preferences.get('budget', 500)
    group_size = preferences.get('group_size', 2)
    interests = preferences.get('interests', [])
    
    itinerary = []
    remaining_budget = budget
    
    for day in range(1, days + 1):
        day_plan = {
            'day': day,
            'morning': None,
            'afternoon': None,
            'evening': None,
            'total_cost': 0
        }
        
        # Get activities for the day
        available_activities = Activity.query.filter_by(is_active=True).all()
        
        # Filter by interests if specified
        if interests:
            available_activities = [a for a in available_activities if a.category in interests]
        
        # Filter by budget
        affordable_activities = [
            a for a in available_activities 
            if a.price * group_size <= remaining_budget / days
        ]
        
        if affordable_activities:
            # Select morning activity
            morning_activity = random.choice(affordable_activities)
            day_plan['morning'] = morning_activity
            morning_cost = morning_activity.price * group_size
            
            # Select afternoon activity (different from morning)
            remaining_activities = [a for a in affordable_activities if a.id != morning_activity.id]
            if remaining_activities:
                afternoon_activity = random.choice(remaining_activities)
                day_plan['afternoon'] = afternoon_activity
                afternoon_cost = afternoon_activity.price * group_size
            else:
                afternoon_cost = 0
            
            day_plan['total_cost'] = morning_cost + afternoon_cost
            remaining_budget -= day_plan['total_cost']
        
        itinerary.append(day_plan)
    
    return itinerary
