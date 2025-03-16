import os
import openai
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({'recipe': "No ingredients provided."}), 400

    # Build the chat-style prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that generates creative and tasty recipes."
        },
        {
            "role": "user",
            "content": f"Suggest a creative and tasty recipe using the following ingredients: {ingredients}."
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",  # The chat model you want to use
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        # For a chat model, the response text is in response.choices[0].message.content
        recipe = response.choices[0].message.content.strip()
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return jsonify({'recipe': recipe})
