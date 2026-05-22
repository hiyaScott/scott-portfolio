js_funcs = {
    "drawShadow": """function drawShadow() {
  const ctx = shadowCtx, w = 600, h = 250;
  ctx.clearRect(0, 0, w, h);

  // Ground
  ctx.fillStyle = '#0a0e1a';
  ctx.fillRect(0, h - 40, w, 40);
  ctx.strokeStyle = 'rgba(252,238,10,0.2)';
  ctx.beginPath(); ctx.moveTo(0, h - 40); ctx.lineTo(w, h - 40); ctx.stroke();

  // Sun
  const sunX = w / 2 - 150 * Math.cos(sunAngle * Math.PI / 180);
  const sunY = h - 40 - 150 * Math.sin(sunAngle * Math.PI / 180);
  ctx.fillStyle = '#fcee0a';
  ctx.shadowColor = '#fcee0a'; ctx.shadowBlur = 30;
  ctx.beginPath(); ctx.arc(sunX, sunY, 18, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;

  // Tree
  const treeX = w / 2, treeBase = h - 40;
  const treeH = 100, treeW = 20;
  ctx.fillStyle = '#2d4a3e';
  ctx.fillRect(treeX - treeW / 2, treeBase - treeH, treeW, treeH);
  ctx.fillStyle = '#3d6a4e';
  ctx.beginPath(); ctx.arc(treeX, treeBase - treeH, 30, 0, Math.PI * 2); ctx.fill();

  // Shadow
  const shadowLen = treeH / Math.tan(sunAngle * Math.PI / 180);
  ctx.fillStyle = 'rgba(0,0,0,0.5)';
  ctx.beginPath();
  ctx.moveTo(treeX + treeW / 2, treeBase);
  ctx.lineTo(treeX + treeW / 2 + shadowLen, treeBase);
  ctx.lineTo(treeX - treeW / 2 + shadowLen * 0.8, treeBase);
  ctx.lineTo(treeX - treeW / 2, treeBase);
  ctx.closePath(); ctx.fill();

  // Light rays
  ctx.strokeStyle = 'rgba(252,238,10,0.4)';
  ctx.setLineDash([5, 5]);
  ctx.beginPath(); ctx.moveTo(sunX, sunY); ctx.lineTo(treeX - treeW / 2, treeBase - treeH); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(sunX, sunY); ctx.lineTo(treeX + treeW / 2, treeBase - treeH); ctx.stroke();
  ctx.setLineDash([]);

  // Shadow length text
  ctx.fillStyle = '#fcee0a';
  ctx.font = '14px Share Tech Mono';
  ctx.fillText(`影长 ≈ ${shadowLen.toFixed(1)} px`, treeX + 20, treeBase + 20);
}""",
    "setEclipse": """function setEclipse(type) { eclipseType = type; drawEclipse(); }""",
    "drawEclipse": """function drawEclipse() {
  const ctx = eclipseCtx, w = 600, h = 200;
  ctx.clearRect(0, 0, w, h);

  const sunX = 80, earthX = 520, midX = 300;
  const y = h / 2;

  // Sun
  ctx.fillStyle = '#fcee0a';
  ctx.shadowColor = '#fcee0a'; ctx.shadowBlur = 40;
  ctx.beginPath(); ctx.arc(sunX, y, 35, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = '#fcee0a'; ctx.font = '12px Orbitron';
  ctx.fillText('☀️', sunX - 8, y + 50);

  // Earth
  ctx.fillStyle = '#00bbf9';
  ctx.beginPath(); ctx.arc(earthX, y, 30, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#00bbf9'; ctx.font = '12px Orbitron';
  ctx.fillText('🌍', earthX - 8, y + 50);

  if (eclipseType === 'solar') {
    // Moon between Sun and Earth
    const moonX = midX;
    ctx.fillStyle = '#aaa';
    ctx.beginPath(); ctx.arc(moonX, y, 25, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
    ctx.fillText('🌑', moonX - 8, y + 50);

    // Shadow cone
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.beginPath();
    ctx.moveTo(sunX + 35, y - 20);
    ctx.lineTo(moonX + 25, y - 15);
    ctx.lineTo(earthX - 5, y - 8);
    ctx.lineTo(earthX - 5, y + 8);
    ctx.lineTo(moonX + 25, y + 15);
    ctx.lineTo(sunX + 35, y + 20);
    ctx.closePath(); ctx.fill();

    ctx.fillStyle = '#fcee0a';
    ctx.fillText('日食：月球遮挡太阳光 → 地球影子区', 200, 30);
  } else {
    // Earth between Sun and Moon
    const moonX = midX + 100;
    ctx.fillStyle = '#aaa';
    ctx.beginPath(); ctx.arc(moonX, y, 25, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
    ctx.fillText('🌕', moonX - 8, y + 50);

    // Shadow cone from Earth to Moon
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.beginPath();
    ctx.moveTo(earthX - 30, y - 12);
    ctx.lineTo(moonX, y - 20);
    ctx.lineTo(moonX, y + 20);
    ctx.lineTo(earthX - 30, y + 12);
    ctx.closePath(); ctx.fill();

    ctx.fillStyle = '#fcee0a';
    ctx.fillText('月食：地球遮挡太阳光 → 月球进入地球影子', 200, 30);
  }

  // Light direction arrows
  ctx.strokeStyle = 'rgba(252,238,10,0.3)';
  ctx.setLineDash([3, 3]);
  ctx.beginPath(); ctx.moveTo(sunX + 50, y); ctx.lineTo(earthX - 40, y); ctx.stroke();
  ctx.setLineDash([]);
}""",
    "setReflect": """function setReflect(type) { reflectType = type; drawReflect(); }""",
    "drawReflect": """function drawReflect() {
  const ctx = reflectCtx, w = 600, h = 280;
  ctx.clearRect(0, 0, w, h);

  // Mirror surface
  ctx.fillStyle = 'rgba(200,200,200,0.2)';
  ctx.fillRect(0, h - 60, w, 60);
  ctx.strokeStyle = 'rgba(255,255,255,0.3)';
  ctx.beginPath(); ctx.moveTo(0, h - 60); ctx.lineTo(w, h - 60); ctx.stroke();

  // Normal line
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(w / 2, 20); ctx.lineTo(w / 2, h - 60); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#aaa'; ctx.font = '11px Orbitron';
  ctx.fillText('法线', w / 2 + 5, 35);

  const originX = w / 2, mirrorY = h - 60;
  const angle = 35 * Math.PI / 180;
  const rayLen = 140;

  // Incident ray
  ctx.strokeStyle = '#fcee0a'; ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(originX - rayLen * Math.sin(angle), mirrorY - rayLen * Math.cos(angle));
  ctx.lineTo(originX, mirrorY);
  ctx.stroke();
  ctx.fillStyle = '#fcee0a'; ctx.font = '12px Orbitron';
  ctx.fillText('入射光线', originX - 120, mirrorY - 100);

  if (reflectType === 'mirror') {
    // Single reflected ray
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(originX, mirrorY);
    ctx.lineTo(originX + rayLen * Math.sin(angle), mirrorY - rayLen * Math.cos(angle));
    ctx.stroke();
    ctx.fillStyle = '#00f0c8';
    ctx.fillText('反射光线', originX + 80, mirrorY - 100);

    // Angle arcs
    ctx.strokeStyle = 'rgba(252,238,10,0.5)';
    ctx.beginPath(); ctx.arc(originX, mirrorY, 30, -Math.PI / 2 - angle, -Math.PI / 2); ctx.stroke();
    ctx.strokeStyle = 'rgba(0,240,200,0.5)';
    ctx.beginPath(); ctx.arc(originX, mirrorY, 35, -Math.PI / 2, -Math.PI / 2 + angle); ctx.stroke();

    ctx.fillStyle = '#fcee0a'; ctx.font = '12px Orbitron';
    ctx.fillText('i = 35°', originX - 70, mirrorY - 15);
    ctx.fillStyle = '#00f0c8';
    ctx.fillText('r = 35°', originX + 45, mirrorY - 15);

    ctx.fillStyle = '#aaa';
    ctx.fillText('🪞 镜面反射：平行入射 → 平行反射', 160, 30);
  } else {
    // Diffuse reflection - multiple rays at different angles
    const angles = [20, 45, 60, 80, 100, 120, 140].map(a => a * Math.PI / 180);
    angles.forEach(a => {
      ctx.strokeStyle = 'rgba(0,240,200,0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(originX, mirrorY);
      ctx.lineTo(originX + rayLen * 0.7 * Math.sin(a), mirrorY - rayLen * 0.7 * Math.cos(a));
      ctx.stroke();
    });

    ctx.fillStyle = '#aaa';
    ctx.fillText('📄 漫反射：平行入射 → 向各方向反射（我们能从各个角度看到物体）', 80, 30);
  }

  ctx.lineWidth = 1;
}""",
    "drawMirror": """function drawMirror() {
  const ctx = mirrorCtx, w = 600, h = 300;
  ctx.clearRect(0, 0, w, h);

  const mirrorX = w / 2;

  // Mirror
  ctx.fillStyle = 'rgba(200,200,220,0.15)';
  ctx.fillRect(mirrorX - 2, 40, 4, h - 80);
  ctx.strokeStyle = 'rgba(255,255,255,0.4)';
  ctx.beginPath(); ctx.moveTo(mirrorX, 40); ctx.lineTo(mirrorX, h - 40); ctx.stroke();
  ctx.fillStyle = '#aaa'; ctx.font = '11px Orbitron';
  ctx.fillText('平面镜', mirrorX + 8, h - 30);

  // Object (candle)
  const objX = mirrorX - mirrorDist;
  const baseY = h - 60;
  ctx.fillStyle = '#fcee0a';
  ctx.fillRect(objX - 8, baseY - 50, 16, 50);
  ctx.fillStyle = '#ff6b35';
  ctx.beginPath(); ctx.arc(objX, baseY - 58, 10, 0, Math.PI * 2); ctx.fill();

  // Object label
  ctx.fillStyle = '#fcee0a'; ctx.font = '13px Orbitron';
  ctx.fillText('🔥 物', objX - 15, baseY + 20);
  ctx.fillStyle = '#aaa'; ctx.font = '11px Share Tech Mono';
  ctx.fillText(`距离 = ${mirrorDist}px`, objX - 30, baseY + 38);

  // Image (virtual, behind mirror)
  const imgX = mirrorX + mirrorDist;
  ctx.globalAlpha = 0.4;
  ctx.fillStyle = '#00f0c8';
  ctx.fillRect(imgX - 8, baseY - 50, 16, 50);
  ctx.fillStyle = '#00bbf9';
  ctx.beginPath(); ctx.arc(imgX, baseY - 58, 10, 0, Math.PI * 2); ctx.fill();
  ctx.globalAlpha = 1;

  // Image label
  ctx.fillStyle = '#00f0c8'; ctx.font = '13px Orbitron';
  ctx.fillText('👤 像', imgX - 10, baseY + 20);
  ctx.fillStyle = '#aaa'; ctx.font = '11px Share Tech Mono';
  ctx.fillText(`距离 = ${mirrorDist}px`, imgX - 30, baseY + 38);

  // Distance bracket
  ctx.strokeStyle = 'rgba(252,238,10,0.3)';
  ctx.setLineDash([3, 3]);
  ctx.beginPath(); ctx.moveTo(objX, baseY - 80); ctx.lineTo(mirrorX, baseY - 80); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(mirrorX, baseY - 80); ctx.lineTo(imgX, baseY - 80); ctx.stroke();
  ctx.setLineDash([]);

  // Dashed lines for virtual image
  ctx.strokeStyle = 'rgba(0,240,200,0.3)';
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(objX, baseY - 58); ctx.lineTo(mirrorX, baseY - 58); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(mirrorX, baseY - 58); ctx.lineTo(imgX, baseY - 58); ctx.stroke();
  ctx.setLineDash([]);

  // Symmetry text
  ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
  ctx.fillText('像距 = 物距', mirrorX - 40, 30);
  ctx.fillText('像与物大小相等', mirrorX - 55, 48);
}""",
    "setMedium": """function setMedium(type) { mediumType = type; drawRefract(); }""",
    "drawRefract": """function drawRefract() {
  const ctx = refractCtx, w = 600, h = 300;
  ctx.clearRect(0, 0, w, h);

  const [from, to] = mediumType.split('-');
  const n1 = n[from], n2 = n[to];
  const i = incidentAngleVal * Math.PI / 180;

  // Snell's law: n1 sin i = n2 sin r
  const sinR = (n1 / n2) * Math.sin(i);
  const r = Math.asin(Math.min(sinR, 1));

  // Medium backgrounds
  ctx.fillStyle = from === 'air' ? 'rgba(10,14,26,0.5)' : (from === 'water' ? 'rgba(0,100,200,0.15)' : 'rgba(100,200,200,0.15)');
  ctx.fillRect(0, 0, w, h / 2);
  ctx.fillStyle = to === 'air' ? 'rgba(10,14,26,0.5)' : (to === 'water' ? 'rgba(0,100,200,0.15)' : 'rgba(100,200,200,0.15)');
  ctx.fillRect(0, h / 2, w, h / 2);

  // Boundary
  ctx.strokeStyle = 'rgba(255,255,255,0.3)';
  ctx.beginPath(); ctx.moveTo(0, h / 2); ctx.lineTo(w, h / 2); ctx.stroke();

  // Labels
  ctx.fillStyle = '#aaa'; ctx.font = '13px Orbitron';
  ctx.fillText(`${from === 'air' ? '🌫️ 空气' : (from === 'water' ? '💧 水' : '🔮 玻璃')}  n=${n1}`, 20, 30);
  ctx.fillText(`${to === 'air' ? '🌫️ 空气' : (to === 'water' ? '💧 水' : '🔮 玻璃')}  n=${n2}`, 20, h - 20);

  const originX = w / 2, originY = h / 2;

  // Normal
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(originX, 20); ctx.lineTo(originX, h - 20); ctx.stroke();
  ctx.setLineDash([]);

  // Incident ray
  const rayLen = 130;
  ctx.strokeStyle = '#fcee0a'; ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(originX - rayLen * Math.sin(i), originY - rayLen * Math.cos(i));
  ctx.lineTo(originX, originY);
  ctx.stroke();

  // Refracted ray
  if (sinR <= 1) {
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(originX, originY);
    ctx.lineTo(originX + rayLen * Math.sin(r), originY + rayLen * Math.cos(r));
    ctx.stroke();

    // Angle labels
    ctx.fillStyle = '#fcee0a'; ctx.font = '12px Orbitron';
    ctx.fillText(`i=${incidentAngleVal}°`, originX - 50, originY - 20);
    ctx.fillStyle = '#00f0c8';
    ctx.fillText(`r=${(r * 180 / Math.PI).toFixed(1)}°`, originX + 20, originY + 35);
  } else {
    // Total internal reflection
    ctx.strokeStyle = '#ff6b35'; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(originX, originY);
    ctx.lineTo(originX + rayLen * Math.sin(i), originY - rayLen * Math.cos(i));
    ctx.stroke();
    ctx.fillStyle = '#ff6b35'; ctx.font = '12px Orbitron';
    ctx.fillText('全反射', originX + 50, originY - 30);
  }

  ctx.lineWidth = 1;
}""",
    "drawPrism": """function drawPrism() {
  const ctx = prismCtx, w = 600, h = 250;
  ctx.clearRect(0, 0, w, h);

  const cx = w / 2, cy = h / 2 + 20;
  const size = 70;

  // Prism triangle
  ctx.fillStyle = 'rgba(200,200,220,0.1)';
  ctx.strokeStyle = 'rgba(255,255,255,0.3)';
  ctx.beginPath();
  ctx.moveTo(cx, cy - size);
  ctx.lineTo(cx - size * 0.866, cy + size * 0.5);
  ctx.lineTo(cx + size * 0.866, cy + size * 0.5);
  ctx.closePath();
  ctx.fill(); ctx.stroke();

  // Incident white light
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(40, cy); ctx.lineTo(cx - 50, cy); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.font = '12px Orbitron';
  ctx.fillText('☀️ 白光', 10, cy - 10);

  // Spectrum rays
  const colors = [
    { c: '#ff0000', a: -18 }, { c: '#ff7f00', a: -12 }, { c: '#ffff00', a: -6 },
    { c: '#00ff00', a: 0 }, { c: '#0000ff', a: 6 }, { c: '#4b0082', a: 12 }, { c: '#9400d3', a: 18 }
  ];
  const rayLen = 120;
  colors.forEach(col => {
    const rad = col.a * Math.PI / 180;
    ctx.strokeStyle = col.c; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx + 50, cy);
    ctx.lineTo(cx + 50 + rayLen * Math.cos(rad), cy + rayLen * Math.sin(rad));
    ctx.stroke();
  });

  ctx.fillStyle = '#aaa'; ctx.font = '12px Orbitron';
  ctx.fillText('🌈 光谱', cx + 130, cy + 5);

  // Color labels
  const labels = ['红','橙','黄','绿','蓝','靛','紫'];
  const labelColors = ['#ff0000','#ff7f00','#ffff00','#00ff00','#0000ff','#4b0082','#9400d3'];
  labels.forEach((lab, i) => {
    ctx.fillStyle = labelColors[i];
    ctx.fillText(lab, cx + 50 + rayLen + 20 + i * 22, cy + (i - 3) * 12);
  });

  ctx.lineWidth = 1;
}""",
    "drawLens": """function drawLens() {
  const ctx = lensCtx, w = 600, h = 320;
  ctx.clearRect(0, 0, w, h);

  const f = 60;
  const u = lensU * f / 10;
  const lensX = w / 2;
  const axisY = h / 2 + 20;

  // Principal axis
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.beginPath(); ctx.moveTo(40, axisY); ctx.lineTo(w - 40, axisY); ctx.stroke();

  // Focal points
  ctx.fillStyle = '#fcee0a';
  ctx.beginPath(); ctx.arc(lensX - f, axisY, 4, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(lensX + f, axisY, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#aaa'; ctx.font = '11px Orbitron';
  ctx.fillText('F', lensX - f - 5, axisY + 20);
  ctx.fillText('F', lensX + f - 5, axisY + 20);

  // 2F points
  ctx.fillStyle = '#ff6b35';
  ctx.beginPath(); ctx.arc(lensX - 2 * f, axisY, 4, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(lensX + 2 * f, axisY, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#aaa'; ctx.font = '11px Orbitron';
  ctx.fillText('2F', lensX - 2 * f - 10, axisY + 20);
  ctx.fillText('2F', lensX + 2 * f - 10, axisY + 20);

  // Lens
  ctx.strokeStyle = 'rgba(200,200,220,0.3)';
  ctx.beginPath();
  ctx.moveTo(lensX, axisY - 60);
  ctx.quadraticCurveTo(lensX + 12, axisY - 30, lensX, axisY);
  ctx.quadraticCurveTo(lensX - 12, axisY + 30, lensX, axisY + 60);
  ctx.stroke();
  ctx.fillStyle = 'rgba(200,200,220,0.05)';
  ctx.fill();

  // Object (arrow)
  const objX = lensX - u;
  const objH = 40;
  ctx.strokeStyle = '#fcee0a'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(objX, axisY); ctx.lineTo(objX, axisY - objH); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(objX - 6, axisY - objH + 8); ctx.lineTo(objX, axisY - objH); ctx.lineTo(objX + 6, axisY - objH + 8); ctx.stroke();
  ctx.fillStyle = '#fcee0a'; ctx.font = '12px Orbitron';
  ctx.fillText('🔥 物', objX - 12, axisY + 20);

  // Calculate image position using lens formula: 1/u + 1/v = 1/f
  let v, imgH, real;
  if (u > f) {
    v = (u * f) / (u - f);
    imgH = objH * v / u;
    real = true;
  } else {
    v = (u * f) / (f - u);
    imgH = objH * v / u;
    real = false;
  }

  const imgX = lensX + v;

  if (real) {
    // Real image - inverted
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(imgX, axisY); ctx.lineTo(imgX, axisY + imgH); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(imgX - 6, axisY + imgH - 8); ctx.lineTo(imgX, axisY + imgH); ctx.lineTo(imgX + 6, axisY + imgH - 8); ctx.stroke();
    ctx.fillStyle = '#00f0c8'; ctx.font = '12px Orbitron';
    ctx.fillText('👤 实像', imgX - 15, axisY - 15);
  } else {
    // Virtual image - upright, on same side as object
    const virtX = lensX - v;
    ctx.globalAlpha = 0.5;
    ctx.strokeStyle = '#00f0c8'; ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(virtX, axisY); ctx.lineTo(virtX, axisY - imgH); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(virtX - 6, axisY - imgH + 8); ctx.lineTo(virtX, axisY - imgH); ctx.lineTo(virtX + 6, axisY - imgH + 8); ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#00f0c8'; ctx.font = '12px Orbitron';
    ctx.fillText('👤 虚像', virtX - 15, axisY + 20);
  }

  // Ray diagram
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 3]);

  // Ray 1: parallel to axis → through F'
  ctx.strokeStyle = 'rgba(252,238,10,0.3)';
  ctx.beginPath(); ctx.moveTo(objX, axisY - objH); ctx.lineTo(lensX, axisY - objH); ctx.stroke();
  if (real) {
    ctx.beginPath(); ctx.moveTo(lensX, axisY - objH); ctx.lineTo(imgX, axisY); ctx.stroke();
  } else {
    ctx.beginPath(); ctx.moveTo(lensX, axisY - objH); ctx.lineTo(lensX + 200, axisY - objH - 200 * (objH / f)); ctx.stroke();
    // Backward extension to virtual image
    ctx.strokeStyle = 'rgba(0,240,200,0.2)';
    ctx.beginPath(); ctx.moveTo(lensX, axisY - objH); ctx.lineTo(lensX - v, axisY - imgH); ctx.stroke();
  }

  // Ray 2: through center → straight
  ctx.strokeStyle = 'rgba(252,238,10,0.3)';
  ctx.beginPath(); ctx.moveTo(objX, axisY - objH); ctx.lineTo(imgX, real ? axisY + imgH : axisY - imgH); ctx.stroke();

  ctx.setLineDash([]);

  // Description
  let desc = '';
  if (u > 2 * f) desc = 'u > 2f：倒立、缩小、实像';
  else if (u === 2 * f) desc = 'u = 2f：倒立、等大、实像';
  else if (u > f) desc = 'f < u < 2f：倒立、放大、实像';
  else desc = 'u < f：正立、放大、虚像';

  ctx.fillStyle = '#fcee0a'; ctx.font = '13px Orbitron';
  ctx.fillText(desc, 40, 30);

  ctx.lineWidth = 1;
}""",
    "iife_reflectlaw": """(function(){
  const c = document.getElementById('reflectLawCanvas'); if(!c) return;
  const ctx = c.getContext('2d');
  const angInput = document.getElementById('incidentAngle');
  const angVal = document.getElementById('incidentVal');
  function draw() {
    let i = angInput ? parseInt(angInput.value) : 45;
    if(angVal) angVal.textContent = i + '°';
    ctx.clearRect(0,0,500,250);
    ctx.strokeStyle = 'var(--text-dim)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(50,200); ctx.lineTo(450,200); ctx.stroke();
    ctx.strokeStyle = 'var(--accent)'; ctx.lineWidth = 2;
    let rad = i * Math.PI / 180;
    ctx.beginPath(); ctx.moveTo(250,200); ctx.lineTo(250 - Math.sin(rad)*180, 200 - Math.cos(rad)*180); ctx.stroke();
    ctx.strokeStyle = 'var(--accent2)'; ctx.beginPath(); ctx.moveTo(250,200); ctx.lineTo(250 + Math.sin(rad)*180, 200 - Math.cos(rad)*180); ctx.stroke();
    ctx.fillStyle = 'var(--text-dim)'; ctx.font = '14px monospace';
    ctx.fillText('法线', 260, 120); ctx.fillText('入射角 = 反射角 = ' + i + '°', 150, 40);
    requestAnimationFrame(draw);
  }
  draw();
})();""",
    "iife_lens": """(function(){
  const c = document.getElementById('lensCanvas'); if(!c) return;
  const ctx = c.getContext('2d');
  const dInput = document.getElementById('objDist');
  const dVal = document.getElementById('objDistVal');
  function draw() {
    let u = dInput ? parseInt(dInput.value) : 100;
    if(dVal) dVal.textContent = u + ' mm';
    let f = 50, v = f*u/(u-f);
    ctx.clearRect(0,0,500,250);
    ctx.strokeStyle = 'var(--text-dim)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(50,125); ctx.lineTo(450,125); ctx.stroke();
    ctx.strokeStyle = 'var(--accent)'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(250,50); ctx.lineTo(250,200); ctx.stroke();
    ctx.fillStyle = 'var(--accent2)'; ctx.fillRect(250-u-10, 110, 20, 30);
    if(v > 0) { ctx.fillStyle = 'var(--success)'; ctx.fillRect(250+v-10, 110, 20, 30); }
    ctx.fillStyle = 'var(--text)'; ctx.font = '12px monospace';
    ctx.fillText('f=' + f + 'mm', 260, 220); ctx.fillText('v=' + Math.abs(v).toFixed(0) + 'mm', 320, 220);
    requestAnimationFrame(draw);
  }
  draw();
})();""",
}
