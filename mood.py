def get_mood_preferences(mood: str):
    mood = mood.lower().strip()

    mood_map = {
        "happy": {
            "keywords": "sweet fruity colorful fresh light",
            "nutrition": {"max_cal": 700}
        },
        "sad": {
            "keywords": "warm spicy rich creamy comforting",
            "nutrition": {"max_cal": 1000}
        },
        "tired": {
            "keywords": "protein rice dal curry energy",
            "nutrition": {"min_protein": 10}
        },
        "stressed": {
            "keywords": "cool refreshing yogurt mint calm light",
            "nutrition": {"max_cal": 600}
        },
        "energetic": {
            "keywords": "fresh protein salad bowl crisp healthy",
            "nutrition": {"min_protein": 12}
        }
    }

    return mood_map[mood]