import streamlit as st
import pandas as pd
import altair as alt
from recommender import RecipeRecommender
from mood import get_mood_preferences
from nutrition import get_nutrition

# ------------------------------
# STREAMLIT CONFIG
# ------------------------------
st.set_page_config(
    page_title="Mood2Meal AI",
    page_icon="🍽️",
    layout="wide",
)

st.title("🍽️ Mood2Meal – AI Recipe Recommender")

st.markdown("""
Welcome! This AI recommends Indian recipes based on your mood and provides a nutrition breakdown of each dish.
""")

# ------------------------------
# LOAD ENGINE
# ------------------------------
try:
    engine = RecipeRecommender("indian_food.csv")
except Exception as e:
    st.error(f"❌ Could not load dataset: {e}")
    st.stop()

# ------------------------------
# MOOD SELECTION
# ------------------------------
mood = st.selectbox(
    "How are you feeling today?",
    ["happy", "sad", "stressed", "tired", "angry", "sleepy", "energetic"]
)

if not mood:
    st.stop()

st.success(f"Showing recipe recommendations for **{mood.upper()}** mood")

# ------------------------------
# GET RECOMMENDATIONS (Safe)
# ------------------------------
try:
    results = engine.recommend(mood)
except Exception as e:
    st.error(f"❌ Error generating recommendations: {e}")
    st.stop()

if results is None or len(results) == 0:
    st.warning("⚠️ No recipes found for this mood.")
    st.stop()

# ------------------------------
# SHOW TABLE
# ------------------------------
st.subheader("📋 Recommended Recipes")
st.dataframe(results, use_container_width=True)

# ------------------------------
# PROTEIN CHART (NO NEGATIVE AXIS)
# ------------------------------
st.subheader("🥗 Protein Comparison Chart")

if "protein" in results.columns:
    # Make sure values are numeric
    results["protein"] = results["protein"].astype(float)

    chart_df = pd.DataFrame({
        "Recipe": results["name"],
        "Protein (g)": results["protein"]
    })

    # BUILD ALTAR CHART
    protein_chart = (
        alt.Chart(chart_df)
        .mark_bar(color="#4CAF50")
        .encode(
            x=alt.X("Recipe:N", sort=None, title="Recipe"),
            y=alt.Y(
                "Protein (g):Q",
                title="Protein (g)",
                scale=alt.Scale(
                    domain=[0, float(chart_df["Protein (g)"].max())]  # Force zero start
                ),
                axis=alt.Axis(tickMinStep=1)
            ),
            tooltip=["Recipe", "Protein (g)"]
        )
        .properties(height=400)
    )

    st.altair_chart(protein_chart, use_container_width=True)

# ------------------------------
# DETAILED NUTRITION PANEL
# ------------------------------
st.subheader("🍱 Detailed Nutrition Panel")

for _, row in results.iterrows():
    name = row["name"]
    ingredient = row["nutrition_ingredient"]

    st.markdown(f"<h3>{name}</h3>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <p style="font-size: 15px;">
            <b>Ingredient Used:</b> {ingredient.title()}
        </p>

        <p style="font-size: 15px;">
            <b>Calories:</b> {row['calories']} kcal  
            | <b>Protein:</b> {row['protein']} g  
            | <b>Fat:</b> {row['fat']} g  
            | <b>Carbs:</b> {row['carbs']} g
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)