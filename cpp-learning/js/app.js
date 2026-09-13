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

  function renderCard(c) {
    const externalBadge = c.external_video
      ? `<span class="external-badge">🔗 外部视频</span>`
      : '';

    return `
      <article class="course-card" data-id="${c.id}" onclick="goToCourse('${c.id}')">
        <div class="card-thumbnail">
          <div class="play-icon">▶</div>
          ${externalBadge}
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

    // 更新视频
    const localBox = $('#localVideoBox');
    const externalBox = $('#externalVideoBox');
    const externalLink = $('#externalVideoLink');
    const externalNote = $('#externalVideoNote');

    if (course.external_video) {
      // 外部视频模式 - iframe 嵌入
      if (localBox) localBox.style.display = 'none';
      if (externalBox) externalBox.style.display = 'flex';
      const frame = $('#externalVideoFrame');
      if (frame) frame.src = course.external_video;
      if (externalLink) {
        externalLink.href = course.external_video;
        externalLink.style.display = 'inline';
      }
      if (externalNote) externalNote.textContent = course.external_note || '';
    } else {
      // 本地视频模式
      if (localBox) localBox.style.display = 'block';
      if (externalBox) externalBox.style.display = 'none';
      if (externalLink) externalLink.style.display = 'none';
      const video = $('#courseVideo');
      if (video) {
        const source = video.querySelector('source');
        source.src = course.video;
        video.poster = course.poster || '';
        video.load();
      }
    }

    // 更新信息
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

    // 更新 PDF
    const pdfFrame = $('#pdfFrame');
    if (pdfFrame) pdfFrame.src = course.pdf;

    const pdfDownload = $('#pdfDownload');
    if (pdfDownload) pdfDownload.href = course.pdf;

    // 渲染导航
    renderLessonNav(courseId, courses);
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
    const main = $('.course-main');
    if (main) {
      main.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1; padding-top: 120px;">
          <h2 style="margin-bottom: 12px;">课程未找到</h2>
          <p>该课程不存在或已被移除</p>
          <br>
          <a href="index.html" style="color: var(--accent);">← 返回课程列表</a>
        </div>
      `;
    }
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

  // ===== 初始化 =====
  async function init() {
    await loadCourses();

    const page = location.pathname.split('/').pop();

    if (page === 'index.html' || page === '' || page === '/') {
      // 首页
      renderCourseList();
      initFilters();
    } else if (page === 'course.html') {
      // 详情页
      const id = getParam('id');
      if (id) {
        loadCourseDetail(id);
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
