import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 减小 page-container 的 padding-bottom
content = content.replace(
    '''            padding-bottom: 100px; /* 确保 footer 完全显示 */''',
    '''            padding-bottom: 60px; /* 确保 footer 完全显示 */'''
)

content = content.replace(
    '''                padding-bottom: 120px; /* 移动端更多空间 */''',
    '''                padding-bottom: 80px; /* 移动端更多空间 */'''
)

# 2. 调整 footer 的 padding-bottom，不要太大
content = content.replace(
    '''            padding-bottom: calc(50px + env(safe-area-inset-bottom, 0px));''',
    '''            padding-bottom: calc(40px + env(safe-area-inset-bottom, 0px));'''
)

content = content.replace(
    '''                padding-bottom: calc(60px + env(safe-area-inset-bottom, 0px));''',
    '''                padding-bottom: calc(50px + env(safe-area-inset-bottom, 0px));'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')