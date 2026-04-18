import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# GAMES top: 90px, header: 70px, 所以 GAMES 距离导航栏 = 20px
# 让 GAMES 到卡片也等于 20px：
# 卡片起始位置 = 90px (GAMES top) + title-size + 20px = title-size + 110px
content = content.replace(
    'margin-top: calc(var(--games-title-size) + 90px); /* GAMES到导航栏距离 = GAMES到卡片距离 */',
    'margin-top: calc(var(--games-title-size) + 110px); /* GAMES到导航栏距离(20px) = GAMES到卡片距离(20px) */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')