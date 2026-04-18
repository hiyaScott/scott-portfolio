import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修复移动端触摸离开问题 - 添加 touchcancel 和更可靠的 touchend
old_touch_reset = '''        // Reset when mouse/touch leaves screen
        document.addEventListener('mouseleave', () => {
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        });
        
        document.addEventListener('touchend', () => {
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        });'''

new_touch_reset = '''        // Reset when mouse/touch leaves screen
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

content = content.replace(old_touch_reset, new_touch_reset)

# 2. 调整卡片容器初始位置 - 从 40vh 改为 200px（略低于 GAMES 标题）
content = content.replace(
    'margin-top: 40vh; /* 留出空间显示 GAMES 标题 */',
    'margin-top: 200px; /* 略低于 GAMES 标题 */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')