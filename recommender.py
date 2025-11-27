import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from mood import get_mood_preferences
from nutrition import get_nutrition, clean_ingredient


class RecipeRecommender:

    def __init__(self, csv_path="indian_food.csv"):
        self.df = pd.read_csv(csv_path)
        self.df["ingredients"] = self.df["ingredients"].astype(str).str.lower()

        # Build TF-IDF vector model
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["ingredients"])

    def nutrition_filter(self, recipe, rules):
        """Apply calorie + protein filtering."""
        first_ing = recipe["ingredients"].split(",")[0].strip()
        clean_ing = clean_ingredient(first_ing)

        nutri = get_nutrition(clean_ing)

        if nutri is None:
            return True

        if "max_cal" in rules and nutri["calories"] > rules["max_cal"]:
            return False

        if "min_protein" in rules and nutri["protein"] < rules["min_protein"]:
            return False

        return True

    def recommend(self, mood, topn=10):
        """Generate final recipe recommendations."""
        prefs = get_mood_preferences(mood)
        keywords = prefs["keywords"]

        # Compute similarity
        mood_vec = self.vectorizer.transform([keywords])
        similarity = cosine_similarity(mood_vec, self.tfidf_matrix).flatten()

        self.df["score"] = similarity

        selected = []

        # Select top N recipes that match nutrition rules
        for _, row in self.df.sort_values("score", ascending=False).iterrows():
            if self.nutrition_filter(row, prefs["nutrition"]):
                selected.append(row)
            if len(selected) == topn:
                break

        out_df = pd.DataFrame(selected)[["name", "ingredients", "diet", "region", "score"]]

        # Add NUTRITION COLUMNS
        calories = []
        proteins = []
        fats = []
        carbs = []
        ing_used = []

        for ing in out_df["ingredients"]:
            first_ing = clean_ingredient(ing.split(",")[0])
            ing_used.append(first_ing)

            nutri = get_nutrition(first_ing)

            if nutri:
                calories.append(nutri["calories"])
                proteins.append(nutri["protein"])
                fats.append(nutri["fat"])
                carbs.append(nutri["carbs"])
            else:
                calories.append(0)
                proteins.append(0)
                fats.append(0)
                carbs.append(0)

        out_df["nutrition_ingredient"] = ing_used
        out_df["calories"] = calories
        out_df["protein"] = proteins
        out_df["fat"] = fats
        out_df["carbs"] = carbs

        return out_df