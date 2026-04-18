import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 添加 CSS 变量到 :root，用于同步 GAMES 标题大小
old_root = '''        :root {
            --color-header: #1a1a1a;
            --color-text: #333;
            --color-text-light: #666;
            --color-bg: #f8f8f8;
            --header-height: 70px;
            --max-content-width: 1200px;
        }'''

new_root = '''        :root {
            --color-header: #1a1a1a;
            --color-text: #333;
            --color-text-light: #666;
            --color-bg: #f8f8f8;
            --header-height: 70px;
            --max-content-width: 1200px;
            --games-title-size: clamp(80px, 15vw, 180px);
        }'''

content = content.replace(old_root, new_root)

# 2. 修改 GAMES 标题使用 CSS 变量
content = content.replace(
    'font-size: clamp(80px, 15vw, 180px);',
    'font-size: var(--games-title-size);'
)

# 3. 修改卡片容器 margin-top 跟随标题大小
content = content.replace(
    'margin-top: 60px; /* 紧贴 GAMES 标题下方 */',
    'margin-top: calc(var(--games-title-size) + 20px); /* 跟随 GAMES 标题大小 */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')