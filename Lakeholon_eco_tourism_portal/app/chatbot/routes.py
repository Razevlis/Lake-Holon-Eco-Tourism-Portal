from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from database import db
from app.chatbot import bp
from app.models import Activity, Guide, Trail, Accommodation, Booking
import re
from datetime import datetime, timedelta

class LakeHolonChatbot:
    def __init__(self):
        self.activities = []
        self.guides = []
        self.trails = []
        self.accommodations = []
    
    def load_data(self):
        """Load data from database"""
        try:
            self.activities = Activity.query.filter_by(is_active=True).all()
            self.guides = Guide.query.filter_by(is_available=True).all()
            self.trails = Trail.query.filter_by(is_active=True).all()
            self.accommodations = Accommodation.query.filter_by(is_active=True).all()
        except Exception as e:
            # If database is not available, use empty lists
            self.activities = []
            self.guides = []
            self.trails = []
            self.accommodations = []
    
    def get_response(self, message, user_id=None):
        """Generate response based on user message"""
        message = message.lower().strip()
        
        # Load fresh data for each request
        self.load_data()
        
        # Greetings
        if any(word in message for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return self.get_greeting_response()
        
        # Help and information
        if any(word in message for word in ['help', 'what can you do', 'how can you help']):
            return self.get_help_response()
        
        # Activities
        if any(word in message for word in ['activity', 'activities', 'things to do', 'what to do']):
            return self.get_activities_response(message)
        
        # Trails
        if any(word in message for word in ['trail', 'trails', 'hiking', 'trek']):
            return self.get_trails_response(message)
        
        # Guides
        if any(word in message for word in ['guide', 'guides', 'tour guide']):
            return self.get_guides_response(message)
        
        # Accommodations
        if any(word in message for word in ['accommodation', 'hotel', 'stay', 'lodging']):
            return self.get_accommodations_response(message)
        
        # Booking
        if any(word in message for word in ['booking', 'book', 'reserve', 'reservation']):
            return self.get_booking_response(message)
        
        # Lake Holon information
        if any(word in message for word in ['lake holon', 'lake', 'holon', 'location', 'where']):
            return self.get_lake_holon_info()
        
        # Pricing
        if any(word in message for word in ['price', 'cost', 'how much', 'fee']):
            return self.get_pricing_response(message)
        
        # Weather and best time
        if any(word in message for word in ['weather', 'best time', 'when to visit', 'season']):
            return self.get_weather_response()
        
        # Difficulty levels
        if any(word in message for word in ['difficulty', 'easy', 'hard', 'moderate', 'challenging']):
            return self.get_difficulty_response(message)
        
        # Default response
        return self.get_default_response()
    
    def get_greeting_response(self):
        responses = [
            "Hello! Welcome to Lake Holon Eco-Tourism Portal! I'm here to help you plan your perfect adventure. What would you like to know?",
            "Hi there! I'm your Lake Holon travel assistant. How can I help you explore our beautiful destination today?",
            "Greetings! Lake Holon is waiting for you! Ask me anything about activities, trails, guides, or accommodations."
        ]
        return responses[hash(len(responses)) % len(responses)]
    
    def get_help_response(self):
        return """I can help you with information about:

🏔️ **Activities**: Hiking, photography, cultural tours, camping, wildlife watching
🥾 **Trails**: Different difficulty levels and scenic routes
👨‍🏫 **Guides**: Professional tour guides and their specializations
🏨 **Accommodations**: Hotels, camping sites, and lodges
💰 **Pricing**: Cost information for activities and services
📅 **Booking**: How to make reservations
🌤️ **Best times**: When to visit and weather information

Just ask me anything about Lake Holon!"""
    
    def get_activities_response(self, message):
        if not self.activities:
            return "I'm sorry, but I don't have any activity information available right now. Please check back later."
        
        # Filter activities based on keywords
        filtered_activities = self.activities
        
        if 'hiking' in message:
            filtered_activities = [a for a in filtered_activities if 'hiking' in a.category.lower()]
        elif 'photography' in message:
            filtered_activities = [a for a in filtered_activities if 'photography' in a.category.lower()]
        elif 'cultural' in message:
            filtered_activities = [a for a in filtered_activities if 'cultural' in a.category.lower()]
        elif 'camping' in message:
            filtered_activities = [a for a in filtered_activities if 'camping' in a.category.lower()]
        elif 'wildlife' in message:
            filtered_activities = [a for a in filtered_activities if 'wildlife' in a.category.lower()]
        
        if 'easy' in message:
            filtered_activities = [a for a in filtered_activities if a.difficulty == 'easy']
        elif 'hard' in message or 'challenging' in message:
            filtered_activities = [a for a in filtered_activities if a.difficulty == 'hard']
        elif 'moderate' in message:
            filtered_activities = [a for a in filtered_activities if a.difficulty == 'moderate']
        
        if not filtered_activities:
            return "I couldn't find any activities matching your criteria. Try asking about different activities or difficulty levels."
        
        response = f"Here are some great activities at Lake Holon:\n\n"
        for activity in filtered_activities[:5]:
            response += f"🏔️ **{activity.name}**\n"
            response += f"   Category: {activity.category.title()}\n"
            response += f"   Difficulty: {activity.difficulty.title()}\n"
            response += f"   Price: ${activity.price}\n"
            response += f"   Duration: {activity.duration}\n\n"
        
        if len(filtered_activities) > 5:
            response += f"And {len(filtered_activities) - 5} more activities! Would you like more details about any specific one?"
        
        return response
    
    def get_trails_response(self, message):
        if not self.trails:
            return "I'm sorry, but I don't have trail information available right now."
        
        # Filter trails based on keywords
        filtered_trails = self.trails
        
        if 'easy' in message:
            filtered_trails = [t for t in filtered_trails if t.difficulty == 'easy']
        elif 'hard' in message or 'challenging' in message:
            filtered_trails = [t for t in filtered_trails if t.difficulty == 'hard']
        elif 'moderate' in message:
            filtered_trails = [t for t in filtered_trails if t.difficulty == 'moderate']
        
        if not filtered_trails:
            return "I couldn't find any trails matching your criteria. Try asking about different difficulty levels."
        
        response = f"Here are some amazing trails at Lake Holon:\n\n"
        for trail in filtered_trails[:3]:
            response += f"🥾 **{trail.name}**\n"
            response += f"   Difficulty: {trail.difficulty.title()}\n"
            response += f"   Distance: {trail.distance} km\n"
            response += f"   Duration: {trail.duration}\n"
            response += f"   Elevation: {trail.elevation_gain}m gain\n\n"
        
        return response
    
    def get_guides_response(self, message):
        if not self.guides:
            return "I'm sorry, but I don't have guide information available right now."
        
        # Filter guides based on keywords
        filtered_guides = self.guides
        
        if 'hiking' in message:
            filtered_guides = [g for g in filtered_guides if 'hiking' in g.specialization.lower()]
        elif 'photography' in message:
            filtered_guides = [g for g in filtered_guides if 'photography' in g.specialization.lower()]
        elif 'cultural' in message:
            filtered_guides = [g for g in filtered_guides if 'cultural' in g.specialization.lower()]
        
        if not filtered_guides:
            filtered_guides = self.guides
        
        response = f"Here are our expert guides at Lake Holon:\n\n"
        for guide in filtered_guides[:3]:
            response += f"👨‍🏫 **{guide.name}**\n"
            response += f"   Specialization: {guide.specialization}\n"
            response += f"   Experience: {guide.experience_years} years\n"
            response += f"   Rating: ⭐{guide.rating}\n\n"
        
        return response
    
    def get_accommodations_response(self, message):
        if not self.accommodations:
            return "I'm sorry, but I don't have accommodation information available right now."
        
        response = f"Here are accommodation options at Lake Holon:\n\n"
        for accommodation in self.accommodations[:3]:
            response += f"🏨 **{accommodation.name}**\n"
            response += f"   Type: {accommodation.type.title()}\n"
            response += f"   Price: ${accommodation.price_per_night}/night\n"
            response += f"   Location: {accommodation.location}\n\n"
        
        return response
    
    def get_booking_response(self, message):
        return """To make a booking at Lake Holon:

1. Browse activities on our website
2. Select your preferred activity and date
3. Choose the number of participants
4. Fill in your details
5. Complete the payment

You can also book by calling our hotline or visiting our tourist center. Need help with a specific activity?"""
    
    def get_lake_holon_info(self):
        return """🌊 **About Lake Holon**

Lake Holon is a stunning crater lake located in South Cotabato, Philippines. Known as the "Queen of Philippine Lakes," it's a popular destination for:

🏔️ **Hiking and Trekking**: Challenging trails with breathtaking views
📸 **Photography**: Perfect for landscape and nature photography
🌿 **Eco-Tourism**: Pristine natural environment and biodiversity
🏕️ **Camping**: Overnight camping experiences
👥 **Cultural Experiences**: Learn from local T'boli communities

Best time to visit: October to May (dry season)
Altitude: Approximately 1,340 meters above sea level"""
    
    def get_pricing_response(self, message):
        # Check for specific activity pricing
        activity_prices = {}
        for activity in self.activities:
            activity_prices[activity.name.lower()] = activity.price
        
        response = "Here's pricing information for Lake Holon activities:\n\n"
        
        if self.activities:
            response += "🏔️ **Activities** (per person):\n"
            for activity in self.activities[:5]:
                response += f"   {activity.name}: ${activity.price}\n"
            response += "\n"
        
        if self.accommodations:
            response += "🏨 **Accommodations** (per night):\n"
            for accommodation in self.accommodations[:3]:
                response += f"   {accommodation.name}: ${accommodation.price_per_night}\n"
        
        response += "\nPrices may vary depending on the season and group size. Contact us for group discounts!"
        
        return response
    
    def get_weather_response(self):
        return """🌤️ **Best Time to Visit Lake Holon**

**Dry Season (October - May)**: Best time for hiking and outdoor activities
- Clear skies and good visibility
- Less rainfall, better trail conditions
- Peak tourist season: December to February

**Rainy Season (June - September)**: 
- Lush green landscapes
- Fewer crowds
- Some trails may be slippery
- Good for photography with dramatic clouds

**Temperature**: 15-25°C (59-77°F) year-round
**What to bring**: Warm clothing for evenings, rain gear, sun protection"""
    
    def get_difficulty_response(self):
        return """🥾 **Trail Difficulty Levels at Lake Holon**

**Easy**: 
- Suitable for beginners and families
- Well-marked trails
- 2-3 hours hiking time
- Minimal elevation gain

**Moderate**: 
- Some hiking experience recommended
- 4-6 hours hiking time
- Moderate elevation gain
- Some steep sections

**Hard/Challenging**: 
- Experienced hikers only
- 6-8+ hours hiking time
- Significant elevation gain
- Technical sections possible

Choose based on your fitness level and experience!"""
    
    def get_default_response(self):
        responses = [
            "I'm not sure how to help with that. Try asking me about activities, trails, guides, or accommodations at Lake Holon!",
            "Hmm, I can help you with information about Lake Holon activities, trails, guides, and more. What specific information do you need?",
            "I'd be happy to help you plan your Lake Holon adventure! Ask me about activities, pricing, booking, or general information."
        ]
        return responses[hash(len(responses)) % len(responses)]

# Initialize chatbot
chatbot = LakeHolonChatbot()

@bp.route('/')
def chatbot_page():
    return render_template('chatbot/chat.html')

@bp.route('/chat', methods=['POST'])
@login_required
def chat():
    message = request.json.get('message', '')
    user_id = current_user.id if current_user.is_authenticated else None
    
    response = chatbot.get_response(message, user_id)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/chat/suggestions')
@login_required
def chat_suggestions():
    """Get suggested questions for the chatbot"""
    suggestions = [
        "What activities are available?",
        "Tell me about the trails",
        "How much does it cost?",
        "When is the best time to visit?",
        "Do you have guides available?",
        "What accommodations are there?",
        "How do I make a booking?",
        "What's the weather like?"
    ]
    return jsonify({'suggestions': suggestions})
