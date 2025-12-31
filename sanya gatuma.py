import streamlit as st
import streamlit.components.v1 as components

# Page එක Wide එකට සැකසීම
st.set_page_config(page_title="සංඛ්‍යා ගැටුම - PRO", layout="wide")

# JavaScript සහ HTML Game Engine එක
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: white; }
        #gameCanvas { background: radial-gradient(circle, #1e293b 0%, #0f172a 100%); display: block; }
        
        #ui-layer { 
            position: absolute; top: 20px; left: 20px; pointer-events: none; 
            background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px;
        }
        
        .score-box { font-size: 22px; color: #38bdf8; font-weight: bold; }

        #question-box { 
            position: absolute; top: 50%; left: 50%; 
            transform: translate(-50%, -50%); 
            text-align: center; display: none;
            background: rgba(15, 23, 42, 0.95);
            padding: 40px; border-radius: 30px;
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.5);
            border: 3px solid #38bdf8; z-index: 100;
        }

        #math-problem { font-size: 60px; margin-bottom: 20px; color: #f8fafc; }

        .ans-btn {
            background: #38bdf8; border: none; color: #0f172a;
            padding: 15px 35px; margin: 10px; border-radius: 15px;
            font-size: 24px; font-weight: bold; cursor: pointer; 
            pointer-events: auto; transition: 0.2s;
        }
        .ans-btn:hover { background: #7dd3fc; transform: scale(1.05); }

        #timer-container { width: 100%; height: 15px; background: #334155; border-radius: 10px; margin-top: 20px; overflow: hidden; }
        #timer-bar { width:
