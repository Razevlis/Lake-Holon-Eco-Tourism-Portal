#!/usr/bin/env python3
"""
Script to add placeholder images to activities that don't have them
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application import create_app
from database import db
from app.models import Activity

def add_activity_images():
    """Add placeholder images to activities without images"""
    app = create_app()
    
    with app.app_context():
        # Define placeholder images for different activity categories
        placeholder_images = {
            'hiking': [
                'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1464822759844-d150baec0494?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop'
            ],
            'camping': [
                'https://images.unsplash.com/photo-1508873696983-2ccb989b1257?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1534870249593-9b2153a3b9b8?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1504280390367-361c6dd9d930?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1523731547312-f9c2e28d6140?w=800&h=600&fit=crop'
            ],
            'photography': [
                'https://images.unsplash.com/photo-1502780402664-1b5b3c3b8b3b?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1516035068371-29a1b244cc32?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?w=800&h=600&fit=crop'
            ],
            'cultural': [
                'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1507525428034-b723a9ce6890?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop'
            ],
            'wildlife': [
                'https://images.unsplash.com/photo-1552728089-a573c98a24e9?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1437622368342-7a3d73a05c58?w=800&h=600&fit=crop'
            ],
            'water_sports': [
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1507525428034-b723a9ce6890?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop'
            ]
        }
        
        # Default images for activities without specific category images
        default_images = [
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1507525428034-b723a9ce6890?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&h=600&fit=crop'
        ]
        
        # Get all activities without images
        activities_without_images = Activity.query.filter(
            (Activity.image_url.is_(None)) | (Activity.image_url == '')
        ).all()
        
        print(f"Found {len(activities_without_images)} activities without images")
        
        updated_count = 0
        for activity in activities_without_images:
            # Get images for the activity's category
            category_images = placeholder_images.get(activity.category.lower(), default_images)
            
            # Select an image based on activity ID to ensure consistency
            image_index = activity.id % len(category_images)
            selected_image = category_images[image_index]
            
            # Update the activity
            activity.image_url = selected_image
            updated_count += 1
            
            print(f"Updated: {activity.name} -> {selected_image}")
        
        # Commit changes
        db.session.commit()
        print(f"\nSuccessfully updated {updated_count} activities with placeholder images!")
        
        # Show summary
        total_activities = Activity.query.count()
        activities_with_images = Activity.query.filter(
            (Activity.image_url.isnot(None)) & (Activity.image_url != '')
        ).count()
        
        print(f"\nSummary:")
        print(f"Total activities: {total_activities}")
        print(f"Activities with images: {activities_with_images}")
        print(f"Activities without images: {total_activities - activities_with_images}")

if __name__ == '__main__':
    add_activity_images()
