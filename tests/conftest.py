import pytest
from unittest.mock import patch, MagicMock
from website import create_app

@pytest.fixture
def client():
    """
    Creates a Flask test client using the application factory.
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('openai.ChatCompletion.create')
def test_generate_recipe_success(mock_chat_completion, client):
    """
    Tests that the endpoint returns a 200 status code and the mocked recipe
    when valid ingredients are provided.
    """
    # Mock the OpenAI response
    mock_chat_completion.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(content="Mocked recipe content")
            )
        ]
    )

    response = client.post('/generate_recipe', json={'ingredients': 'chicken, tomatoes'})
    data = response.get_json()

    assert response.status_code == 200
    assert 'recipe' in data
    assert data['recipe'] == "Mocked recipe content"

def test_generate_recipe_no_ingredients(client):
    """
    Tests that the endpoint returns a 400 status code and an error message
    if no ingredients are provided.
    """
    response = client.post('/generate_recipe', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert 'recipe' in data
    assert data['recipe'] == "No ingredients provided."

@patch('openai.ChatCompletion.create')
def test_generate_recipe_exception(mock_chat_completion, client):
    """
    Tests that the endpoint gracefully handles an exception from OpenAI
    and returns the error message in the JSON response.
    """
    # Simulate an exception in the OpenAI API call
    mock_chat_completion.side_effect = Exception("Some error from OpenAI")

    response = client.post('/generate_recipe', json={'ingredients': 'chicken, tomatoes'})
    data = response.get_json()

    assert response.status_code == 200
    assert 'Error generating recipe: Some error from OpenAI' in data['recipe']
