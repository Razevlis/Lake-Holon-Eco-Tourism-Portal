import os
from application import create_app, db
from app.models import User, Activity, Guide, Booking, Review, VisitorAnalytics, Accommodation, Trail

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Activity': Activity,
        'Guide': Guide,
        'Booking': Booking,
        'Review': Review,
        'VisitorAnalytics': VisitorAnalytics,
        'Accommodation': Accommodation,
        'Trail': Trail
    }

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
