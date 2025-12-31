import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="සංඛ්‍යා ගැටුම", layout="wide")

# index.html file එක කියවීම
def load_game():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Game එක display කිරීම
try:
    game_code = load_game()
    components.html(game_code, height=800)
except Exception as e:
    st.error(f"Error loading game: {e}")

st.info("ප්‍රශ්න 20ක් තියෙනවා. එක ප්‍රශ්නයකට තත්පර 15ක් ලැබෙනවා. සද්ද ඇහෙන්න එක පාරක් Click කරන්න.")
