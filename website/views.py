import os
import openai
import logging
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

travel_bp = Blueprint('travel_bp', __name__)
logging.basicConfig(level=logging.DEBUG)

@travel_bp.route('/')
def index():
    return render_template('index.html')

@travel_bp.route('/plan_trip', methods=['POST'])
def plan_trip():
    data = request.get_json()
    logging.debug(f"Received request data: {data}")
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    interests = data.get('interests', 'general interests')
    budget = data.get('budget', 'moderate budget')

    if not destination or not start_date or not end_date:
        return jsonify({'itinerary': "Please provide a destination and valid start/end dates."}), 400

    # Build a chat-style prompt for generating a travel itinerary.
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI travel assistant. Your task is to generate a detailed, multi-day travel itinerary "
                "that includes recommended activities, restaurants, and travel tips based on user input."
            )
        },
        {
            "role": "user",
            "content": (
                f"Plan a trip to {destination} from {start_date} to {end_date}. "
                f"My interests include {interests}. My budget is {budget}. "
                "Please provide a day-by-day itinerary with recommendations for activities, dining, and travel tips."
            )
        }
    ]
    logging.debug(f"Constructed messages: {messages}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )
        itinerary = response.choices[0].message.content.strip()
        logging.debug(f"Generated itinerary: {itinerary}")
    except Exception as e:
        logging.exception("OpenAI API call failed")
        itinerary = f"Error generating itinerary: {str(e)}"

    return jsonify({'itinerary': itinerary})
