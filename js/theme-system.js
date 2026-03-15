/**
 * DeepSpace / Daylight 全局主题系统
 * 
 * 功能：
 * - 自动从 localStorage 读取主题偏好
 * - 提供 toggleTheme() 全局切换函数
 * - 跨页面主题同步
 * 
 * 使用方法：
 * 1. 在 HTML 中引入：
 *    <script src="/js/theme-system.js"></script>
 * 
 * 2. 添加切换按钮（自动初始化）：
 *    <button class="theme-toggle-btn" onclick="toggleTheme()">
 *      <span id="theme-icon">🌑</span>
 *    </button>
 * 
 * 3. 或者使用自动注入的浮动按钮（如果不存在则创建）
 */

(function() {
    'use strict';
    
    const THEME_KEY = 'scott-portfolio-theme';
    const THEMES = {
        DARK: 'dark',
        LIGHT: 'daylight'
    };
    
    // 获取当前主题
    function getCurrentTheme() {
        return localStorage.getItem(THEME_KEY) || THEMES.DARK;
    }
    
    // 设置主题
    function setTheme(theme) {
        const body = document.body;
        const icon = document.getElementById('theme-icon') || document.getElementById('themeIcon');
        const text = document.getElementById('theme-text') || document.getElementById('themeText');
        
        if (theme === THEMES.LIGHT) {
            body.classList.add('daylight');
            if (icon) icon.textContent = '☀️';
            if (text) text.textContent = '白昼';
        } else {
            body.classList.remove('daylight');
            if (icon) icon.textContent = '🌑';
            if (text) text.textContent = '深空';
        }
        
        localStorage.setItem(THEME_KEY, theme);
        
        // 触发自定义事件，供其他脚本监听
        window.dispatchEvent(new CustomEvent('themechange', { 
            detail: { theme: theme } 
        }));
    }
    
    // 切换主题
    function toggleTheme() {
        const current = getCurrentTheme();
        const next = current === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
        setTheme(next);
    }
    
    // 初始化主题
    function initTheme() {
        const savedTheme = getCurrentTheme();
        setTheme(savedTheme);
    }
    
    // 创建浮动主题切换按钮（如果页面中没有）
    function createFloatingToggle() {
        // 检查是否已存在主题切换按钮
        if (document.querySelector('.theme-toggle, .theme-toggle-btn, #theme-toggle')) {
            return;
        }
        
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle-floating';
        toggle.innerHTML = '<span id="theme-icon">🌑</span>';
        toggle.onclick = toggleTheme;
        toggle.title = '切换主题';
        
        // 样式 - 避开顶部固定栏（如音乐控制台）
        toggle.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--bg-card, #1a1a2e);
            border: 1px solid var(--border-default, #333);
            color: var(--text-primary, #fff);
            font-size: 20px;
            cursor: pointer;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        `;
        
        toggle.addEventListener('mouseenter', () => {
            toggle.style.transform = 'scale(1.1)';
            toggle.style.borderColor = 'var(--accent-cyan, #00ffff)';
        });
        
        toggle.addEventListener('mouseleave', () => {
            toggle.style.transform = 'scale(1)';
            toggle.style.borderColor = 'var(--border-default, #333)';
        });
        
        document.body.appendChild(toggle);
    }
    
    // 监听其他页面的主题变化（通过 storage 事件）
    window.addEventListener('storage', (e) => {
        if (e.key === THEME_KEY) {
            setTheme(e.newValue);
        }
    });
    
    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initTheme();
            createFloatingToggle();
        });
    } else {
        initTheme();
        createFloatingToggle();
    }
    
    // 暴露全局函数
    window.toggleTheme = toggleTheme;
    window.getCurrentTheme = getCurrentTheme;
    window.setTheme = setTheme;
    
})();
