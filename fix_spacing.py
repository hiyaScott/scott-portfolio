import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 修改 cards-wrapper 的 margin-top，让距离与 GAMES 到导航栏的距离相等
# GAMES top: 90px, header: 70px, 所以 GAMES 到导航栏 = 20px
# 让 GAMES 到卡片也等于 20px，所以 margin-top = title-size + 90px
content = content.replace(
    'margin-top: calc(var(--games-title-size) + 20px); /* 跟随 GAMES 标题大小 */',
    'margin-top: calc(var(--games-title-size) + 90px); /* GAMES到导航栏距离 = GAMES到卡片距离 */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')