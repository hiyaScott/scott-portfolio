css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
  --bg: #06080f;
  --panel: rgba(10, 14, 26, 0.9);
  --accent: #ff6b35;
  --accent2: #ffcc00;
  --danger: #ef476f;
  --warning: #ffd166;
  --success: #06d6a0;
  --grid: rgba(255, 107, 53, 0.08);
  --text: #c0c8d8;
  --text-dim: #586070;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Scanlines */
body::before {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
  pointer-events: none;
  z-index: 5;
}

/* HUD Grid */
#hud-grid {
  position: fixed; inset: 0;
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 1;
}

/* Corners */
.corner-tl, .corner-tr, .corner-bl, .corner-br {
  position: fixed; width: 80px; height: 80px; z-index: 2; pointer-events: none;
}
.corner-tl { top: 10px; left: 10px; border-top: 2px solid var(--accent); border-left: 2px solid var(--accent); }
.corner-tr { top: 10px; right: 10px; border-top: 2px solid var(--accent); border-right: 2px solid var(--accent); }
.corner-bl { bottom: 10px; left: 10px; border-bottom: 2px solid var(--accent); border-left: 2px solid var(--accent); }
.corner-br { bottom: 10px; right: 10px; border-bottom: 2px solid var(--accent); border-right: 2px solid var(--accent); }

#app { position: relative; z-index: 10; max-width: 900px; margin: 0 auto; padding: 40px 20px; }

.title-bar {
  text-align: center;
  border-bottom: 1px solid var(--accent);
  padding-bottom: 16px;
  margin-bottom: 24px;
}
.title-bar h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: 32px; letter-spacing: 4px;
  color: var(--accent);
  text-shadow: 0 0 20px var(--accent), 0 0 40px var(--accent);
}
.title-bar .subtitle {
  font-size: 14px; color: var(--text-dim);
  margin-top: 8px; letter-spacing: 2px;
}

.progress-bar {
  display: flex; gap: 6px;
  margin-bottom: 32px;
  justify-content: center;
}
.progress-seg {
  width: 60px; height: 4px;
  background: rgba(88,96,112,0.3);
  border-radius: 2px;
  transition: all 0.3s;
}
.progress-seg.active { background: var(--accent); box-shadow: 0 0 10px var(--accent); }
.progress-seg.done { background: var(--success); }

.card {
  background: var(--panel);
  border: 1px solid rgba(255,107,53,0.2);
  border-radius: 8px;
  padding: 28px;
  margin-bottom: 20px;
  position: relative;
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(255,107,53,0.15);
  padding-bottom: 12px; margin-bottom: 16px;
}
.card-header h2 {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px; color: var(--accent); margin: 0;
}
.chapter-num { font-size: 13px; color: var(--text-dim); letter-spacing: 1px; }
.card.hidden { display: none; }

.concept-box {
  background: rgba(6,8,15,0.6);
  border-left: 3px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 16px;
  margin: 16px 0;
}
.concept-box .label {
  font-size: 11px; color: var(--accent);
  text-transform: uppercase; letter-spacing: 2px;
  margin-bottom: 8px; font-family: 'Orbitron', sans-serif;
}
.concept-box p { margin: 8px 0; line-height: 1.7; }

.formula {
  background: rgba(255,107,53,0.05);
  border: 1px solid rgba(255,107,53,0.2);
  border-radius: 6px;
  padding: 12px 16px;
  margin: 12px 0;
  font-size: 16px;
  color: var(--accent);
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 10px rgba(255,107,53,0.3);
}

.example-list { margin: 20px 0; }
.example-item {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,107,53,0.15);
  border-radius: 6px;
  margin-bottom: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}
.example-item:hover { border-color: rgba(255,107,53,0.3); }
.example-item .q {
  padding: 12px 16px;
  font-size: 14px;
  display: flex; align-items: center; gap: 8px;
}
.example-item .a {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
  padding: 0 16px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-dim);
}
.example-item.expanded .a {
  max-height: 500px;
  padding: 12px 16px 16px;
  border-top: 1px solid rgba(255,107,53,0.1);
}
.example-item .step {
  margin-top: 8px;
  padding: 8px 12px;
  background: rgba(255,107,53,0.05);
  border-left: 2px solid var(--accent);
  border-radius: 0 4px 4px 0;
  font-size: 12px;
  color: var(--text-dim);
}

.quiz-box {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,107,53,0.15);
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}
.quiz-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  color: var(--accent);
  margin-bottom: 16px;
  letter-spacing: 1px;
}
.quiz-question { margin-bottom: 12px; font-size: 14px; line-height: 1.6; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-btn {
  text-align: left;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,107,53,0.2);
  color: var(--text);
  padding: 12px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  font-size: 14px;
}
.quiz-btn:hover { border-color: var(--accent); background: rgba(255,107,53,0.05); }
.quiz-btn.correct { border-color: var(--success); background: rgba(6,214,160,0.1); }
.quiz-btn.wrong { border-color: var(--danger); background: rgba(239,71,111,0.1); }
.quiz-btn:disabled { opacity: 0.6; cursor: default; }
.quiz-feedback {
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  min-height: 20px;
}

.anim-area {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,107,53,0.15);
  border-radius: 8px;
  padding: 20px;
  margin: 16px 0;
}

.btn {
  background: var(--accent);
  color: #000;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  margin: 4px;
  text-decoration: none;
  display: inline-block;
}
.btn:hover { box-shadow: 0 0 20px var(--accent); transform: translateY(-1px); }
.btn-ghost {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
}
.btn-ghost:hover { background: rgba(255,107,53,0.1); }
.btn-warn {
  background: rgba(255,209,102,0.1);
  border: 1px solid var(--warning);
  color: var(--warning);
}
.btn-warn:hover { background: rgba(255,209,102,0.2); box-shadow: 0 0 20px var(--warning); }

.btn-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  gap: 12px;
}

.footer-note {
  text-align: center;
  padding: 20px 0;
  color: var(--text-dim);
  font-size: 12px;
  letter-spacing: 1px;
}

/* Slider controls */
.slider-control {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 0;
}
.slider-control input[type="range"] {
  flex: 1;
  accent-color: var(--accent);
}
.slider-control label {
  min-width: 100px;
  font-size: 14px;
}
.slider-control .value {
  min-width: 60px;
  text-align: right;
  color: var(--accent);
}

.demo-box {
  background: rgba(0,0,0,0.3);
  border: 1px dashed rgba(255,107,53,0.3);
  border-radius: 8px;
  padding: 20px;
  margin: 16px 0;
  text-align: center;
}

.formula-box {
  background: rgba(6,8,15,0.8);
  border: 1px solid var(--accent);
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  text-align: center;
  font-size: 16px;
  color: var(--accent);
  text-shadow: 0 0 10px rgba(255,107,53,0.3);
}

canvas { max-width: 100%; border-radius: 6px; display: block; margin: 0 auto; }

@media (max-width: 768px) {
  .title-bar h1 { font-size: 22px; }
  .card { padding: 18px; }
  .progress-seg { width: 50px; }
}
@media (max-width: 480px) {
  .title-bar h1 { font-size: 18px; letter-spacing: 2px; }
  .card { padding: 14px; }
  .card-header h2 { font-size: 16px; }
  .progress-seg { width: 36px; }
}
</style>"""
unit1 = """<div class="card" id="ch1">
  <div class="card-header">
    <h2>🏃 机械运动</h2>
    <span class="chapter-num">第 1 / 6 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>参照物</strong>：判断物体是否运动，需要选择一个标准物体作为参照。</p>
    <p>同一物体，选择不同的参照物，运动状态可能不同。</p>
    <div class="formula">速度 v = s / t （路程 ÷ 时间）</div>
    <p><strong>匀速直线运动</strong>：速度不变，沿直线运动。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🎯 运动与参照物演示</div>
    <div class="demo-box">
      <canvas id="motionCanvas" width="600" height="250"></canvas>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">观察：选择不同参照物，同一物体的运动状态描述不同</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：坐在行驶的汽车里，以汽车为参照物，路边的树是运动还是静止的？</div>
      <div class="a">
        <strong>解：</strong>以汽车为参照物，路边的树相对于汽车的位置在不断变化，所以树是<strong style="color:var(--success)">运动</strong>的。
        <div class="step">判断运动：看物体相对于参照物的位置是否改变。位置变了 → 运动；位置没变 → 静止。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：小明骑自行车上学，速度为 5 m/s，家到学校距离 1500 m，求所需时间。</div>
      <div class="a">
        <strong>解：</strong>v = s / t → t = s / v = 1500 / 5 = <strong style="color:var(--success)">300 s = 5 分钟</strong>
        <div class="step">速度公式 v = s/t 变形：t = s/v，s = v×t。注意单位统一！</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：甲乙两车从同一地点出发，甲车速度 60 km/h，乙车速度 90 km/h，同向行驶。2 小时后两车相距多远？</div>
      <div class="a">
        <strong>解：</strong>甲车行驶距离：s₁ = 60 × 2 = 120 km<br>
        乙车行驶距离：s₂ = 90 × 2 = 180 km<br>
        相距：Δs = s₂ - s₁ = 180 - 120 = <strong style="color:var(--success)">60 km</strong>
        <div class="step">同向行驶：距离差 = 速度差 × 时间 = (90-60) × 2 = 60 km。可以直接用相对速度计算。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch1-quiz">
    <div class="quiz-title">🎯 随堂测验 — 机械运动</div>
    <div class="quiz-question"><strong>Q1.</strong> 坐在行驶汽车中的乘客，说自己是静止的，他选择的参照物是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！以汽车为参照物，乘客位置不变，是静止的。')">A. 汽车</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。以路边树木为参照物，乘客位置在变，是运动的。')">B. 路边树木</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。以地面为参照物，乘客位置在变，是运动的。')">C. 地面</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 一辆汽车以 20 m/s 的速度匀速行驶，10 秒内通过的路程是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。s = v×t = 20×10 = 200 m。')">A. 2 m</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！s = v×t = 20×10 = 200 m。')">B. 200 m</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。s = v×t = 20×10 = 200 m。')">C. 20 m</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 下列说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。运动和静止是相对的，取决于参照物。')">A. 运动是绝对的，静止是相对的</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！同一物体选择不同参照物，运动状态可能不同。')">B. 同一物体，选择不同参照物，运动状态可能不同</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。任何物体都可以被选作参照物。')">C. 只有静止的物体才能作参照物</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn" onclick="goTo(2)">下一单元 →</button>
  </div>
</div>"""
