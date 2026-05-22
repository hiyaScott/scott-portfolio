# Part 2: Units 2-6 for ch05

unit2 = '''<div class="card hidden" id="ch2">
  <div class="card-header">
    <h2>💪 力的概念</h2>
    <span class="chapter-num">第 2 / 6 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>力</strong>是物体对物体的作用。力的单位是<strong>牛顿（N）</strong>。</p>
    <p>力的两种作用效果：<br>① 改变物体的形状（形变）<br>② 改变物体的运动状态（速度大小或方向）</p>
    <p>力的三要素：<strong>大小、方向、作用点</strong>。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">💪 力的作用效果演示</div>
    <div class="demo-box">
      <canvas id="forceCanvas" width="600" height="250"></canvas>
      <div style="margin-top:10px">
        <button class="btn" onclick="setForceDemo('shape')">🔧 形变效果</button>
        <button class="btn btn-ghost" onclick="setForceDemo('motion')">🏃 运动效果</button>
      </div>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">观察力如何改变物体形状或运动状态</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：用手拉弹簧，弹簧变长了；用手压气球，气球变扁了。这说明力可以产生什么效果？</div>
      <div class="a">
        <strong>解：</strong>拉弹簧和压气球都使物体发生了形状变化，说明力可以改变物体的<strong style="color:var(--success)">形状</strong>（产生形变）。
        <div class="step">力的作用效果之一：使物体发生形变（形状变化）。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：踢足球时，足球由静止变为运动；守门员接住足球，足球由运动变为静止。这说明力可以产生什么效果？</div>
      <div class="a">
        <strong>解：</strong>两种情况都改变了足球的<strong style="color:var(--success)">运动状态</strong>（速度从 0 变到非 0，或从非 0 变到 0）。
        <div class="step">力的作用效果之二：改变物体的运动状态（速度大小或方向）。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：用大小相同的力推门，作用在门把手上比作用在门轴附近更容易把门推开，这说明力的作用效果与什么有关？</div>
      <div class="a">
        <strong>解：</strong>力的大小和方向相同，但<strong style="color:var(--success)">作用点</strong>不同，效果不同。
        <div class="step">力的三要素：大小、方向、作用点。三者中任意一个改变，力的作用效果都可能改变。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch2-quiz">
    <div class="quiz-title">🎯 随堂测验 — 力的概念</div>
    <div class="quiz-question"><strong>Q1.</strong> 下列现象中，不属于力改变物体运动状态的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。球停下来是运动状态改变（速度变小到0）。')">A. 滚动的足球慢慢停下来</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！捏橡皮泥是改变形状，不是运动状态。')">B. 捏扁橡皮泥</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。汽车加速是运动状态改变（速度增大）。')">C. 汽车加速行驶</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 力的单位是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。kg 是质量单位。')">A. kg</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！力的单位是牛顿（N）。')">B. N（牛顿）</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。m 是长度单位。')">C. m</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 影响力的作用效果的三要素是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！力的大小、方向、作用点决定了力的作用效果。')">A. 大小、方向、作用点</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。速度不是力的三要素。')">B. 大小、方向、速度</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。形状不是力的三要素。')">C. 大小、形状、作用点</button>
    </div>
    <div class="quiz-feedback" id="ch2-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(1)">← 上一单元</button>
    <button class="btn" onclick="goTo(3)">下一单元 →</button>
  </div>
</div>'''

unit3 = '''<div class="card hidden" id="ch3">
  <div class="card-header">
    <h2>🌍 重力</h2>
    <span class="chapter-num">第 3 / 6 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>重力</strong>：由于地球吸引而使物体受到的力。方向<strong>竖直向下</strong>（指向地心）。</p>
    <p><strong>重心</strong>：物体各部分所受重力的等效作用点。均匀规则物体的重心在几何中心。</p>
    <div class="formula">G = mg （重力 = 质量 × 重力加速度）</div>
    <p>g ≈ 9.8 N/kg（地球表面），粗略计算可取 10 N/kg。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🌍 重力与质量关系</div>
    <div class="demo-box">
      <canvas id="gravityCanvas" width="600" height="250"></canvas>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">质量越大，受到的重力越大。G = mg</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：一个质量为 50 kg 的中学生，受到的重力大约是多少？（g 取 10 N/kg）</div>
      <div class="a">
        <strong>解：</strong>G = mg = 50 × 10 = <strong style="color:var(--success)">500 N</strong>
        <div class="step">重力公式 G = mg。质量 m 单位 kg，g 单位 N/kg，重力 G 单位 N。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：一头大象的质量是 5000 kg，它受到的重力是多少？如果把它搬到月球上（月球 g ≈ 1.6 N/kg），重力变为多少？</div>
      <div class="a">
        <strong>解：</strong><br>
        地球上：G₁ = 5000 × 10 = <strong style="color:var(--success)">50,000 N</strong><br>
        月球上：G₂ = 5000 × 1.6 = <strong style="color:var(--success)">8,000 N</strong>
        <div class="step">质量是物体的固有属性，不随位置变化；重力随 g 的变化而变化。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：一个物体在地球上的重力是 196 N，它的质量是多少？（g = 9.8 N/kg）</div>
      <div class="a">
        <strong>解：</strong>G = mg → m = G/g = 196 / 9.8 = <strong style="color:var(--success)">20 kg</strong>
        <div class="step">公式变形：m = G/g。注意 g = 9.8 N/kg 时不能用 10 来估算。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch3-quiz">
    <div class="quiz-title">🎯 随堂测验 — 重力</div>
    <div class="quiz-question"><strong>Q1.</strong> 关于重力，下列说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。重力的方向是竖直向下，不是垂直向下（竖直是相对于水平面，垂直是相对于接触面）。')">A. 重力的方向垂直向下</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！质量不随位置变化，月球上质量仍为 60 kg。')">B. 质量 60 kg 的人到月球上，质量仍为 60 kg</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。G = mg，同一地点重力与质量成正比。')">C. 物体受到的重力与质量无关</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 一个质量为 5 kg 的物体，在地球上受到的重力约为？（g 取 10 N/kg）</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。G = mg = 5×10 = 50 N。')">A. 5 N</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！G = mg = 5×10 = 50 N。')">B. 50 N</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。G = mg = 5×10 = 50 N。')">C. 0.5 N</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 下列物体的重心位置，说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！均匀正方体的重心在其几何中心（对角线交点）。')">A. 均匀正方体的重心在几何中心</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。重心与物体是否空心有关，空心球的重心也在球心。')">B. 空心球没有重心</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。均匀圆环的重心在圆心，不在环上。')">C. 均匀圆环的重心在环上</button>
    </div>
    <div class="quiz-feedback" id="ch3-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(2)">← 上一单元</button>
    <button class="btn" onclick="goTo(4)">下一单元 →</button>
  </div>
</div>'''

unit4 = '''<div class="card hidden" id="ch4">
  <div class="card-header">
    <h2>🌀 弹力与摩擦力</h2>
    <span class="chapter-num">第 4 / 6 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>弹力</strong>：物体发生弹性形变时产生的力。弹簧测力计就是利用弹力工作的。</p>
    <p><strong>弹簧测力计原理</strong>：在弹性限度内，弹簧的伸长量与拉力成正比。</p>
    <p><strong>摩擦力</strong>：两个相互接触的物体，当它们相对运动或有相对运动趋势时，在接触面上产生的阻碍相对运动的力。</p>
    <p>增大摩擦：增大压力、增大接触面粗糙程度<br>减小摩擦：加润滑油、变滑动为滚动、减小压力</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🌀 弹簧测力计原理</div>
    <div class="demo-box">
      <canvas id="springCanvas" width="600" height="250"></canvas>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">在弹性限度内，弹簧伸长量与拉力成正比</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：弹簧测力计的刻度是均匀的，这是因为什么？</div>
      <div class="a">
        <strong>解：</strong>因为在弹性限度内，弹簧的伸长量与受到的拉力成<strong style="color:var(--success)">正比</strong>，所以刻度均匀。
        <div class="step">胡克定律（初中简化版）：F = kx，拉力与伸长量成正比。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：自行车轮胎上有凹凸不平的花纹，这是通过什么方式增大摩擦？</div>
      <div class="a">
        <strong>解：</strong>轮胎花纹使接触面更粗糙，这是通过<strong style="color:var(--success)">增大接触面粗糙程度</strong>来增大摩擦。
        <div class="step">增大摩擦的方法：①增大压力 ②增大接触面粗糙程度。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：给机器加润滑油、行李箱底部安装轮子，各是通过什么方式减小摩擦？</div>
      <div class="a">
        <strong>解：</strong><br>
        加润滑油：使接触面分离，<strong style="color:var(--success)">减小接触面粗糙程度</strong><br>
        安装轮子：<strong style="color:var(--success)">变滑动为滚动</strong>，滚动摩擦远小于滑动摩擦
        <div class="step">减小摩擦的方法：①加润滑油 ②变滑动为滚动 ③减小压力 ④使接触面分离。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch4-quiz">
    <div class="quiz-title">🎯 随堂测验 — 弹力与摩擦力</div>
    <div class="quiz-question"><strong>Q1.</strong> 弹簧测力计是利用什么原理工作的？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。弹簧测力计利用的是弹力，不是重力。')">A. 重力</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！弹簧测力计利用弹力：弹性限度内，伸长量与拉力成正比。')">B. 弹力</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。弹簧测力计利用的是弹力。')">C. 摩擦力</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 下列实例中，属于增大摩擦的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！鞋底花纹增大接触面粗糙程度，从而增大摩擦。')">A. 鞋底有花纹</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。加润滑油是减小摩擦。')">B. 给机器加润滑油</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。安装轮子是变滑动为滚动，减小摩擦。')">C. 行李箱安装轮子</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 关于弹力，下列说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。弹力是物体发生弹性形变时产生的，与是否接触有关。')">A. 弹力不需要接触就能产生</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。塑性形变（不能恢复的形变）不产生弹力。')">B. 任何形变都会产生弹力</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！只有弹性形变（能恢复的形变）才会产生弹力。')">C. 只有弹性形变才会产生弹力</button>
    </div>
    <div class="quiz-feedback" id="ch4-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(3)">← 上一单元</button>
    <button class="btn" onclick="goTo(5)">下一单元 →</button>
  </div>
</div>'''

unit5 = '''<div class="card hidden" id="ch5">
  <div class="card-header">
    <h2>🚀 牛顿第一定律</h2>
    <span class="chapter-num">第 5 / 6 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p><strong>牛顿第一定律（惯性定律）</strong>：一切物体在没有受到力的作用时，总保持静止状态或匀速直线运动状态。</p>
    <p><strong>惯性</strong>：物体保持原来运动状态不变的性质。惯性大小只与<strong>质量</strong>有关，质量越大，惯性越大。</p>
    <p>惯性是物体的固有属性，不是力，不能说"受到惯性"。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🚀 惯性演示</div>
    <div class="demo-box">
      <canvas id="inertiaCanvas" width="600" height="250"></canvas>
      <div style="margin-top:10px">
        <button class="btn" onclick="setInertia('start')">▶ 启动小车</button>
        <button class="btn btn-ghost" onclick="setInertia('stop')">⏹ 紧急刹车</button>
      </div>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">观察：小车突然停止时，车上的小球由于惯性会继续保持运动</p>
    </div>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：行驶中的汽车突然刹车，乘客会向前倾倒，这是什么原因？</div>
      <div class="a">
        <strong>解：</strong>汽车刹车时，乘客的下半身随汽车一起减速，但上半身由于<strong style="color:var(--success)">惯性</strong>要保持原来的运动状态，所以向前倾倒。
        <div class="step">惯性：物体保持原来运动状态的性质。不是力，不能说"受到惯性"。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：为什么汽车超载容易发生交通事故？</div>
      <div class="a">
        <strong>解：</strong>超载后汽车的总质量增大，<strong style="color:var(--success)">惯性</strong>变大。刹车时更难改变运动状态，制动距离变长，容易发生事故。
        <div class="step">惯性大小只与质量有关：质量越大，惯性越大，运动状态越难改变。</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：跳远运动员为什么要助跑？</div>
      <div class="a">
        <strong>解：</strong>助跑使运动员起跳前具有一定的速度。起跳后，运动员由于<strong style="color:var(--success)">惯性</strong>要保持原来的运动状态，继续向前运动，从而跳得更远。
        <div class="step">利用惯性：起跳前获得速度，起跳后惯性使人继续向前运动。</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch5-quiz">
    <div class="quiz-title">🎯 随堂测验 — 牛顿第一定律</div>
    <div class="quiz-question"><strong>Q1.</strong> 关于牛顿第一定律，下列说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。牛顿第一定律描述的是不受力时的状态，现实中完全不受力很难实现。')">A. 不受力的物体是不存在的，所以牛顿第一定律没有实际意义</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！不受力时，静止的保持静止，运动的保持匀速直线运动。')">B. 不受力时，静止的物体保持静止，运动的物体保持匀速直线运动</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。惯性不是力，不能说"受到惯性"。')">C. 运动的物体是因为受到惯性才继续运动</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 下列现象中，不属于利用惯性的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。跳远助跑利用了惯性。')">A. 跳远运动员助跑</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！系安全带是为了防止惯性带来的危害，不是利用惯性。')">B. 汽车前排乘客系安全带</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。拍打衣服除尘是利用灰尘的惯性。')">C. 拍打衣服除尘</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 同一辆汽车，满载时比空载时更难刹车，这是因为？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。惯性大小与速度无关，只与质量有关。')">A. 满载时速度更大</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！惯性大小只与质量有关，满载时质量大，惯性大，运动状态更难改变。')">B. 满载时质量更大，惯性更大</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。惯性不是力。')">C. 满载时受到的阻力更小</button>
    </div>
    <div class="quiz-feedback" id="ch5-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(4)">← 上一单元</button>
    <button class="btn" onclick="goTo(6)">下一单元 →</button>
  </div>
</div>'''

unit6 = '''<div class="card hidden" id="ch6">
  <div class="card-header">
    <h2>📋 公式与要点总结</h2>
    <span class="chapter-num">第 6 / 6 节</span>
  </div>

  <div class="formula-box" style="text-align:left;font-size:15px">
    <p>🏃 <strong>速度公式：</strong>v = s / t</p>
    <p style="margin-top:12px">💪 <strong>力的三要素：</strong>大小、方向、作用点</p>
    <p style="margin-top:12px">🌍 <strong>重力公式：</strong>G = mg （g ≈ 9.8 N/kg）</p>
    <p style="margin-top:12px">🌀 <strong>弹簧原理：</strong>弹性限度内，伸长量与拉力成正比</p>
    <p style="margin-top:12px">🚀 <strong>牛顿第一定律：</strong>不受力时，静止保持静止，运动保持匀速直线运动</p>
  </div>

  <div class="concept-box">
    <div class="label">易错警示</div>
    <p>❌ "惯性力"——惯性不是力，不能说"受到惯性"</p>
    <p>❌ 重力的方向"垂直向下"——应该是"竖直向下"</p>
    <p>❌ 质量与重力混淆——质量是 kg，重力是 N；质量不随位置变化，重力随 g 变化</p>
    <p>❌ 弹力产生条件——必须发生弹性形变，塑性形变不产生弹力</p>
  </div>

  <div class="quiz-box" id="ch6-quiz">
    <div class="quiz-title">🎯 本章综合测试</div>
    <div class="quiz-question"><strong>Q1.</strong> 下列说法正确的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。惯性只与质量有关，与速度无关。')">A. 速度越大，惯性越大</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！重力 G=mg，同一地点 g 相同，G 与 m 成正比。')">B. 物体受到的重力与质量成正比</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。质量是固有属性，不随位置变化。')">C. 物体到月球上质量变小</button>
    </div>
    <div class="quiz-feedback" id="ch6-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 弹簧测力计示数为 10 N，下面挂的物体重力为 10 N，该物体的质量约为？（g 取 10 N/kg）</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。m = G/g = 10/10 = 1 kg。')">A. 10 kg</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！m = G/g = 10÷10 = 1 kg。')">B. 1 kg</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。m = G/g = 10/10 = 1 kg。')">C. 100 kg</button>
    </div>
    <div class="quiz-feedback" id="ch6-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 下列事例中，为了增大摩擦的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！轮胎花纹增大粗糙程度，增大摩擦。')">A. 轮胎有花纹</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。加润滑油是减小摩擦。')">B. 给轴承加润滑油</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。气垫船是使接触面分离，减小摩擦。')">C. 气垫船</button>
    </div>
    <div class="quiz-feedback" id="ch6-fb3"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q4.</strong> 汽车突然刹车时，乘客向前倾的原因是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。不能说"受到惯性"，惯性不是力。')">A. 乘客受到惯性</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！乘客上半身由于惯性保持原来的运动状态，所以向前倾。')">B. 乘客上半身具有惯性</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。不是受到向前的力，而是惯性。')">C. 乘客受到向前的力</button>
    </div>
    <div class="quiz-feedback" id="ch6-fb4"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-ghost" onclick="goTo(5)">← 上一单元</button>
    <a class="btn btn-warn" href="game.html">🎮 挑战模式 →</a>
  </div>
</div>'''

print(f"Unit 2: {len(unit2)} bytes")
print(f"Unit 3: {len(unit3)} bytes")
print(f"Unit 4: {len(unit4)} bytes")
print(f"Unit 5: {len(unit5)} bytes")
print(f"Unit 6: {len(unit6)} bytes")

# Save for assembly
with open('part2.py', 'w') as f:
    f.write(f'unit2 = """{unit2}"""\n')
    f.write(f'unit3 = """{unit3}"""\n')
    f.write(f'unit4 = """{unit4}"""\n')
    f.write(f'unit5 = """{unit5}"""\n')
    f.write(f'unit6 = """{unit6}"""\n')

print("Saved to part2.py")
