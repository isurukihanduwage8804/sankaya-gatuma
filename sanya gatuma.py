import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="සංඛ්‍යා ගැටුම", layout="wide")

# JavaScript සහ HTML කෑල්ල මෙතනින් පටන් ගන්නවා
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Arial', sans-serif; background: #1a1a2e; color: white; }
        #gameCanvas { background: #16213e; border: 4px solid #0f3460; border-radius: 15px; }
        #ui-layer { position: absolute; top: 20px; left: 20px; pointer-events: none; }
        .score-box { font-size: 24px; color: #e94560; font-weight: bold; }
        #question-box { 
            position: absolute; top: 50%; left: 50%; 
            transform: translate(-50%, -50%); 
            text-align: center; display: none;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px; border-radius: 20px;
            backdrop-filter: blur(10px); border: 2px solid #e94560;
        }
        .ans-btn {
            background: #e94560; border: none; color: white;
            padding: 10px 25px; margin: 10px; border-radius: 10px;
            font-size: 20px; cursor: pointer; pointer-events: auto;
        }
        #timer-bar { width: 100%; height: 10px; background: #00ff00; margin-top: 10px; }
    </style>
</head>
<body>

<div id="ui-layer">
    <div class="score-box">ලකුණු: <span id="score">0</span> | ප්‍රශ්නය: <span id="q-count">0</span>/20</div>
</div>

<div id="question-box">
    <h1 id="math-problem" style="font-size: 50px; margin: 0;"></h1>
    <div id="timer-bar"></div>
    <div id="answers"></div>
</div>

<canvas id="gameCanvas"></canvas>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let score = 0;
    let questionsDone = 0;
    let isQuestionActive = false;
    let timerWidth = 100;
    let timerInterval;

    // Sounds (නොමිලේ ලබාගත හැකි සරල සද්ද)
    const collideSound = new Audio('https://actions.google.com/sounds/v1/foley/glass_break.ogg');
    const winSound = new Audio('https://actions.google.com/sounds/v1/cartoon/clime_up_the_ladder.ogg');
    const loseSound = new Audio('https://actions.google.com/sounds/v1/alarms/alarm_clock_beeping.ogg');

    class Ball {
        constructor(id) {
            this.id = id;
            this.radius = 40;
            this.x = Math.random() * (canvas.width - this.radius * 2) + this.radius;
            this.y = Math.random() * (canvas.height - this.radius * 2) + this.radius;
            this.dx = (Math.random() - 0.5) * 6;
            this.dy = (Math.random() - 0.5) * 6;
            this.value = Math.floor(Math.random() * 50) + 1;
            this.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            ctx.fillStyle = "white";
            ctx.font = "bold 20px Arial";
            ctx.textAlign = "center";
            ctx.fillText(this.value, this.x, this.y + 7);
            ctx.closePath();
        }

        update() {
            if (this.x + this.radius > canvas.width || this.x - this.radius < 0) this.dx = -this.dx;
            if (this.y + this.radius > canvas.height || this.y - this.radius < 0) this.dy = -this.dy;
            this.x += this.dx;
            this.y += this.dy;
            this.draw();
        }
    }

    let balls = [];
    for(let i=0; i<6; i++) balls.push(new Ball(i));

    function checkCollision() {
        if (isQuestionActive) return;
        for(let i=0; i<balls.length; i++) {
            for(let j=i+1; j<balls.length; j++) {
                let dist = Math.hypot(balls[i].x - balls[j].x, balls[i].y - balls[j].y);
                if (dist < balls[i].radius + balls[j].radius) {
                    collideSound.play();
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
        
        let options = [correct, correct + 5, correct - 3, Math.floor(Math.random()*100)];
        options.sort(() => Math.random() - 0.5);

        let ansDiv = document.getElementById('answers');
        ansDiv.innerHTML = '';
        options.forEach(opt => {
            let btn = document.createElement('button');
            btn.className = 'ans-btn';
            btn.innerText = opt;
            btn.onclick = () => selectAnswer(opt, correct);
            ansDiv.appendChild(btn);
        });

        startTimer(correct);
    }

    function startTimer(correct) {
        timerWidth = 100;
        document.getElementById('timer-bar').style.width = '100%';
        timerInterval = setInterval(() => {
            timerWidth -= 1;
            document.getElementById('timer-bar').style.width = timerWidth + '%';
            if (timerWidth <= 0) {
                clearInterval(timerInterval);
                selectAnswer(-1, correct); // Time Out
            }
        }, 100);
    }

    function selectAnswer(selected, correct) {
        clearInterval(timerInterval);
        document.getElementById('question-box').style.display = 'none';
        
        if (selected === correct) {
            score += 10;
            winSound.play();
        } else {
            score -= 5;
            loseSound.play();
        }
        
        document.getElementById('score').innerText = score;
        
        if (questionsDone >= 20) {
            alert("Game Over! ඔයාගේ ලකුණු: " + score);
            location.reload();
        } else {
            setTimeout(() => { isQuestionActive = false; }, 1000);
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        balls.forEach(ball => ball.update());
        checkCollision();
        requestAnimationFrame(animate);
    }

    animate();
</script>
</body>
</html>
"""

# Streamlit ඇතුළේ HTML එක පෙන්වීම
components.html(game_html, height=700)

st.write("### 🕹️ සෙල්ලම් කරන විදිහ:")
st.write("බෝල දෙකක් හැප්පුනාම ප්‍රශ්නයක් එනවා. තත්පර 10ක් ඇතුළත නිවැරදි පිළිතුර ක්ලික් කරන්න. ලකුණු 10ක් ලැබෙනවා, වැරදුනොත් 5ක් අඩුවෙනවා!")
