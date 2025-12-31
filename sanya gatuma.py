import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="සංඛ්‍යා ගැටුම - Ultimate", layout="wide")

# JavaScript සහ HTML Game Engine
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Arial', sans-serif; background: #020617; color: white; }
        #gameCanvas { background: radial-gradient(circle, #1e293b 0%, #020617 100%); display: block; cursor: crosshair; }
        
        #ui-layer { 
            position: absolute; top: 15px; left: 15px; pointer-events: none; 
            background: rgba(15, 23, 42, 0.8); padding: 12px 20px; border-radius: 12px;
            border: 1px solid #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }
        
        .score-box { font-size: 20px; color: #38bdf8; font-weight: bold; letter-spacing: 1px; }

        #question-box { 
            position: absolute; top: 50%; left: 50%; 
            transform: translate(-50%, -50%); 
            text-align: center; display: none;
            background: rgba(15, 23, 42, 0.98);
            padding: 45px; border-radius: 35px;
            box-shadow: 0 0 60px rgba(56, 189, 248, 0.6);
            border: 4px solid #38bdf8; z-index: 1000;
        }

        #math-problem { font-size: 70px; margin-bottom: 25px; color: #f8fafc; text-shadow: 0 0 10px #38bdf8; }

        .ans-btn {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9); border: none; color: #0f172a;
            padding: 18px 40px; margin: 12px; border-radius: 18px;
            font-size: 26px; font-weight: bold; cursor: pointer; 
            pointer-events: auto; transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .ans-btn:hover { background: #f8fafc; transform: translateY(-3px); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4); }

        #timer-container { width: 100%; height: 18px; background: #1e293b; border-radius: 20px; margin-top: 25px; overflow: hidden; border: 2px solid #334155; }
        #timer-bar { width: 100%; height: 100%; background: #22c55e; transition: width 0.1s linear; }
    </style>
</head>
<body>

<div id="ui-layer">
    <div class="score-box">⭐ SCORE: <span id="score">0</span> | 🎯 Q: <span id="q-count">0</span>/20</div>
</div>

<div id="question-box">
    <div id="math-problem"></div>
    <div id="answers"></div>
    <div id="timer-container"><div id="timer-bar"></div></div>
    <p style="margin-top: 15px; color: #94a3b8; font-weight: bold;">ඔයාට තත්පර 15ක් තියෙනවා!</p>
</div>

<canvas id="gameCanvas"></canvas>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();

    let score = 0, questionsDone = 0, isQuestionActive = false;
    let timerWidth = 100, timerInterval;

    // --- SOUNDS (Zelda themed for high quality) ---
    const collideSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Bounce.wav');
    const winSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Get_SmallItem.wav');
    const loseSound = new Audio('
