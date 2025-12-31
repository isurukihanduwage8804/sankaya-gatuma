import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="සංඛ්‍යා ගැටුම - සවුන්ඩ් ෆික්ස්", layout="wide")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #0f172a; color: white; font-family: sans-serif; }
        #gameCanvas { display: block; background: #1e293b; cursor: pointer; }
        #ui-layer { position: absolute; top: 10px; left: 10px; pointer-events: none; background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; }
        #question-box { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            background: #0f172a; padding: 30px; border-radius: 20px; border: 3px solid #38bdf8;
            text-align: center; display: none; z-index: 1000;
        }
        .ans-btn { background: #38bdf8; border: none; padding: 10px 20px; margin: 5px; border-radius: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

<div id="ui-layer">⭐ ලකුණු: <span id="score">0</span> | ප්‍රශ්නය: <span id="q-count">0</span>/20</div>

<div id="question-box">
    <h1 id="math-problem"></h1>
    <div id="answers"></div>
</div>

<canvas id="gameCanvas"></canvas>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // --- මාරු කළ සවුන්ඩ් ලින්ක්ස් (Direct MP3) ---
    const collideSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Bounce.wav');
    const winSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Get_SmallItem.wav');
    const loseSound = new Audio('https://noproblo.dayjo.org/ZeldaSounds/OOT/OOT_Bose_Hit.wav');

    // සවුන්ඩ් එක ලෝඩ් කරන්න Force කිරීම
    collideSound.load(); winSound.load(); loseSound.load();

    let score = 0, questionsDone = 0, isQuestionActive = false;

    class Ball {
        constructor() {
            this.radius = 40;
            this.x = Math.random() * (canvas.width - 80) + 40;
            this.y = Math.random() * (canvas.height - 80) + 40;
            this.dx = (Math.random() - 0.5) * 6;
            this.dy = (Math.random() - 0.5) * 6;
            this.value = Math.floor(Math.random() * 20) + 1;
            this.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
        }
        draw() {
            ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color; ctx.fill();
            ctx.fillStyle = "white"; ctx.font = "20px Arial"; ctx.textAlign = "center";
            ctx.fillText(this.value, this.x, this.y + 7); ctx.closePath();
        }
        update() {
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) this.dx *= -1;
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) this.dy *= -1;
            this.x += this.dx; this.y += this.dy; this.draw();
        }
    }

    let balls = [];
    for(let i=0; i<6; i++) balls.push(new Ball());

    function checkCollision() {
        if (isQuestionActive) return;
        for(let i=0; i<balls.length; i++) {
            for(let j=i+1; j<balls.length; j++) {
                let d = Math.hypot(balls[i].x - balls[j].x, balls[i].y - balls[j].y);
                if (d < balls[i].radius + balls[j].radius) {
                    // බෝල මාරු කිරීම
                    balls[i].dx *= -1; balls[j].dx *= -1;
                    
                    // සවුන්ඩ් එක ප්ලේ කිරීම
                    collideSound.currentTime = 0;
                    collideSound.play().catch(() => console.log("Click the screen first!"));
                    
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
        document.getElementById('math-problem').innerText = `${b1.value} + ${b2.value} = ?`;
        document.getElementById('question-box').style.display = 'block';
        
        let options = [correct, correct + 2, correct - 1, correct + 5];
        options.sort(() => Math.random() - 0.5);
        let ansDiv = document.getElementById('answers');
        ansDiv.innerHTML = '';
        options.forEach(opt => {
            let btn = document.createElement('button');
            btn.className = 'ans-btn'; btn.innerText = opt;
            btn.onclick = () => {
                document.getElementById('question-box').style.display = 'none';
                if(opt === correct) { score += 10; winSound.play(); } 
                else { score -= 5; loseSound.play(); }
                document.getElementById('score').innerText = score;
                setTimeout(() => { isQuestionActive = false; }, 1000);
            };
            ansDiv.appendChild(btn);
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        balls.forEach(b => b.update());
        checkCollision();
        requestAnimationFrame(animate);
    }
    animate();
</script>
</body>
</html>
"""

components.html(game_html, height=600)

st.warning("⚠️ වැදගත්: ගේම් එක පටන් ගත් පසු සද්ද ඇසෙන්නට නම් එක පාරක් ගේම් එක මත (බෝල පාවෙන තැන) Click කරන්න.")
