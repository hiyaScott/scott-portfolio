js_funcs = {
    "drawMotion": """function drawMotion() {
  const ctx = motionCtx, w = 600, h = 200;
  ctx.clearRect(0, 0, w, h);

  // Grid
  ctx.strokeStyle = 'rgba(255,107,53,0.1)';
  for (let i = 0; i <= w; i += 50) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }
  for (let i = 0; i <= h; i += 40) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(w, i); ctx.stroke(); }

  // Axis
  ctx.strokeStyle = 'rgba(255,255,255,0.3)';
  ctx.beginPath(); ctx.moveTo(40, h - 30); ctx.lineTo(w - 20, h - 30); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(40, h - 30); ctx.lineTo(40, 20); ctx.stroke();
  ctx.fillStyle = '#aaa'; ctx.font = '11px Orbitron';
  ctx.fillText('t(s)', w - 35, h - 10);
  ctx.fillText('s(m)', 15, 25);

  // s-t line (linear for constant speed)
  const pxPerS = (w - 80) / 10;
  const pxPerM = (h - 60) / 100;
  ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(40, h - 30);
  ctx.lineTo(40 + 10 * pxPerS, h - 30 - motionSpeed * 10 * pxPerM);
  ctx.stroke();
  ctx.lineWidth = 1;

  // Label
  ctx.fillStyle = '#ff6b35'; ctx.font = '13px Orbitron';
  ctx.fillText('v = ' + motionSpeed + ' m/s', 50, 40);

  // Car icon
  const carX = 40 + 5 * pxPerS;
  const carY = h - 30 - motionSpeed * 5 * pxPerM;
  ctx.fillStyle = '#ff6b35';
  ctx.fillRect(carX - 15, carY - 8, 30, 12);
  ctx.fillStyle = '#aaa';
  ctx.beginPath(); ctx.arc(carX - 10, carY + 4, 4, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(carX + 10, carY + 4, 4, 0, Math.PI * 2); ctx.fill();
}""",
    "setForceDemo": """function setForceDemo(type) { forceDemo = type; drawForce(); }""",
    "drawForce": """function drawForce() {
  const ctx = forceCtx, w = 600, h = 250;
  ctx.clearRect(0, 0, w, h);

  const boxX = w / 2, boxY = h / 2 + 30;

  // Box
  ctx.fillStyle = 'rgba(255,107,53,0.15)';
  ctx.strokeStyle = '#ff6b35';
  ctx.fillRect(boxX - 50, boxY - 30, 100, 60);
  ctx.strokeRect(boxX - 50, boxY - 30, 100, 60);

  if (forceDemo === 'size') {
    // Two arrows, different lengths
    ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(boxX - 80, boxY - 15); ctx.lineTo(boxX - 15, boxY - 15); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 15, boxY - 15); ctx.lineTo(boxX - 25, boxY - 22); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 15, boxY - 15); ctx.lineTo(boxX - 25, boxY - 8); ctx.stroke();

    ctx.strokeStyle = '#ffd166'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(boxX + 80, boxY + 15); ctx.lineTo(boxX + 15, boxY + 15); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX + 15, boxY + 15); ctx.lineTo(boxX + 25, boxY + 8); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX + 15, boxY + 15); ctx.lineTo(boxX + 25, boxY + 22); ctx.stroke();

    ctx.fillStyle = '#ff6b35'; ctx.font = '12px Orbitron';
    ctx.fillText('大力 → 大形变', 40, 40);
    ctx.fillStyle = '#ffd166';
    ctx.fillText('小力 → 小形变', w - 160, 40);
  } else if (forceDemo === 'dir') {
    // Same point, different directions
    const dirs = [{dx: -60, dy: 0, c: '#ff6b35'}, {dx: 60, dy: 0, c: '#00f0c8'}, {dx: 0, dy: -60, c: '#ffd166'}];
    dirs.forEach(d => {
      ctx.strokeStyle = d.c; ctx.lineWidth = 2;
      const len = Math.sqrt(d.dx * d.dx + d.dy * d.dy);
      const endX = boxX + d.dx, endY = boxY + d.dy;
      ctx.beginPath(); ctx.moveTo(boxX, boxY); ctx.lineTo(endX, endY); ctx.stroke();
      // Arrowhead
      const ang = Math.atan2(d.dy, d.dx);
      ctx.beginPath(); ctx.moveTo(endX, endY);
      ctx.lineTo(endX - 10 * Math.cos(ang - 0.5), endY - 10 * Math.sin(ang - 0.5));
      ctx.stroke();
      ctx.beginPath(); ctx.moveTo(endX, endY);
      ctx.lineTo(endX - 10 * Math.cos(ang + 0.5), endY - 10 * Math.sin(ang + 0.5));
      ctx.stroke();
    });
    ctx.fillStyle = '#ff6b35'; ctx.font = '12px Orbitron';
    ctx.fillText('方向不同 → 效果不同', 40, 40);
  } else {
    // Same force, different points
    ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(boxX - 80, boxY - 15); ctx.lineTo(boxX - 55, boxY - 15); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 55, boxY - 15); ctx.lineTo(boxX - 65, boxY - 22); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 55, boxY - 15); ctx.lineTo(boxX - 65, boxY - 8); ctx.stroke();

    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(boxX - 80, boxY - 50); ctx.lineTo(boxX - 55, boxY - 50); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 55, boxY - 50); ctx.lineTo(boxX - 65, boxY - 57); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(boxX - 55, boxY - 50); ctx.lineTo(boxX - 65, boxY - 43); ctx.stroke();

    ctx.fillStyle = '#ff6b35'; ctx.font = '11px Orbitron';
    ctx.fillText('推下部→滑动', 40, boxY - 10);
    ctx.fillStyle = '#00f0c8';
    ctx.fillText('推上部→翻倒', 40, boxY - 55);
  }
  ctx.lineWidth = 1;
}""",
    "drawGravity": """function drawGravity() {
  const ctx = gravCtx, w = 600, h = 280;
  ctx.clearRect(0, 0, w, h);

  const groundY = h - 60;
  const g = massVal * 9.8;

  // Ground
  ctx.fillStyle = '#0a0e1a';
  ctx.fillRect(0, groundY, w, 60);
  ctx.strokeStyle = 'rgba(255,107,53,0.2)';
  ctx.beginPath(); ctx.moveTo(0, groundY); ctx.lineTo(w, groundY); ctx.stroke();

  // Earth
  ctx.fillStyle = '#00bbf9';
  ctx.beginPath(); ctx.arc(w / 2, groundY + 80, 60, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#00bbf9'; ctx.font = '14px Orbitron';
  ctx.fillText('🌍', w / 2 - 10, groundY + 85);

  // Object
  const objY = 60 + (20 - massVal) * 5;
  const size = 20 + massVal * 2;
  ctx.fillStyle = '#ff6b35';
  ctx.fillRect(w / 2 - size / 2, objY, size, size);

  // Gravity arrow
  const arrowLen = Math.min(150, g * 0.3);
  ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(w / 2, objY + size); ctx.lineTo(w / 2, objY + size + arrowLen); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(w / 2, objY + size + arrowLen);
  ctx.lineTo(w / 2 - 8, objY + size + arrowLen - 10); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(w / 2, objY + size + arrowLen);
  ctx.lineTo(w / 2 + 8, objY + size + arrowLen - 10); ctx.stroke();
  ctx.lineWidth = 1;

  // Labels
  ctx.fillStyle = '#ff6b35'; ctx.font = '14px Orbitron';
  ctx.fillText(`G = ${g.toFixed(1)} N`, w / 2 + 20, objY + size + arrowLen / 2);
  ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
  ctx.fillText(`m = ${massVal} kg`, w / 2 - 40, objY - 10);
  ctx.fillText('g = 9.8 N/kg', 40, 30);
}""",
    "drawSpring": """function drawSpring() {
  const ctx = springCtx, w = 600, h = 250;
  ctx.clearRect(0, 0, w, h);

  const topY = 40;
  const baseLen = 80;
  const extend = springF * 12;
  const coilCount = 8;
  const coilWidth = 40;

  // Ceiling
  ctx.strokeStyle = 'rgba(255,255,255,0.3)'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(w / 2 - 60, topY); ctx.lineTo(w / 2 + 60, topY); ctx.stroke();
  ctx.lineWidth = 1;

  // Spring
  ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(w / 2, topY);
  for (let i = 0; i <= coilCount; i++) {
    const y = topY + (baseLen + extend) * i / coilCount;
    const xOffset = (i % 2 === 0) ? -coilWidth / 2 : coilWidth / 2;
    ctx.lineTo(w / 2 + xOffset, y);
  }
  ctx.stroke();
  ctx.lineWidth = 1;

  // Weight
  const weightY = topY + baseLen + extend;
  ctx.fillStyle = '#ff6b35';
  ctx.fillRect(w / 2 - 20, weightY, 40, 30);
  ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
  ctx.fillText(`${springF} N`, w / 2 + 30, weightY + 18);

  // Scale
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.beginPath(); ctx.moveTo(w / 2 + 80, topY); ctx.lineTo(w / 2 + 80, topY + 200); ctx.stroke();
  for (let i = 0; i <= 10; i++) {
    const y = topY + i * 20;
    ctx.beginPath(); ctx.moveTo(w / 2 + 75, y); ctx.lineTo(w / 2 + 85, y); ctx.stroke();
    ctx.fillStyle = '#aaa'; ctx.font = '10px Orbitron';
    ctx.fillText(i + 'N', w / 2 + 90, y + 3);
  }
}""",
    "setInertia": """function setInertia(scene) {
  inertiaScene = scene;
  const texts = {
    car: '🚗 汽车刹车：乘客向前倾倒——身体由于惯性保持原来的运动状态',
    hammer: '🔨 挥锤紧固：锤头突然停止，锤柄由于惯性继续向下运动，使锤头紧固',
    run: '🏃 跑步绊倒：脚被绊住停止，上身由于惯性继续向前，导致向前摔倒'
  };
  document.getElementById('inertiaText').textContent = texts[scene];
  drawInertia();
}""",
    "drawInertia": """function drawInertia() {
  const ctx = inertiaCtx, w = 600, h = 250;
  ctx.clearRect(0, 0, w, h);

  if (inertiaScene === 'car') {
    // Car braking, person leaning forward
    ctx.fillStyle = '#2d4a3e';
    ctx.fillRect(100, 150, 200, 40);
    ctx.fillStyle = '#ff6b35';
    ctx.beginPath(); ctx.arc(130, 190, 18, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(270, 190, 18, 0, Math.PI * 2); ctx.fill();

    // Person leaning forward
    ctx.strokeStyle = '#fcee0a'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(200, 150); ctx.lineTo(230, 120); ctx.stroke(); // body leaning
    ctx.beginPath(); ctx.arc(200, 150, 15, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.moveTo(230, 120); ctx.lineTo(245, 110); ctx.stroke(); // head
    ctx.lineWidth = 1;

    // Arrow showing motion
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(320, 130); ctx.lineTo(380, 130); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(380, 130); ctx.lineTo(370, 120); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(380, 130); ctx.lineTo(370, 140); ctx.stroke();
    ctx.lineWidth = 1;
    ctx.fillStyle = '#00f0c8'; ctx.font = '12px Orbitron';
    ctx.fillText('惯性方向', 390, 135);
  } else if (inertiaScene === 'hammer') {
    // Hammer
    ctx.strokeStyle = '#8B4513'; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(200, 100); ctx.lineTo(200, 200); ctx.stroke();
    ctx.lineWidth = 1;
    ctx.fillStyle = '#666';
    ctx.fillRect(170, 80, 60, 30);

    // Arrow
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(200, 220); ctx.lineTo(200, 180); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(200, 220); ctx.lineTo(190, 210); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(200, 220); ctx.lineTo(210, 210); ctx.stroke();
    ctx.lineWidth = 1;
    ctx.fillStyle = '#00f0c8'; ctx.font = '12px Orbitron';
    ctx.fillText('惯性向下', 210, 210);
  } else {
    // Running person tripping
    ctx.strokeStyle = '#fcee0a'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(200, 180); ctx.lineTo(260, 140); ctx.stroke(); // body falling
    ctx.beginPath(); ctx.arc(200, 180, 12, 0, Math.PI * 2); ctx.fill();
    ctx.lineWidth = 1;

    // Tripped foot
    ctx.fillStyle = '#ef476f';
    ctx.fillRect(190, 200, 20, 10);
    ctx.fillStyle = '#ef476f'; ctx.font = '12px Orbitron';
    ctx.fillText('绊住停止', 160, 225);

    // Arrow
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(280, 130); ctx.lineTo(340, 110); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(340, 110); ctx.lineTo(330, 100); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(340, 110); ctx.lineTo(330, 120); ctx.stroke();
    ctx.lineWidth = 1;
    ctx.fillStyle = '#00f0c8'; ctx.font = '12px Orbitron';
    ctx.fillText('上身惯性向前', 350, 115);
  }
}""",
    "draw": """function draw() {
    let a = aInput ? parseInt(aInput.value) : 60;
    if(aVal) aVal.textContent = a + '°';
    ctx.clearRect(0,0,500,250);
    let cx=250, cy=180, L=100;
    ctx.strokeStyle = 'var(--accent)'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+L, cy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+L*Math.cos(a*Math.PI/180), cy-L*Math.sin(a*Math.PI/180)); ctx.stroke();
    let fx = L + L*Math.cos(a*Math.PI/180), fy = -L*Math.sin(a*Math.PI/180);
    ctx.strokeStyle = 'var(--danger)'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+fx, cy+fy); ctx.stroke();
    ctx.fillStyle = 'var(--text)'; ctx.font = '12px monospace';
    ctx.fillText('F₂', cx+L+10, cy); ctx.fillText('F₁', cx+L*Math.cos(a*Math.PI/180)+10, cy-L*Math.sin(a*Math.PI/180));
    requestAnimationFrame(draw);
  }""",
}

highlights = {
    1: [
        """
      <strong>参照物</strong>：判断物体是否运动，需要选择一个标准物体作为参照。<br>
      同一物体，选择不同的参照物，运动状态可能不同。
    """,
        """
      一辆汽车在平直公路上以 20 m/s 的速度匀速行驶，5 秒钟内通过的路程是多少？
    """,
    ],
    2: [
        """
      <strong>力的两种作用效果：</strong><br>
      ① 改变物体的<strong>形状</strong>（形变）<br>
      ② 改变物体的<strong>运动状态</strong>（速度大小或方向）
    """,
        """
      用力推桌子的上部，桌子会翻倒；推下部，桌子会滑动。这说明力的作用效果与什么有关？
    """,
    ],
    3: [
        """
      <strong>重力的方向：</strong>竖直向下（指向地心）<br>
      <strong>重心：</strong>物体各部分所受重力的等效作用点。均匀规则物体的重心在几何中心。
    """,
        """
      一名中学生的质量约为 50 kg，求他受到的重力。（g取 10 N/kg）
    """,
    ],
    4: [
        """
      <strong>弹簧测力计原理：</strong>在弹性限度内，弹簧的伸长量与拉力成正比。
    """,
        """
      <strong>增大摩擦：</strong>增大压力、增大接触面粗糙程度<br>
      <strong>减小摩擦：</strong>减小压力、变滑动为滚动、加润滑油、使接触面分离
    """,
        """
      自行车轮胎上有花纹，这是通过什么方法增大摩擦？给机器加润滑油又是通过什么方法减小摩擦？
    """,
    ],
    5: [
        """
      <strong>牛顿第一定律（惯性定律）：</strong><br>
      一切物体在没有受到力的作用时，总保持静止状态或匀速直线运动状态。
    """,
        """
      公交车突然刹车时，乘客会向前倾倒，这是为什么？
    """,
    ],
    6: [
        """
      <strong>力学实验口诀：</strong><br>
      "速度等于路程除时间，重力等于质量乘g。<br>
      不受力时不改变，惯性只看质量大小。<br>
      三要素变效果变，增大摩擦粗糙加压力。"
    """,
        """
      <strong>力学实验口诀：</strong><br>
      "速度等于路程除时间，重力等于质量乘g。<br>
      不受力时不改变，惯性只看质量大小。<br>
      三要素变效果变，增大摩擦粗糙加压力。"
    """,
    ],
}
