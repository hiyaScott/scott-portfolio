import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 调回更小的间距，让卡片更靠近 GAMES
# GAMES bottom = 90px + title-size
# 让间距约 30px (稍微大于导航栏到GAMES的20px)
content = content.replace(
    'margin-top: calc(var(--games-title-size) + 110px); /* GAMES到导航栏距离(20px) = GAMES到卡片距离(20px) */',
    'margin-top: calc(var(--games-title-size) + 30px); /* 卡片距离GAMES底部30px */'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')