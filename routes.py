```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User, Room, Booking, Payment
from . import db

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Invalid request'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Invalid request'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    if not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@main.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    """Get all rooms"""
    rooms = Room.query.all()
    return jsonify([{'id': room.id, 'room_number': room.room_number, 'room_type': room.room_type, 'price': room.price} for room in rooms]), 200

@main.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    user_id = get_jwt_identity()
    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    if not room_id or not check_in or not check_out:
        return jsonify({'error': 'Invalid request'}), 400

    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404

    new_booking = Booking(user_id=user_id, room_id=room_id, check_in=check_in, check_out=check_out, total_cost=room.price)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully'}), 201

@main.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    """Create a new payment"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    booking_id = data.get('booking_id')
    payment_method = data.get('payment_method')

    if not booking_id or not payment_method:
        return jsonify({'error': 'Invalid request'}), 400

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    new_payment = Payment(booking_id=booking_id, payment_method=payment_method, payment_date=datetime.now())
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'Payment created successfully'}), 201
```

###