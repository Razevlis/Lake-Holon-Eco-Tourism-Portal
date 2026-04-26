import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from app.py directly
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import app module
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", "app.py")
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

from database import db
from app.models import User, Activity, Guide, Trail, Accommodation
from datetime import datetime

def init_sample_data():
    app = app_module.create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@lakeholon.com',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample guides
        guides = [
            Guide(
                name='Juan Dela Cruz',
                email='juan@lakeholon.com',
                phone='+639123456789',
                specialization='Mountain Hiking',
                experience_years=8,
                bio='Experienced mountain guide with extensive knowledge of Lake Holon trails.',
                rating=4.8
            ),
            Guide(
                name='Maria Santos',
                email='maria@lakeholon.com',
                phone='+639987654321',
                specialization='Wildlife Photography',
                experience_years=5,
                bio='Professional photographer and nature enthusiast.',
                rating=4.9
            ),
            Guide(
                name='Carlos Reyes',
                email='carlos@lakeholon.com',
                phone='+639456789123',
                specialization='Cultural Tours',
                experience_years=10,
                bio='Local cultural expert sharing the rich heritage of Lake Holon.',
                rating=4.7
            )
        ]
        
        for guide in guides:
            db.session.add(guide)
        
        # Create sample activities
        activities = [
            Activity(
                name='Lake Holon Sunrise Trek',
                description='Experience the breathtaking sunrise over Lake Holon with an early morning trek. This guided tour takes you through scenic trails to the best viewing spots.',
                category='hiking',
                difficulty='moderate',
                duration_hours=4.0,
                max_participants=12,
                price=45.0
            ),
            Activity(
                name='Wildlife Photography Workshop',
                description='Learn professional wildlife photography techniques while exploring the diverse ecosystem around Lake Holon. Perfect for photography enthusiasts.',
                category='photography',
                difficulty='easy',
                duration_hours=6.0,
                max_participants=8,
                price=75.0
            ),
            Activity(
                name='Cultural Heritage Tour',
                description='Discover the rich cultural heritage of the local communities around Lake Holon. Visit traditional villages and learn about local customs.',
                category='cultural',
                difficulty='easy',
                duration_hours=3.0,
                max_participants=15,
                price=35.0
            ),
            Activity(
                name='Lakeside Camping Experience',
                description='Spend a night under the stars at our eco-friendly camping site near Lake Holon. Includes dinner and breakfast.',
                category='camping',
                difficulty='easy',
                duration_hours=24.0,
                max_participants=20,
                price=120.0
            ),
            Activity(
                name='Advanced Trail Challenge',
                description='Test your limits with this challenging trail that takes you to the highest peaks around Lake Holon. For experienced hikers only.',
                category='hiking',
                difficulty='hard',
                duration_hours=8.0,
                max_participants=6,
                price=85.0
            ),
            Activity(
                name='Bird Watching Expedition',
                description='Join our expert ornithologist for a morning of bird watching. Lake Holon is home to over 100 species of birds.',
                category='wildlife',
                difficulty='easy',
                duration_hours=4.0,
                max_participants=10,
                price=40.0
            )
        ]
        
        for activity in activities:
            db.session.add(activity)
        
        # Create sample trails
        trails = [
            Trail(
                name='Lake Holon Circuit Trail',
                description='A scenic trail that circles the entire lake, offering stunning views from multiple angles.',
                difficulty='moderate',
                length_km=12.5,
                estimated_duration=4.5,
                elevation_gain=350,
                trail_type='loop',
                start_point='Main Visitor Center',
                end_point='Main Visitor Center'
            ),
            Trail(
                name='Summit Ridge Trail',
                description='Challenging trail to the highest viewpoint overlooking Lake Holon.',
                difficulty='hard',
                length_km=8.0,
                estimated_duration=5.0,
                elevation_gain=650,
                trail_type='out-and-back',
                start_point='North Parking Area',
                end_point='Summit Viewpoint'
            ),
            Trail(
                name='Lakeside Walk',
                description='Easy walking path along the shoreline, perfect for families and casual walkers.',
                difficulty='easy',
                length_km=3.0,
                estimated_duration=1.5,
                elevation_gain=50,
                trail_type='loop',
                start_point='East Beach Entrance',
                end_point='East Beach Entrance'
            ),
            Trail(
                name='Forest Discovery Trail',
                description='Educational trail through the surrounding forest with interpretive signs about local flora and fauna.',
                difficulty='easy',
                length_km=5.0,
                estimated_duration=2.5,
                elevation_gain=150,
                trail_type='loop',
                start_point='Nature Center',
                end_point='Nature Center'
            )
        ]
        
        for trail in trails:
            db.session.add(trail)
        
        # Create sample accommodations
        accommodations = [
            Accommodation(
                name='Lake Holon Eco Lodge',
                description='Sustainable eco-friendly lodge with panoramic lake views. Solar powered and uses rainwater harvesting.',
                type='lodge',
                location='North Shore, Lake Holon',
                price_per_night=120.0,
                max_occupancy=4,
                amenities='WiFi, Restaurant, Bar, Swimming Pool, Spa, Guided Tours, Airport Shuttle'
            ),
            Accommodation(
                name='Lakeside Camping Grounds',
                description='Pristine camping spots right by the lake with basic facilities. Perfect for nature lovers.',
                type='camping',
                location='East Beach Area, Lake Holon',
                price_per_night=25.0,
                max_occupancy=6,
                amenities='Toilets, Showers, Picnic Tables, Fire Pits, Drinking Water, Security'
            ),
            Accommodation(
                name='Mountain View Hotel',
                description='Comfortable hotel with modern amenities and stunning mountain views.',
                type='hotel',
                location='South Entrance, Lake Holon',
                price_per_night=85.0,
                max_occupancy=2,
                amenities='WiFi, Air Conditioning, TV, Mini Bar, Room Service, Restaurant, Gym'
            ),
            Accommodation(
                name='Local Family Guesthouse',
                description='Authentic local experience with warm hospitality and home-cooked meals.',
                type='guesthouse',
                location='Village Center, Lake Holon',
                price_per_night=45.0,
                max_occupancy=3,
                amenities='WiFi, Breakfast, Laundry Service, Local Tours, Bicycle Rental'
            )
        ]
        
        for accommodation in accommodations:
            db.session.add(accommodation)
        
        # Commit all changes
        db.session.commit()
        
        print("Sample data initialized successfully!")
        print("Admin login: username='admin', password='admin123'")

if __name__ == '__main__':
    init_sample_data()
