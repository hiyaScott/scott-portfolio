import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 进一步减小卡片容器初始位置 - 紧贴 GAMES 标题下方
content = content.replace(
    'margin-top: 100px; /* 紧贴 GAMES 标题下方 */',
    'margin-top: 60px; /* 紧贴 GAMES 标题下方 */'
)

# 2. 同时减小 games-mask-container 的 padding
content = content.replace(
    'padding: 60px 40px 40px;',
    'padding: 30px 40px 20px;'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')