# Lake Holon Eco-Tourism Portal

A comprehensive eco-tourism management system built with Flask that provides centralized information, online booking, AI-powered recommendations, and visitor analytics for Lake Holon tourism.

## Features

### Core Features
- **Tourist Account System**: Secure registration and login for tourists to book trips and access personal itineraries
- **Lake Holon Information Portal**: Detailed pages about trails, activities, accommodations, and local guides
- **Online Booking and Reservation Module**: Enables users to reserve guided tours, camping sites, or permits
- **Admin Dashboard**: Allows authorities to manage bookings, guides, and monitor visitor statistics
- **AI Travel Recommendation System**: Suggests the best itinerary, activities, or guides based on preferences, weather, and availability

### Additional Features
- **Visitor Analytics**: Real-time insights on visitor trends and popular activities
- **Searchable Directory**: Geolocation and reviews for easy access to tours and services
- **Responsive Design**: Mobile-friendly interface for all devices
- **Secure Payment Integration**: Ready for payment gateway integration
- **Multi-language Support**: Extensible for international tourists

## Technology Stack

- **Backend**: Flask (Python Web Framework)
- **Database**: SQLAlchemy with SQLite (easily configurable for PostgreSQL/MySQL)
- **Authentication**: Flask-Login with password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Frontend**: Bootstrap 5 with custom CSS
- **AI Recommendations**: Scikit-learn for personalized recommendations
- **Analytics**: Custom visitor tracking system

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project** to your local directory

2. **Navigate to the project directory**:
   ```bash
   cd Lakeholon_eco_tourism_portal
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database** with sample data:
   ```bash
   python init_data.py
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

7. **Access the application**:
   - Open your web browser and go to `http://localhost:5000`
   - Admin login: username=`admin`, password=`admin123`

## Project Structure

```
Lakeholon_eco_tourism_portal/
├── app/
│   ├── __init__.py
│   ├── models.py                 # Database models
│   ├── auth/                     # Authentication module
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/                     # Main application routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/                    # Admin dashboard
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── booking/                  # Booking system
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── recommendations/          # AI recommendation system
│   │   ├── __init__.py
│   │   └── routes.py
│   └── templates/                # HTML templates
│       ├── base.html
│       ├── auth/
│       ├── main/
│       ├── admin/
│       ├── booking/
│       └── recommendations/
├── config.py                     # Configuration settings
├── run.py                        # Application entry point
├── init_data.py                  # Sample data initialization
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Usage Guide

### For Tourists
1. **Register** an account to access all features
2. **Browse activities**, trails, and accommodations
3. **Book tours** and activities with secure online payment
4. **Get personalized recommendations** based on preferences
5. **Leave reviews** for completed activities
6. **Manage bookings** through your profile

### For Administrators
1. **Login** with admin credentials
2. **Access dashboard** for overview and analytics
3. **Manage activities** - add, edit, delete activities
4. **Manage guides** - add guide profiles and availability
5. **Monitor bookings** - view and update booking status
6. **Track visitors** - analyze visitor trends and statistics

### AI Recommendations
The system uses machine learning to provide personalized recommendations:
- Analyzes user booking history and preferences
- Considers activity ratings and popularity
- Factors in budget and time constraints
- Provides itinerary suggestions for multi-day trips

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///lakeholon_tourism.db
FLASK_CONFIG=development
```

### Database Configuration
Default configuration uses SQLite. For production, update `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/lakeholon_db'
```

## Features in Detail

### 1. Tourist Account System
- Secure registration with email validation
- Password hashing with bcrypt
- Profile management
- Booking history
- Review management

### 2. Information Portal
- **Activities**: Browse by category, difficulty, duration
- **Trails**: Detailed trail information with difficulty ratings
- **Guides**: Professional guide profiles with specializations
- **Accommodations**: Various lodging options with amenities

### 3. Online Booking System
- Real-time availability checking
- Secure booking process
- Payment integration ready
- Booking status tracking
- Cancellation management

### 4. Admin Dashboard
- User management
- Activity and guide management
- Booking oversight
- Visitor analytics
- System statistics

### 5. AI Recommendation Engine
- Collaborative filtering
- Content-based recommendations
- Personalized itineraries
- Preference-based suggestions

## Security Features
- CSRF protection on all forms
- Password hashing with bcrypt
- Session management
- Admin access control
- Input validation and sanitization

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support
For technical support or questions:
- Check the documentation
- Review the code comments
- Create an issue for bugs or feature requests

## License
This project is open source and available under the MIT License.

## Future Enhancements
- Mobile app development
- Real-time weather integration
- Multi-language support
- Advanced analytics dashboard
- Social media integration
- Loyalty program for repeat visitors
- Virtual tour features
- Sustainable tourism tracking
