#!/usr/bin/env python3
"""
Script to update activity images with more category-specific and Lake Holon relevant images
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application import create_app
from database import db
from app.models import Activity

def update_activity_images():
    """Update activity images with more category-specific images"""
    app = create_app()
    
    with app.app_context():
        # Define more specific and relevant images for each activity category
        category_specific_images = {
            'hiking': [
                'https://images.unsplash.com/photo-1464822759844-d150baec0494?w=800&h=600&fit=crop',  # Mountain sunrise
                'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&h=600&fit=crop',  # Mountain trail
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',  # Hiker on mountain
                'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&h=600&fit=crop',  # Mountain lake view
                'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop'   # Lake mountain view
            ],
            'camping': [
                'https://images.unsplash.com/photo-1508873696983-2ccb989b1257?w=800&h=600&fit=crop',  # Tent by lake
                'https://images.unsplash.com/photo-1534870249593-9b2153a3b9b8?w=800&h=600&fit=crop',  # Camping by water
                'https://images.unsplash.com/photo-1523731547312-f9c2e28d6140?w=800&h=600&fit=crop',  # Lakeside camping
                'https://images.unsplash.com/photo-1504280390367-361c6dd9d930?w=800&h=600&fit=crop',  # Tent with lake view
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop'   # Camping in mountains
            ],
            'photography': [
                'https://images.unsplash.com/photo-1502780402664-1b5b3c3b8b3b?w=800&h=600&fit=crop',  # Photographer with camera
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',  # Nature photography
                'https://images.unsplash.com/photo-1516035068371-29a1b244cc32?w=800&h=600&fit=crop',  # Photography equipment
                'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?w=800&h=600&fit=crop',  # Landscape photography
                'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=600&fit=crop'   # Nature photographer
            ],
            'cultural': [
                'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&h=600&fit=crop',  # Cultural experience
                'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&h=600&fit=crop',  # Local culture
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop',  # Cultural tour
                'https://images.unsplash.com/photo-1507525428034-b723a9ce6890?w=800&h=600&fit=crop',  # Traditional experience
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop'   # Cultural heritage
            ],
            'wildlife': [
                'https://images.unsplash.com/photo-1552728089-a573c98a24e9?w=800&h=600&fit=crop',  # Eagle in flight
                'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&h=600&fit=crop',  # Bird watching
                'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=800&h=600&fit=crop',  # Wildlife in nature
                'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800&h=600&fit=crop',  # Deer in forest
                'https://images.unsplash.com/photo-1437622368342-7a3d73a05c58?w=800&h=600&fit=crop'   # Birds in nature
            ],
            'water_sports': [
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop',  # Kayaking on lake
                'https://images.unsplash.com/photo-1507525428034-b723a9ce6890?w=800&h=600&fit=crop',  # Lake activities
                'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800&h=600&fit=crop',  # Water sports
                'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&h=600&fit=crop',  # Lake recreation
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop'   # Water activities
            ]
        }
        
        # Get all activities
        all_activities = Activity.query.filter_by(is_active=True).all()
        
        print(f"Updating {len(all_activities)} activities with category-specific images...")
        
        updated_count = 0
        for activity in all_activities:
            # Get images for the activity's category
            category_images = category_specific_images.get(activity.category.lower(), [])
            
            if category_images:
                # Select an image based on activity name for variety
                image_index = hash(activity.name) % len(category_images)
                selected_image = category_images[image_index]
                
                # Update the activity
                old_image = activity.image_url
                activity.image_url = selected_image
                updated_count += 1
                
                print(f"Updated: {activity.name} ({activity.category})")
                print(f"  Old: {old_image}")
                print(f"  New: {selected_image}")
                print()
            else:
                print(f"No specific images found for category: {activity.category}")
        
        # Commit changes
        db.session.commit()
        print(f"\nSuccessfully updated {updated_count} activities with category-specific images!")
        
        # Show summary by category
        print(f"\nSummary by category:")
        categories = db.session.query(Activity.category).distinct().all()
        for category in categories:
            category_name = category[0]
            count = Activity.query.filter_by(category=category_name).count()
            print(f"  {category_name.title()}: {count} activities")

if __name__ == '__main__':
    update_activity_images()
