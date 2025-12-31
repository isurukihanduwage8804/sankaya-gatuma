import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="සංඛ්‍යා ගැටුම - Ultimate", layout="wide")

# JavaScript සහ HTML Game Engine එක string එකක් විදිහට මෙතන තියෙනවා
# මෙහි f-string පාවිච්චි නොකරන නිසා syntax error එන්නේ නැහැ
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
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            text-align: center; display: none; background: rgba(15, 23, 42, 0.98);
            padding: 45px; border-radius: 35px; box-shadow: 0 0 60px rgba(56, 189, 248, 0.6);
            border: 4px solid #38bdf8; z-index: 1000;
        }
        #math-problem { font-size: 70px; margin-bottom: 25px; color: #f8fafc; text-shadow: 0 0 10px #38bdf8; }
        .ans-btn {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9); border: none; color: #0f172a;
            padding: 18px 40px; margin: 12px; border-radius: 18px; font-size: 26px; font-weight: bold;
            cursor: pointer; pointer-events: auto; transition: all 0.2s ease;
        }
        .ans-btn:hover { background: #f8fafc; transform: translateY(-3px); }
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

    const collideSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Bounce.wav');
    const winSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Get_SmallItem.wav');
    const loseSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Error.wav');

    class Ball {
        constructor() {
            this.radius = 45;
            this.x = Math.random() * (canvas.width - 100) + 50;
            this.y = Math.random() * (canvas.height - 100) + 50;
            this.dx = (Math.random() - 0.5) * 7;
            this.dy = (Math.random() - 0.5) * 7;
            this.value = Math.floor(Math.random() * 50) + 1;
            this.color = "hsl(" + (Math.random() * 360) + ", 80%, 60%)";
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 20; ctx.shadowColor = this.color;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.fillStyle = "white"; ctx.font = "bold 26px Arial"; ctx.textAlign = "center";
            ctx.fillText(this.value, this.x, this.y + 10);
            ctx.closePath();
        }
        update() {
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) this.dx *= -1;
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) this.dy *= -1;
            this.x += this.dx; this.y += this.dy;
            this.draw();
        }
    }

    let balls = [];
    for(let i=0; i<6; i++) balls.push(new Ball());

    function checkCollision() {
        if (isQuestionActive || questionsDone >= 20) return;
        for(let i=0; i<balls.length; i++) {
            for(let j=i+1; j<balls.length; j++) {
                let dist = Math.hypot(balls[i].x - balls[j].x, balls[i].y - balls[j].y);
                if (dist < balls[i].radius + balls[j].radius) {
                    balls[i].dx *= -1; balls[j].dx *= -1;
                    collideSound.currentTime = 0;
                    collideSound.play().catch(()=>{});
                    showQuestion(balls[i], balls[j]);
                    return;
                }
            }
        }
    }

    function showQuestion(b1, b2) {
        isQuestionActive = true;
        questionsDone++;
        document.getElementById('q-count').innerText = questionsDone;
        let correct = b1.value + b2.value;
        document.getElementById('math-problem').innerText = b1.value + " + " + b2.value + " = ?";
        document.getElementById('question-box').style.display = 'block';
        
        let options = [correct, correct + 5, correct - 2, correct + 10];
        options.sort(() => Math.random() - 0.5);

        let ansDiv = document.getElementById('answers');
        ansDiv.innerHTML = '';
        options.forEach(opt => {
            let btn = document.createElement('button');
            btn.className = 'ans-btn'; btn.innerText = opt;
            btn.onclick = () => selectAnswer(opt, correct);
            ansDiv.appendChild(btn);
        });
        startTimer(correct);
    }

    function startTimer(correct) {
        timerWidth =
