/**
 * C++ 课程网站 - 核心逻辑
 * 支持：课程列表渲染、筛选、详情页加载、上下课导航
 */

(function () {
  'use strict';

  // ===== 状态 =====
  let coursesData = { courses: [] };
  let currentCourseId = null;

  // ===== 工具函数 =====
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  function getParam(name) {
    return new URLSearchParams(location.search).get(name);
  }

  // ===== 加载课程数据 =====
  async function loadCourses() {
    try {
      const res = await fetch('data/courses.json');
      if (!res.ok) throw new Error('加载失败');
      coursesData = await res.json();
      return coursesData;
    } catch (e) {
      console.error('课程数据加载失败:', e);
      return { courses: [] };
    }
  }

  // ===== 首页：渲染课程列表（按部分分组）=====
  function renderCourseList(filterLevel = 'all') {
    const container = $('#courseGroups');
    if (!container) return;

    const courses = coursesData.courses || [];
    const filtered = filterLevel === 'all'
      ? courses
      : courses.filter(c => c.level === filterLevel);

    if (filtered.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>暂无该分类的课程</p>
        </div>
      `;
      return;
    }

    // 按 part 分组
    const groups = {};
    filtered.forEach(c => {
      const part = c.part || '未分类';
      if (!groups[part]) groups[part] = [];
      groups[part].push(c);
    });

    // 保持原始顺序
    const orderedParts = [];
    courses.forEach(c => {
      if (!orderedParts.includes(c.part)) orderedParts.push(c.part);
    });

    container.innerHTML = orderedParts
      .filter(part => groups[part] && groups[part].length > 0)
      .map(part => `
        <section class="course-group">
          <h3 class="group-title">${escapeHtml(part)}</h3>
          <div class="course-grid">
            ${groups[part].map(c => renderCard(c)).join('')}
          </div>
        </section>
      `).join('');
  }

  // ===== 题目完成状态管理（按洛谷题号，全局共享）=====
  function getDoneProblems() {
    try {
      return JSON.parse(localStorage.getItem('cpp_done_problems') || '{}');
    } catch (e) {
      return {};
    }
  }

  function saveDoneProblems(done) {
    localStorage.setItem('cpp_done_problems', JSON.stringify(done));
  }

  function isProblemDone(problemId) {
    return !!getDoneProblems()[problemId];
  }

  function setProblemDone(problemId, done) {
    const data = getDoneProblems();
    if (done) {
      data[problemId] = Date.now();
    } else {
      delete data[problemId];
    }
    saveDoneProblems(data);
  }

  // 统计一门课的练习题完成情况
  function getExerciseStats(course) {
    const ex = course && course.exercises;
    if (!ex) return { total: 0, done: 0 };
    const doneMap = getDoneProblems();
    let total = 0, done = 0;
    ['basic', 'practice', 'advanced'].forEach(k => {
      (ex[k] || []).forEach(item => {
        total++;
        if (doneMap[item.id]) done++;
      });
    });
    return { total, done };
  }

  // ===== 二次确认对话框 =====
  let confirmCallback = null;

  function showConfirmDialog(title, message, onConfirm, options) {
    const dialog = $('#confirmDialog');
    const titleEl = $('#confirmDialogTitle');
    const msgEl = $('#confirmDialogMessage');
    const confirmBtn = $('#confirmDialogConfirmBtn');

    if (!dialog || !titleEl || !msgEl || !confirmBtn) return;

    titleEl.textContent = title;
    msgEl.textContent = message;
    confirmCallback = onConfirm;

    // 移除旧事件，绑定新事件
    const newBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
    newBtn.className = 'confirm-dialog-btn confirm-dialog-confirm' + (options && options.danger ? ' danger' : '');
    newBtn.addEventListener('click', () => {
      const cb = confirmCallback;
      closeConfirmDialog();
      if (cb) cb();
    });

    dialog.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }

  window.closeConfirmDialog = function () {
    const dialog = $('#confirmDialog');
    if (dialog) dialog.style.display = 'none';
    document.body.style.overflow = '';
    confirmCallback = null;
  };

  // ===== 切换题目完成状态（勾选/取消均需二次确认）=====
  window.toggleProblemDone = function (event, problemId) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    if (!problemId) return;

    if (isProblemDone(problemId)) {
      showConfirmDialog(
        '取消完成标记',
        `确定要取消【${problemId}】的完成标记吗？`,
        () => {
          setProblemDone(problemId, false);
          refreshExerciseUI();
          refreshWalkthroughUI();
        },
        { danger: true }
      );
    } else {
      showConfirmDialog(
        '确认完成',
        `确定要将【${problemId}】标记为已完成吗？`,
        () => {
          setProblemDone(problemId, true);
          refreshExerciseUI();
          refreshWalkthroughUI();
        }
      );
    }
  };

  // 刷新练习题列表 + 进度显示
  function refreshExerciseUI() {
    const courses = coursesData.courses || [];
    const course = courses.find(c => c.id === currentCourseId);
    if (course) {
      renderExercises(course);
      updateExerciseProgressUI(course);
    }
  }

  // 更新"本课练习"进度条
  function updateExerciseProgressUI(course) {
    const section = $('#exerciseProgressSection');
    const countEl = $('#exerciseProgressCount');
    const barEl = $('#exerciseProgressBar');
    if (!section || !countEl || !barEl) return;

    const { total, done } = getExerciseStats(course);
    if (total === 0) {
      section.style.display = 'none';
      return;
    }

    section.style.display = 'block';
    countEl.textContent = `${done} / ${total}`;
    const percent = Math.round((done / total) * 100);
    barEl.style.width = percent + '%';
    barEl.classList.toggle('complete', done === total);
  }

  // ===== 首页：渲染课程卡片（带刷题进度）=====
  function renderCard(c) {
    const externalBadge = c.external_video
      ? `<span class="external-badge">🔗 外部视频</span>`
      : '';

    const { total, done } = getExerciseStats(c);
    const progressBadge = total > 0 && done > 0
      ? `<span class="progress-badge${done === total ? ' all-done' : ''}">${done}/${total}</span>`
      : '';

    return `
      <article class="course-card" data-id="${c.id}" onclick="goToCourse('${c.id}')">
        <div class="card-thumbnail">
          <div class="play-icon">▶</div>
          ${externalBadge}
          ${progressBadge}
          <span class="duration">${c.duration}</span>
        </div>
        <div class="card-body">
          <h3 class="card-title">${escapeHtml(c.title)}</h3>
          <p class="card-desc">${escapeHtml(c.description)}</p>
          <div class="card-footer">
            <span class="level-badge" data-level="${c.level}">${c.level}</span>
            <div class="card-tags">
              ${(c.tags || []).map(t => `<span>${escapeHtml(t)}</span>`).join('')}
            </div>
          </div>
        </div>
      </article>
    `;
  }

  // ===== 首页：筛选标签事件 =====
  function initFilters() {
    const tabs = $$('.filter-tabs .tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        renderCourseList(tab.dataset.filter);
      });
    });
  }

  // ===== 详情页：加载课程 =====
  function loadCourseDetail(courseId) {
    const courses = coursesData.courses || [];
    const course = courses.find(c => c.id === courseId);
    if (!course) {
      showNotFound();
      return;
    }

    currentCourseId = courseId;

    // 更新标题
    document.title = `${course.title} - C++ 核心课程`;
    const navTitle = $('#navTitle');
    if (navTitle) navTitle.textContent = course.title;

    // 更新课程信息（右侧栏）
    const titleEl = $('#courseTitle');
    if (titleEl) titleEl.textContent = course.title;

    const levelEl = $('#courseLevel');
    if (levelEl) {
      levelEl.textContent = course.level;
      levelEl.dataset.level = course.level;
    }

    const durEl = $('#courseDuration');
    if (durEl) durEl.textContent = course.duration;

    const descEl = $('#courseDesc');
    if (descEl) descEl.textContent = course.description;

    const tagsEl = $('#courseTags');
    if (tagsEl) {
      tagsEl.innerHTML = (course.tags || []).map(t =>
        `<span>${escapeHtml(t)}</span>`
      ).join('');
    }

    // 更新视频卡片
    const videoCard = $('#videoCard');
    const videoLink = $('#videoLink');
    const videoNote = $('#videoCardNote');

    if (course.external_video) {
      if (videoCard) videoCard.style.display = 'flex';
      if (videoLink) videoLink.href = course.external_video;
      if (videoNote) videoNote.textContent = course.external_note || '点击跳转到视频平台观看';
    } else {
      if (videoCard) videoCard.style.display = 'none';
    }

    // 更新腾讯会议卡片
    const tencentCard = $('#tencentCard');
    const tencentLink = $('#tencentLink');
    const tencentNote = $('#tencentCardNote');
    const resourceTags = $('#resourceTags');

    if (course.tencent_meeting) {
      if (tencentCard) tencentCard.style.display = 'flex';
      if (tencentLink) tencentLink.href = course.tencent_meeting;
      if (tencentNote) tencentNote.textContent = course.tencent_note || '腾讯会议录制';
      if (resourceTags) resourceTags.style.display = 'flex';
    } else {
      if (tencentCard) tencentCard.style.display = 'none';
      if (resourceTags) resourceTags.style.display = 'none';
    }

    // 加载课程纪要
    loadMeetingNotes(courseId);

    // 渲染练习题
    renderExercises(course);

    // 更新本课练习进度
    updateExerciseProgressUI(course);

    // 更新 PDF（左侧主体）
    const pdfFrame = $('#pdfFrame');
    if (pdfFrame) pdfFrame.src = course.pdf;

    const pdfDownload = $('#pdfDownload');
    if (pdfDownload) pdfDownload.href = course.pdf;

    // 渲染导航
    renderLessonNav(courseId, courses);
  }

  // ===== 渲染练习题 =====
  function renderExercises(course) {
    const section = $('#exercisesSection');
    const container = $('#exercisesGroups');
    if (!section || !container) return;

    const ex = course.exercises;
    if (!ex || (!ex.basic && !ex.practice && !ex.advanced)) {
      section.style.display = 'none';
      return;
    }

    section.style.display = 'block';

    const groups = [
      { key: 'basic', label: '⭐ 基础练习', desc: '直接应用课堂知识点' },
      { key: 'practice', label: '⭐⭐ 巩固提升', desc: '需要组合多个知识点' },
      { key: 'advanced', label: '⭐⭐⭐ 挑战拓展', desc: '灵活运用，需要思考' }
    ];

    container.innerHTML = groups.map(g => {
      const items = ex[g.key] || [];
      if (items.length === 0) return '';
      return `
        <div class="exercise-group">
          <div class="exercise-group-header">
            <span class="exercise-group-label">${g.label}</span>
            <span class="exercise-group-desc">${g.desc}</span>
          </div>
          <div class="exercise-list">
            ${items.map(item => {
              const done = isProblemDone(item.id);
              return `
              <div class="exercise-item${done ? ' done' : ''}" data-pid="${escapeHtml(item.id)}">
                <button type="button"
                        class="exercise-check${done ? ' checked' : ''}"
                        onclick="toggleProblemDone(event, '${escapeHtml(item.id)}')"
                        title="${done ? '已完成，点击取消' : '标记为已完成'}"
                        aria-label="切换完成状态">✓</button>
                <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener" class="exercise-link">
                  <span class="exercise-id">${escapeHtml(item.id)}</span>
                  <span class="exercise-name">${escapeHtml(item.title)}</span>
                  <span class="exercise-arrow">→</span>
                </a>
              </div>
            `;
            }).join('')}
          </div>
        </div>
      `;
    }).join('');
  }

  // ===== 加载课程纪要 =====
  async function loadMeetingNotes(courseId) {
    const notesContainer = $('#meetingNotes');
    if (!notesContainer) return;

    try {
      const res = await fetch('data/meeting-notes.json');
      if (!res.ok) return;
      const notesData = await res.json();
      const notes = notesData[courseId];
      if (!notes) {
        notesContainer.style.display = 'none';
        return;
      }

      notesContainer.style.display = 'block';

      const sourceEl = $('#notesSource');
      if (sourceEl) sourceEl.textContent = `来源：${notes.source} · ${notes.url}`;

      const summaryEl = $('#notesSummary');
      if (summaryEl) summaryEl.textContent = notes.summary;

      const sectionsEl = $('#notesSections');
      if (sectionsEl) {
        sectionsEl.innerHTML = (notes.sections || []).map(section => `
          <div class="notes-section">
            <div class="notes-section-title">
              ${escapeHtml(section.title)}
              <span class="notes-section-time">${escapeHtml(section.time)}</span>
            </div>
            ${(section.items || []).map(item => `
              <div class="notes-item">
                <div class="notes-item-subtitle">${escapeHtml(item.subtitle)}</div>
                <div class="notes-item-content">${escapeHtml(item.content)}</div>
              </div>
            `).join('')}
          </div>
        `).join('');
      }

      // 绑定展开/收起
      const toggle = $('#notesToggle');
      if (toggle) {
        toggle.addEventListener('click', () => {
          notesContainer.classList.toggle('open');
          const content = $('#notesContent');
          if (content) {
            content.style.display = notesContainer.classList.contains('open') ? 'block' : 'none';
          }
        });
      }
    } catch (e) {
      console.error('纪要加载失败:', e);
      notesContainer.style.display = 'none';
    }
  }

  // ===== 详情页：上下课导航 =====
  function renderLessonNav(currentId, courses) {
    const nav = $('#lessonNav');
    if (!nav) return;

    const idx = courses.findIndex(c => c.id === currentId);
    const prev = idx > 0 ? courses[idx - 1] : null;
    const next = idx < courses.length - 1 ? courses[idx + 1] : null;
    const currentNum = idx + 1;
    const total = courses.length;

    nav.innerHTML = `
      <button class="lesson-nav-btn" onclick="goToCourse('${prev ? prev.id : ''}')" ${!prev ? 'disabled' : ''}>
        <span>←</span>
        <div>
          <div class="label">上一课</div>
          <div class="title">${prev ? escapeHtml(prev.title) : '没有了'}</div>
        </div>
      </button>

      <span class="lesson-nav-center">${currentNum} / ${total}</span>

      <button class="lesson-nav-btn" onclick="goToCourse('${next ? next.id : ''}')" ${!next ? 'disabled' : ''}>
        <div style="text-align: right;">
          <div class="label">下一课</div>
          <div class="title">${next ? escapeHtml(next.title) : '没有了'}</div>
        </div>
        <span>→</span>
      </button>
    `;
  }

  // ===== 404 =====
  function showNotFound() {
    const main = $('.course-main') || $('.wt-content') || document.body;
    if (main) {
      main.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1; padding-top: 120px;">
          <h2 style="margin-bottom: 12px;">内容未找到</h2>
          <p>该内容不存在或已被移除</p>
          <br>
          <a href="index.html" style="color: var(--accent);">← 返回课程列表</a>
        </div>
      `;
    }
  }

  // ============================================================
  // 习题讲解板块
  // ============================================================
  let walkthroughsCache = null;
  let currentWalkthrough = null; // { meta, parsed }

  window.goToWalkthrough = function (id) {
    if (!id) return;
    location.href = `walkthrough.html?id=${id}`;
  };

  // ----- 首页：板块切换 -----
  function initBoards() {
    const tabs = $$('.board-tab');
    if (!tabs.length) return;
    const saved = localStorage.getItem('cpp_home_board') || 'courses';
    switchBoard(saved, false);
    tabs.forEach(tab => {
      tab.addEventListener('click', () => switchBoard(tab.dataset.board, true));
    });
  }

  function switchBoard(board, save) {
    $$('.board-tab').forEach(t => t.classList.toggle('active', t.dataset.board === board));
    const coursesBoard = $('#boardCourses');
    const wtBoard = $('#boardWalkthrough');
    if (coursesBoard) coursesBoard.style.display = board === 'courses' ? 'block' : 'none';
    if (wtBoard) wtBoard.style.display = board === 'walkthrough' ? 'block' : 'none';
    if (save) localStorage.setItem('cpp_home_board', board);
    if (board === 'walkthrough') renderWalkthroughCards();
  }

  // ----- 首页：渲染习题讲解卡片 -----
  async function renderWalkthroughCards() {
    const grid = $('#walkthroughGrid');
    if (!grid) return;

    if (!walkthroughsCache) {
      try {
        const res = await fetch('data/walkthroughs.json');
        walkthroughsCache = res.ok ? await res.json() : { walkthroughs: [] };
      } catch (e) {
        walkthroughsCache = { walkthroughs: [] };
      }
    }

    const list = walkthroughsCache.walkthroughs || [];
    if (list.length === 0) {
      grid.innerHTML = `<div class="empty-state"><p>暂无习题讲解</p></div>`;
      return;
    }

    const cards = await Promise.all(list.map(async w => {
      let pids = [];
      try {
        const res = await fetch(w.md);
        if (res.ok) {
          const md = await res.text();
          pids = [...md.matchAll(/^##\s+\d+\.\s*(P\d+)/gm)].map(m => m[1]);
        }
      } catch (e) { /* 忽略，进度显示 0 */ }

      const done = pids.filter(pid => isProblemDone(pid)).length;
      const total = pids.length;
      const progressBadge = total > 0 && done > 0
        ? `<span class="progress-badge${done === total ? ' all-done' : ''}">${done}/${total}</span>`
        : '';

      return `
        <article class="course-card" data-id="${w.id}" onclick="goToWalkthrough('${w.id}')">
          <div class="card-thumbnail wt-thumbnail">
            <span class="wt-thumbnail-icon">📒</span>
            <span class="wt-thumbnail-date">${formatWtDate(w.date)}</span>
            ${progressBadge}
          </div>
          <div class="card-body">
            <h3 class="card-title">${escapeHtml(w.title)}</h3>
            <p class="card-desc">${escapeHtml(w.intro)}</p>
            <div class="card-footer">
              <span class="level-badge" data-level="综合">习题讲解</span>
              <div class="card-tags">
                ${pids.slice(0, 5).map(pid => `<span>${pid}</span>`).join('')}
                ${total > 5 ? `<span>共${total}题</span>` : ''}
              </div>
            </div>
          </div>
        </article>
      `;
    }));

    grid.innerHTML = cards.join('');
  }

  function formatWtDate(d) {
    const m = String(d || '').match(/(\d{4})-(\d{2})-(\d{2})/);
    return m ? `${parseInt(m[2], 10)}月${parseInt(m[3], 10)}日` : (d || '');
  }

  // ----- 习题讲解详情页 -----
  async function loadWalkthroughDetail(id) {
    try {
      const res = await fetch('data/walkthroughs.json');
      if (!res.ok) throw new Error('清单加载失败');
      const data = await res.json();
      const wt = (data.walkthroughs || []).find(w => w.id === id);
      if (!wt) { showNotFound(); return; }

      const mdRes = await fetch(wt.md);
      if (!mdRes.ok) throw new Error('讲义加载失败');
      const md = await mdRes.text();

      const parsed = parseWalkthrough(md);
      currentWalkthrough = { meta: wt, parsed };
      renderWalkthrough(wt, parsed);
    } catch (e) {
      console.error('习题讲解加载失败:', e);
      showNotFound();
    }
  }

  // 解析 markdown：题号分节 + 小结 + 开头引言
  function parseWalkthrough(md) {
    let lines = md.replace(/\r\n/g, '\n').split('\n');
    if (lines.length && /^#\s+/.test(lines[0])) lines = lines.slice(1);
    while (lines.length && lines[0].trim() === '') lines.shift();

    const intro = [];
    const problems = [];
    let summary = null;
    let cur = intro;

    lines.forEach(line => {
      const pm = line.match(/^##\s+(\d+)\.\s*(P\d+)\s+(.+)$/);
      if (pm) {
        cur = { num: pm[1], pid: pm[2], title: pm[3].trim(), anchor: 'problem-' + pm[1], lines: [] };
        problems.push(cur);
        return;
      }
      if (/^##\s+/.test(line)) {
        cur = { title: line.replace(/^##\s+/, '').trim(), anchor: 'summary', lines: [] };
        summary = cur;
        return;
      }
      if (Array.isArray(cur)) cur.push(line);
      else cur.lines.push(line);
    });

    return { intro, problems, summary };
  }

  function renderWalkthrough(wt, parsed) {
    document.title = `${wt.title} - 习题讲解`;
    const navTitle = $('#navTitle');
    if (navTitle) navTitle.textContent = '习题讲解';

    const dateEl = $('#wtDate');
    if (dateEl) dateEl.textContent = formatWtDate(wt.date);
    const titleEl = $('#wtTitle');
    if (titleEl) titleEl.textContent = wt.title;
    const introEl = $('#wtIntro');
    if (introEl) introEl.textContent = wt.intro;

    const nav = $('#wtNav');
    if (nav) {
      nav.innerHTML = parsed.problems.map(p => `
        <a class="wt-chip" href="#${p.anchor}">
          <span class="wt-chip-pid">${p.pid}</span>${escapeHtml(p.title)}
        </a>
      `).join('');
    }

    const sections = parsed.problems.map(p => {
      const done = isProblemDone(p.pid);
      return `
        <section class="wt-problem" id="${p.anchor}">
          <div class="wt-problem-header">
            <button type="button"
                    class="exercise-check wt-check${done ? ' checked' : ''}"
                    onclick="toggleProblemDone(event, '${p.pid}')"
                    title="${done ? '已完成，点击取消' : '标记为已完成'}"
                    aria-label="切换完成状态">✓</button>
            <h2 class="wt-problem-title">${p.num}. <span class="wt-problem-pid">${p.pid}</span> ${escapeHtml(p.title)}</h2>
            <a class="wt-luogu-btn" href="https://www.luogu.com.cn/problem/${p.pid}" target="_blank" rel="noopener">洛谷 ↗</a>
          </div>
          <div class="wt-problem-body">
            ${renderMarkdown(p.lines)}
          </div>
        </section>
      `;
    });

    if (parsed.summary) {
      sections.push(`
        <section class="wt-problem wt-summary" id="summary">
          <h2 class="wt-problem-title">${escapeHtml(parsed.summary.title)}</h2>
          <div class="wt-problem-body">${renderMarkdown(parsed.summary.lines)}</div>
        </section>
      `);
    }

    const content = $('#wtContent');
    if (content) content.innerHTML = sections.join('\n');
    updateWtProgress();
  }

  function updateWtProgress() {
    if (!currentWalkthrough) return;
    const bar = $('#wtProgressBar');
    const count = $('#wtProgressCount');
    if (!bar || !count) return;
    const problems = currentWalkthrough.parsed.problems;
    const total = problems.length;
    const done = problems.filter(p => isProblemDone(p.pid)).length;
    count.textContent = `${done} / ${total}`;
    bar.style.width = total ? Math.round((done / total) * 100) + '%' : '0%';
    bar.classList.toggle('complete', total > 0 && done === total);
  }

  // 勾选后原地刷新（不重排页面）
  function refreshWalkthroughUI() {
    if (!currentWalkthrough) return;
    currentWalkthrough.parsed.problems.forEach(p => {
      const sec = document.getElementById(p.anchor);
      if (!sec) return;
      const done = isProblemDone(p.pid);
      const btn = sec.querySelector('.exercise-check');
      if (btn) {
        btn.classList.toggle('checked', done);
        btn.title = done ? '已完成，点击取消' : '标记为已完成';
      }
    });
    updateWtProgress();
  }

  // ----- 极简 Markdown 渲染（行状态机，兼容移动端）-----
  function renderMarkdown(lines) {
    const html = [];
    let i = 0;
    let para = [];

    const flushPara = () => {
      if (para.length) {
        html.push(`<p>${para.join('<br>')}</p>`);
        para = [];
      }
    };

    while (i < lines.length) {
      const line = lines[i];
      const t = line.trim();

      if (t === '') { flushPara(); i++; continue; }
      if (t === '---') { flushPara(); html.push('<hr>'); i++; continue; }
      if (/^###\s+/.test(t)) { flushPara(); html.push(`<h3>${renderInline(t.replace(/^###\s+/, ''))}</h3>`); i++; continue; }
      if (/^##\s+/.test(t)) { flushPara(); html.push(`<h2>${renderInline(t.replace(/^##\s+/, ''))}</h2>`); i++; continue; }
      if (/^```/.test(t)) {
        flushPara();
        const code = [];
        i++;
        while (i < lines.length && !/^```/.test(lines[i].trim())) { code.push(lines[i]); i++; }
        i++; // 跳过结束 ```
        html.push(renderCodeBlock(code.join('\n')));
        continue;
      }
      if (t.startsWith('|')) {
        flushPara();
        const tbl = [];
        while (i < lines.length && lines[i].trim().startsWith('|')) { tbl.push(lines[i]); i++; }
        html.push(renderTable(tbl));
        continue;
      }
      if (/^[-*]\s+/.test(t)) {
        flushPara();
        const items = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) {
          items.push(lines[i].trim().replace(/^[-*]\s+/, ''));
          i++;
        }
        html.push(`<ul>${items.map(it => `<li>${renderInline(it)}</li>`).join('')}</ul>`);
        continue;
      }
      if (/^\d+\.\s+/.test(t)) {
        flushPara();
        const items = [];
        while (i < lines.length && /^\d+\.\s+/.test(lines[i].trim())) {
          items.push(lines[i].trim().replace(/^\d+\.\s+/, ''));
          i++;
        }
        html.push(`<ol>${items.map(it => `<li>${renderInline(it)}</li>`).join('')}</ol>`);
        continue;
      }

      para.push(renderInline(t));
      i++;
    }
    flushPara();
    return html.join('\n');
  }

  function renderInline(text) {
    let s = escapeHtml(text);
    // markdown 图片：懒加载 + 宽高比防跳动（渲染为块级，独立于段落）
    s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g,
      '<img class="md-img" src="$2" alt="$1" loading="lazy" decoding="async">');
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return s;
  }

  // C++ 代码块：注释高亮（这些讲义每行都有中文注释，高亮注释最提可读性）
  function renderCodeBlock(code) {
    const escaped = escapeHtml(code)
      .replace(/(\/\/[^\n]*)/g, '<span class="code-comment">$1</span>');
    return `<pre class="code-block"><code>${escaped}</code></pre>`;
  }

  function renderTable(rows) {
    const parse = r => r.trim().replace(/^\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
    const isSep = r => /^\|[\s\-|:]+\|?$/.test(r.trim());
    const header = parse(rows[0]);
    const body = rows.slice(1).filter(r => !isSep(r));
    return `<div class="table-wrap"><table>
      <thead><tr>${header.map(h => `<th>${renderInline(h)}</th>`).join('')}</tr></thead>
      <tbody>${body.map(r => `<tr>${parse(r).map(c => `<td>${renderInline(c)}</td>`).join('')}</tr>`).join('')}</tbody>
    </table></div>`;
  }

  // ===== HTML 转义 =====
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ===== 全局跳转 =====
  window.goToCourse = function (id) {
    if (!id) return;
    location.href = `course.html?id=${id}`;
  };

  // ===== 主题切换 =====
  function initTheme() {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    setTheme(theme);
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    const btn = $('#themeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    setTheme(current === 'dark' ? 'light' : 'dark');
  }

  // ===== 初始化 =====
  async function init() {
    initTheme();

    const themeBtn = $('#themeToggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    await loadCourses();

    const page = location.pathname.split('/').pop();

    if (page === 'index.html' || page === '' || page === '/') {
      // 首页
      renderCourseList();
      initFilters();
      initBoards();
    } else if (page === 'course.html') {
      // 详情页
      const id = getParam('id');
      if (id) {
        loadCourseDetail(id);
      } else {
        showNotFound();
      }
    } else if (page === 'walkthrough.html') {
      // 习题讲解详情页
      const id = getParam('id');
      if (id) {
        loadWalkthroughDetail(id);
      } else {
        showNotFound();
      }
    }
  }

  // DOM 就绪后启动
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
