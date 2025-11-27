import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CALORIE_NINJA_KEY")   # <-- your key from .env


def clean_ingredient(text):
    """Cleans and normalizes ingredients for CalorieNinjas."""
    if not text:
        return None

    text = text.lower().strip()
    text = text.split(",")[0]

    mapping = {
        "chana dal": "chana dal",
        "urad dal": "urad dal",
        "moong dal": "moong dal",
        "toor dal": "toor dal",
        "dal": "lentils",
        "rajma": "rajma beans",
        "chole": "chickpeas",

        "paneer": "paneer",
        "curd": "yogurt",
        "dahi": "yogurt",

        "aloo": "potato",
        "gobi": "cauliflower",
        "baingan": "eggplant",
        "brinjal": "eggplant",
        "bhindi": "okra",

        "fresh coconut": "coconut",
        "coconut milk": "coconut milk",

        "gram flour": "gram flour",
        "besan": "chickpea flour",

        "cashews": "cashews",
        "green peas": "peas",
        "sweet potato": "sweet potato",

        "ginger": "ginger",
        "garlic": "garlic",

        "green chilli": "green chilli",
        "green chillies": "green chilli",
    }

    for k, v in mapping.items():
        if k in text:
            return v

    return text


def get_nutrition(ingredient):
    """Fetch nutrition using CalorieNinjas API."""
    ingredient = clean_ingredient(ingredient)

    print("\n=== CALLING CALORIE NINJAS ===")
    print("Ingredient:", ingredient)

    url = f"https://api.calorieninjas.com/v1/nutrition?query={ingredient}"

    headers = {"X-Api-Key": API_KEY}

    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)
    print("Raw:", response.text)

    if response.status_code != 200:
        return None

    data = response.json()

    if "items" not in data or len(data["items"]) == 0:
        return None

    item = data["items"][0]  # Best match

    return {
        "calories": item.get("calories", 0),
        "protein": item.get("protein_g", 0),
        "carbs": item.get("carbohydrates_total_g", 0),
        "fat": item.get("fat_total_g", 0)
    }