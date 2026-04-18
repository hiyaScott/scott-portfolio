import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 移除 page-container 的 padding-bottom（让 footer 决定底部空间）
content = content.replace(
    '''            padding-bottom: 60px; /* 确保 footer 完全显示 */
        }
        
        @media (max-width: 768px) {
            .page-container {
                padding-bottom: 80px; /* 移动端更多空间 */
            }
        }''',
    '''            padding-bottom: 0; /* footer 自己处理底部空间 */
        }'''
)

# 2. 调整 footer 的 padding-bottom，确保足够但不太多
content = content.replace(
    '''            padding-bottom: calc(40px + env(safe-area-inset-bottom, 0px));''',
    '''            padding-bottom: calc(30px + env(safe-area-inset-bottom, 0px));'''
)

content = content.replace(
    '''                padding-bottom: calc(50px + env(safe-area-inset-bottom, 0px));''',
    '''                padding-bottom: calc(40px + env(safe-area-inset-bottom, 0px));'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')