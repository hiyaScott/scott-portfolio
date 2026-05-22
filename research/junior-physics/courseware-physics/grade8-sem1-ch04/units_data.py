unit2 = """<div class="card hidden" id="ch2">
  <div class="card-header">
    <h2>🪞 光的反射</h2>
    <span class="chapter-num">第 2 / 5 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p>光射到物体表面时，部分光被<strong>反射</strong>回原来介质中。</p>
    <p><strong>法线</strong>：过入射点垂直于反射面的直线。</p>
    <p><strong>入射角</strong>：入射光线与法线的夹角。<strong>反射角</strong>：反射光线与法线的夹角。</p>
    <div class="formula">反射定律：∠i = ∠r（入射角 = 反射角）</div>
    <p>反射分为<strong>镜面反射</strong>和<strong>漫反射</strong>。我们能从不同方向看到物体，就是因为发生了漫反射。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">📐 反射定律演示</div>
    <div class="demo-box">
      <canvas id="reflectCanvas" width="600" height="300"></canvas>
      <div class="slider-control">
        <label>入射角</label>
        <input type="range" id="reflectAngle" min="10" max="80" value="45" oninput="drawReflect()">
        <span class="value" id="reflectAngleVal">45°</span>
      </div>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">拖动滑块改变入射角，观察反射角始终相等</p>
    </div>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🪞 平面镜成像</div>
    <div class="demo-box">
      <canvas id="mirrorCanvas" width="600" height="300"></canvas>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">虚像：等大、等距、左右相反</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：一束光线与平面镜成 30° 角入射，求反射角。</div>
      <div class="a">
        <strong>解：</strong>入射角 = 90° - 30° = 60°<br>
        根据反射定律：反射角 = 入射角 = <strong style="color:var(--success)">60°</strong>
        <div class="step">注意：题目给的是光线与镜面夹角，不是入射角！入射角是光线与法线的夹角。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：若入射角增大 10°，反射光线与入射光线的夹角变为多少？（接上题）</div>
      <div class="a">
        <strong>解：</strong>原入射角 60°，增大后 = 70°<br>
        反射角 = 70°<br>
        夹角 = 入射角 + 反射角 = 70° + 70° = <strong style="color:var(--success)">140°</strong>
        <div class="step">反射光线与入射光线的夹角 = 入射角 + 反射角 = 2 × 入射角</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：一个人站在平面镜前 1.5 m 处，镜中像距离他多远？若他向镜子走近 0.5 m，像的大小如何变化？</div>
      <div class="a">
        <strong>解：</strong><br>
        (1) 像距 = 物距 = 1.5 m，像距人 = 1.5 + 1.5 = <strong style="color:var(--success)">3 m</strong><br>
        (2) 走近后像距人 = (1.5-0.5) × 2 = <strong style="color:var(--success)">2 m</strong><br>
        (3) 像的大小<strong style="color:var(--success)">不变</strong>（平面镜成等大的虚像）
        <div class="step">平面镜成像特点：虚像、等大、等距、左右相反、上下不变。像的大小与距离无关。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch2-quiz">
    <div class="quiz-title">🎯 随堂测验 — 光的反射</div>
    <div class="quiz-question"><strong>Q1.</strong> 一束光以 40° 入射角射向平面镜，反射角是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。反射角等于入射角，应该是 40°。')">A. 20°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！反射定律：反射角 = 入射角 = 40°。')">B. 40°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。反射角等于入射角，不是 50°。')">C. 50°</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 我们能从不同方向看到书本，是因为书本表面发生了？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。镜面反射只在特定方向有强光。')">A. 镜面反射</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！漫反射使光线射向各个方向，所以我们能从不同角度看到物体。')">B. 漫反射</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。书本不透明，不会发生折射。')">C. 折射</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 平面镜中的像与物体相比？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。平面镜成等大的像，大小不变。')">A. 变小</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！平面镜成等大的虚像，与物体大小完全相同。')">B. 等大</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。平面镜成虚像，不是实像。')">C. 成实像</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(1)">← 上一单元</button>
    <button class="btn" onclick="goTo(3)">下一单元 →</button>
  </div>
</div>"""
unit3 = """<div class="card hidden" id="ch3">
  <div class="card-header">
    <h2>💎 光的折射</h2>
    <span class="chapter-num">第 3 / 5 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p>光从一种介质斜射入另一种介质时，传播方向发生<strong>偏折</strong>，这种现象叫折射。</p>
    <div class="formula">折射规律：空气 → 水/玻璃，折射角 < 入射角</div>
    <p><strong>光路可逆</strong>：光沿着折射光线入射时，会沿着原入射光线方向折射出去。</p>
    <p><strong>折射率</strong>：n = sin i / sin r（空气→水 n ≈ 1.33，空气→玻璃 n ≈ 1.5）</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">💎 折射规律演示</div>
    <div class="demo-box">
      <canvas id="refractCanvas" width="600" height="300"></canvas>
      <div class="slider-control">
        <label>入射角</label>
        <input type="range" id="refractAngle" min="10" max="70" value="45" oninput="drawRefract()">
        <span class="value" id="refractAngleVal">45°</span>
      </div>
      <div style="margin-top:10px">
        <button class="btn" onclick="setMedium('water')">💧 水 (n≈1.33)</button>
        <button class="btn btn-ghost" onclick="setMedium('glass')">🔷 玻璃 (n≈1.5)</button>
      </div>
    </div>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🌈 光的色散</div>
    <div class="demo-box">
      <canvas id="prismCanvas" width="600" height="250"></canvas>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">白光通过三棱镜分解成七色光谱：红、橙、黄、绿、蓝、靛、紫</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：一束光从空气斜射入水中，入射角为 45°，已知水的折射率约为 1.33，求折射角大约是多少？</div>
      <div class="a">
        <strong>解：</strong>n = sin i / sin r<br>
        sin r = sin 45° / 1.33 ≈ 0.707 / 1.33 ≈ 0.532<br>
        r ≈ arcsin(0.532) ≈ <strong style="color:var(--success)">32°</strong>
        <div class="step">折射率公式：n = sin i / sin r。光从空气进入水，折射角 < 入射角。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：光从水中射入空气时，折射角与入射角的关系是？</div>
      <div class="a">
        <strong>解：</strong>光从水（光密介质）射入空气（光疏介质）<br>
        折射角 <strong style="color:var(--success)">大于</strong> 入射角<br>
        当入射角增大到某一角度时，折射角达到 90°，此时发生<strong>全反射</strong>。
        <div class="step">光路可逆：空气→水时折射角小，水→空气时折射角大。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：游泳池看起来比实际浅，是什么原因？</div>
      <div class="a">
        <strong>解：</strong>光从水中射入空气时发生折射，折射角大于入射角。<br>
        我们逆着折射光线看去，会觉得池底的位置比实际位置<strong style="color:var(--success)">高</strong>（浅），<br>
        所以池水看起来比实际浅。
        <div class="step">这是光的折射造成的视觉误差。同理，水中的筷子看起来"弯折"也是折射。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch3-quiz">
    <div class="quiz-title">🎯 随堂测验 — 光的折射</div>
    <div class="quiz-question"><strong>Q1.</strong> 光从空气斜射入水中时，折射角与入射角的关系是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！光从空气（光疏）进入水（光密），折射角 < 入射角。')">A. 折射角小于入射角</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。折射角等于入射角只有垂直入射时才成立。')">B. 折射角等于入射角</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。光从空气进入水，折射角应该小于入射角。')">C. 折射角大于入射角</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 下列现象中，属于光的折射的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。水中倒影是光的反射。')">A. 水中倒影</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！筷子在水中"弯折"是光的折射造成的。')">B. 筷子在水中看起来弯折</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。黑板反光属于镜面反射。')">C. 黑板反光</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 一束光垂直射向水面，入射角是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！垂直入射时，入射光线与法线重合，入射角 = 0°。')">A. 0°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。垂直入射不是 90°，入射角是光线与法线的夹角。')">B. 90°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。垂直入射时入射角为 0°。')">C. 45°</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(2)">← 上一单元</button>
    <button class="btn" onclick="goTo(4)">下一单元 →</button>
  </div>
</div>"""
unit4 = """<div class="card hidden" id="ch4">
  <div class="card-header">
    <h2>🔍 透镜与成像</h2>
    <span class="chapter-num">第 4 / 5 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>凸透镜</strong>：中间厚边缘薄，对光线有<strong>会聚</strong>作用。</p>
    <p><strong>凹透镜</strong>：中间薄边缘厚，对光线有<strong>发散</strong>作用。</p>
    <p><strong>焦点</strong>：平行于主光轴的光线经凸透镜折射后会聚的点。</p>
    <p><strong>焦距</strong>：光心到焦点的距离，用 f 表示。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🔍 凸透镜成像规律</div>
    <div class="demo-box">
      <canvas id="lensCanvas" width="600" height="300"></canvas>
      <div class="slider-control">
        <label>物距 u</label>
        <input type="range" id="lensU" min="10" max="100" value="60" oninput="drawLens()">
        <span class="value" id="lensUVal">60 cm</span>
      </div>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">拖动滑块改变物距，观察成像变化（u > 2f 成缩小实像，f < u < 2f 成放大实像）</p>
    </div>
  </div>

  <div class="concept-box">
    <div class="label">成像规律总结</div>
    <p><strong>u > 2f</strong>：倒立、缩小、实像（照相机原理）</p>
    <p><strong>u = 2f</strong>：倒立、等大、实像</p>
    <p><strong>f < u < 2f</strong>：倒立、放大、实像（投影仪原理）</p>
    <p><strong>u = f</strong>：不成像（平行光）</p>
    <p><strong>u < f</strong>：正立、放大、虚像（放大镜原理）</p>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：用焦距为 10 cm 的凸透镜做实验，蜡烛放在距透镜 25 cm 处，光屏上得到的像是？</div>
      <div class="a">
        <strong>解：</strong>u = 25 cm，f = 10 cm，2f = 20 cm<br>
        u > 2f（25 > 20）<br>
        成<strong style="color:var(--success)">倒立、缩小、实像</strong>（照相机原理）
        <div class="step">u > 2f → 倒立缩小实像，像距 f < v < 2f</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：上题中，若将蜡烛移到距透镜 15 cm 处，此时成像性质是？</div>
      <div class="a">
        <strong>解：</strong>u = 15 cm，f = 10 cm，2f = 20 cm<br>
        f < u < 2f（10 < 15 < 20）<br>
        成<strong style="color:var(--success)">倒立、放大、实像</strong>（投影仪原理）<br>
        像距 v > 2f
        <div class="step">f < u < 2f → 倒立放大实像，像距 v > 2f</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：老奶奶用放大镜看书，放大镜距书本 8 cm，放大镜焦距为 12 cm，看到的字是什么样的？</div>
      <div class="a">
        <strong>解：</strong>u = 8 cm，f = 12 cm<br>
        u < f（8 < 12）<br>
        成<strong style="color:var(--success)">正立、放大、虚像</strong><br>
        老奶奶看到的字变大了，但不能呈现在光屏上。
        <div class="step">u < f → 正立放大虚像，放大镜原理。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch4-quiz">
    <div class="quiz-title">🎯 随堂测验 — 透镜与成像</div>
    <div class="quiz-question"><strong>Q1.</strong> 照相机镜头相当于一个凸透镜，被拍摄的物体应放在？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！照相机利用 u > 2f 成倒立缩小实像的原理。')">A. 二倍焦距以外</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。u = 2f 成等大实像，不是照相机原理。')">B. 二倍焦距处</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。u < f 成正立放大虚像，是放大镜原理。')">C. 一倍焦距以内</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 投影仪利用凸透镜成什么像？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。缩小实像是照相机原理。')">A. 倒立、缩小、实像</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！投影仪利用 f < u < 2f 成倒立放大实像的原理。')">B. 倒立、放大、实像</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。虚像不能在光屏上呈现。')">C. 正立、放大、虚像</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 凸透镜焦距 15 cm，物体放在 10 cm 处，成像性质是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。u < f 不是缩小实像。')">A. 倒立、缩小、实像</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。u < f 不是放大实像。')">B. 倒立、放大、实像</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！u = 10 cm < f = 15 cm，成正立放大虚像（放大镜）。')">C. 正立、放大、虚像</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(3)">← 上一单元</button>
    <button class="btn" onclick="goTo(5)">下一单元 →</button>
  </div>
</div>"""
unit5 = """<div class="card hidden" id="ch5">
  <div class="card-header">
    <h2>📋 公式与要点总结</h2>
    <span class="chapter-num">第 5 / 5 节</span>
  </div>

  <div class="formula-box" style="text-align:left;font-size:15px">
    <p>⚡ <strong>光速：</strong>c = 3 × 10⁸ m/s（真空中）</p>
    <p style="margin-top:12px">🪞 <strong>反射定律：</strong>∠i = ∠r（入射角 = 反射角）</p>
    <p style="margin-top:12px">💎 <strong>折射规律：</strong>空气→水/玻璃，折射角 < 入射角</p>
    <p style="margin-top:12px">🔍 <strong>凸透镜成像：</strong></p>
    <p style="margin-left:20px">u > 2f → 缩小实像（照相机）</p>
    <p style="margin-left:20px">f < u < 2f → 放大实像（投影仪）</p>
    <p style="margin-left:20px">u < f → 放大虚像（放大镜）</p>
  </div>

  <div class="concept-box">
    <div class="label">易错警示</div>
    <p>❌ 混淆"光线与镜面夹角"和"入射角"——入射角是与法线的夹角</p>
    <p>❌ 认为平面镜成像大小与距离有关——像始终等大</p>
    <p>❌ 折射时忘记判断介质——光密→光疏时折射角 > 入射角</p>
    <p>❌ 透镜成像记不住分界点——记住 f 和 2f 两个关键位置</p>
  </div>

  <div class="quiz-box" id="ch5-quiz">
    <div class="quiz-title">🎯 本章综合测试</div>
    <div class="quiz-question"><strong>Q1.</strong> 光在真空中的传播速度约为？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！c = 3×10⁸ m/s。')">A. 3 × 10⁸ m/s</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。这是声速。')">B. 340 m/s</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。指数错了。')">C. 3 × 10⁵ m/s</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 一束光以 30° 入射角射向平面镜，反射角为？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！反射角 = 入射角 = 30°。')">A. 30°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。反射角等于入射角，不是 60°。')">B. 60°</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。')">C. 90°</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 光从空气斜射入水中时？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！折射角 < 入射角。')">A. 折射角小于入射角</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。')">B. 折射角大于入射角</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。')">C. 传播方向不变</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb3"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q4.</strong> 照相机镜头成像原理是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。这是投影仪。')">A. f < u < 2f</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！u > 2f 成倒立缩小实像。')">B. u > 2f</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。这是放大镜。')">C. u < f</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb4"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(4)">← 上一单元</button>
    <a class="btn btn-warn" href="game.html">🎮 挑战模式 →</a>
  </div>
</div>"""
