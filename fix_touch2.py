import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 彻底重写触摸重置逻辑，使用更可靠的方法
old_touch_logic = '''        // Touch support
        document.addEventListener('touchmove', (e) => {
            if (e.touches.length > 0) {
                targetMouseX = e.touches[0].clientX;
                targetMouseY = e.touches[0].clientY;
            }
        }, { passive: true });
        
        // Reset when mouse/touch leaves screen
        document.addEventListener('mouseleave', () => {
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        });
        
        // Touch end/cancel for mobile - reset to center
        const resetToCenter = () => {
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        };
        
        document.addEventListener('touchend', resetToCenter, { passive: true });
        document.addEventListener('touchcancel', resetToCenter, { passive: true });
        
        // Also reset when all touches end (backup)
        let lastTouchTime = 0;
        document.addEventListener('touchstart', () => { lastTouchTime = Date.now(); }, { passive: true });
        
        setInterval(() => {
            // If no touch for 100ms, consider it ended
            if (Date.now() - lastTouchTime > 100 && lastTouchTime > 0) {
                if (targetMouseX !== window.innerWidth / 2) {
                    resetToCenter();
                }
            }
        }, 50);'''

new_touch_logic = '''        // Touch support - improved mobile detection
        let isTouching = false;
        
        document.addEventListener('touchstart', (e) => {
            isTouching = true;
            if (e.touches.length > 0) {
                targetMouseX = e.touches[0].clientX;
                targetMouseY = e.touches[0].clientY;
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            isTouching = true;
            if (e.touches.length > 0) {
                targetMouseX = e.touches[0].clientX;
                targetMouseY = e.touches[0].clientY;
            }
        }, { passive: true });
        
        // Reset when touch ends - check all touch end types
        const resetToCenter = () => {
            isTouching = false;
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        };
        
        document.addEventListener('touchend', (e) => {
            if (e.touches.length === 0) resetToCenter();
        }, { passive: true });
        
        document.addEventListener('touchcancel', (e) => {
            if (e.touches.length === 0) resetToCenter();
        }, { passive: true });
        
        // Mouse support for desktop
        document.addEventListener('mousemove', (e) => {
            if (!isTouching) {
                targetMouseX = e.clientX;
                targetMouseY = e.clientY;
            }
        });
        
        document.addEventListener('mouseleave', resetToCenter);'''

content = content.replace(old_touch_logic, new_touch_logic)

# 2. 减小卡片容器初始位置 - 从 200px 改为 150px
content = content.replace(
    'margin-top: 200px; /* 略低于 GAMES 标题 */',
    'margin-top: 150px; /* 紧贴 GAMES 标题下方 */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')