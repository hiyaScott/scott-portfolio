import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改 GAMES 标题位置和透明度
# 位置改为紧贴顶部导航（90px，在70px header下方一点点）
# 透明度改为 0.8
content = content.replace(
    '''/* GAMES Text - Fixed background title */
        .games-text {
            font-size: clamp(80px, 15vw, 180px);
            font-weight: 800;
            letter-spacing: -8px;
            color: rgba(0, 0, 0, 0.06); /* 几乎透明，作为背景 */
            line-height: 1;
            text-align: center;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1; /* 在卡片下方 */
            pointer-events: none; /* 不阻挡交互 */
        }''',
    '''/* GAMES Text - Fixed background title */
        .games-text {
            font-size: clamp(80px, 15vw, 180px);
            font-weight: 800;
            letter-spacing: -8px;
            color: rgba(0, 0, 0, 0.8); /* 0.8透明度 */
            line-height: 1;
            text-align: center;
            position: fixed;
            top: 90px; /* 紧贴顶部导航 */
            left: 50%;
            transform: translateX(-50%);
            z-index: 1; /* 在卡片下方 */
            pointer-events: none; /* 不阻挡交互 */
        }'''
)

# 2. 添加鼠标/手指离开屏幕时的重置逻辑
# 找到现有的 touchmove 事件，在后面添加 touchend 和 mouseleave
old_touch = '''        // Touch support
        document.addEventListener('touchmove', (e) => {
            if (e.touches.length > 0) {
                targetMouseX = e.touches[0].clientX;
                targetMouseY = e.touches[0].clientY;
            }
        }, { passive: true });'''

new_touch = '''        // Touch support
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
        
        document.addEventListener('touchend', () => {
            targetMouseX = window.innerWidth / 2;
            targetMouseY = window.innerHeight / 2;
        });'''

content = content.replace(old_touch, new_touch)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')
