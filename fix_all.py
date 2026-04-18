import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改方块效果: rgb(200,200,200), alpha 0.6→1.0
content = content.replace('rgba(250, 250, 250,', 'rgba(200, 200, 200,')
content = content.replace(
    'const alpha = 0.6 + (this.scale - 1) * 2.0;  // scale 1→1.2, alpha 0.6→1.0',
    'const alpha = 0.6 + (this.scale - 1) * 2.0;  // scale 1→1.2, alpha 0.6→1.0'
)
# 注释已经是正确的

# 2. 确保导航栏和主页完全一致
# 主页的导航链接颜色通常是 rgba(255,255,255,0.8) 或类似
# 用户说"Games变白了"，可能是active状态太白
# 让active状态使用和其他链接一样的颜色，只是稍微亮一点，不要纯白
content = content.replace(
    '.nav-link:hover, .nav-link.active { color: #fff; font-weight: 400; }',
    '.nav-link:hover, .nav-link.active { color: rgba(255,255,255,0.95); }'
)

# 3. 调整主体高度
# min-height与主页一致(100vh相关), max-height支持15张卡片
# 修改hero的最小高度，同时允许扩展
content = content.replace(
    '''.hero {
            min-height: 100vh;''',
    '''.hero {
            min-height: calc(100vh - 70px); /* 减去header */
            height: auto; /* 允许扩展 */
            max-height: none; /* 不限制最大高度 */'''
)

# 4. GAMES标题添加透明度0.6并固定位置
content = content.replace(
    '''/* GAMES Text - Cutout Effect */
        .games-text {
            font-size: clamp(80px, 15vw, 180px);
            font-weight: 800;
            letter-spacing: -8px;
            color: #000;
            line-height: 1;
            text-align: center;
            position: relative;
        }''',
    '''/* GAMES Text - Fixed position with alpha */
        .games-text {
            font-size: clamp(80px, 15vw, 180px);
            font-weight: 800;
            letter-spacing: -8px;
            color: rgba(0, 0, 0, 0.6); /* 0.6 alpha */
            line-height: 1;
            text-align: center;
            position: sticky;
            top: 100px; /* 固定在顶部下方 */
            z-index: 10;
        }'''
)

# 5. 调整games-mask-container以支持sticky定位
content = content.replace(
    '''/* GAMES Letter Mask Container */
        .games-mask-container {
            max-width: var(--max-content-width);
            margin: 0 auto;
            width: 100%;
            padding: 60px 40px 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }''',
    '''/* GAMES Letter Mask Container */
        .games-mask-container {
            max-width: var(--max-content-width);
            margin: 0 auto;
            width: 100%;
            padding: 60px 40px 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            position: relative; /* 支持sticky子元素 */
            z-index: 10;
        }'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')
