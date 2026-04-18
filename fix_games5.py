import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改方块效果: rgb(220,220,220), alpha 0.6→1.0
content = content.replace('rgba(200, 200, 200,', 'rgba(220, 220, 220,')

# 2. 修改 GAMES 标题逻辑
# 改为 fixed 定位，滚动时保持不动，卡片通过 z-index 盖在上面
content = content.replace(
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
        }''',
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
        }'''
)

# 3. 调整卡片区域的 z-index，确保盖在 GAMES 之上
content = content.replace(
    '''/* Cards Container - Match Homepage Specs */
        .cards-wrapper {
            flex: 1;
            padding: 0 40px 100px;
            max-width: var(--max-content-width);
            margin: 0 auto;
            width: 100%;
        }''',
    '''/* Cards Container - Match Homepage Specs */
        .cards-wrapper {
            flex: 1;
            padding: 0 40px 100px;
            max-width: var(--max-content-width);
            margin: 0 auto;
            width: 100%;
            position: relative;
            z-index: 2; /* 盖在 GAMES 标题之上 */
            margin-top: 40vh; /* 留出空间显示 GAMES 标题 */
        }'''
)

# 4. 调整 games-mask-container 不需要 sticky 了
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
            position: relative; /* 支持sticky子元素 */
            z-index: 10;
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
            position: relative;
        }'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')
