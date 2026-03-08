# Hotel Booking System

from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Optional, Annotated


class BookingHotel(BaseModel):
    guest_name: Annotated[str, Field(max_length=50)]
    age: Annotated[int, Field(ge=18, le=100)]
    email: EmailStr
    website: AnyUrl
    room_number: int
    nights: Annotated[int, Field(gt=0)]
    price_per_night: Annotated[float, Field(gt=0)]
    amenities: Annotated[list[str], Field(max_length=5)]
    is_vip: Annotated[Optional[bool], Field(default=False)]
    contact: Dict[str, str]

def display_booking(booking: BookingHotel):
    print(f"Guest: {booking.guest_name}")
    print(f"Age: {booking.age}")
    print(f"Room: {booking.room_number}")
    print(f"Nights: {booking.nights}")
    print(f"Total Price: {booking.price_per_night * booking.nights}")
    print(f"VIP Guest: {"Yes" if booking.is_vip else "No"}")

booking_info = {
    "guest_name": "Sarah",
    "age": "28",
    "email": "sarah@gmail.com",
    "website": "https://sarah-travels.com",
    "room_number": "101",
    "nights": "3",
    "price_per_night": "150.50",
    "amenities": ["wifi", "breakfast", "parking"],
    "is_vip": None,
    "contact": {"phone": "123456", "emergency": "789012"}
}

booking1 = BookingHotel(**booking_info)
display_booking(booking1)