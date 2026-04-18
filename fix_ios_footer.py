import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 修改 page-container 添加底部 padding，确保 footer 不被遮挡
old_container = '''        /* Main Content Container */
        .page-container {
            position: relative;
            z-index: 2;
            height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }'''

new_container = '''        /* Main Content Container */
        .page-container {
            position: relative;
            z-index: 2;
            height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            scroll-behavior: smooth;
            padding-bottom: 100px; /* 确保 footer 完全显示 */
        }
        
        @media (max-width: 768px) {
            .page-container {
                padding-bottom: 120px; /* 移动端更多空间 */
            }
        }'''

content = content.replace(old_container, new_container)

# 同时增加 footer 的内边距
old_footer = '''        /* Footer - Match Homepage EXACTLY */
        .footer {
            background: #fff;
            padding: 30px 40px;
            padding-bottom: calc(30px + env(safe-area-inset-bottom, 0px));
            border-top: 1px solid #eee;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            .footer {
                padding: 20px;
                padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px));
            }
        }'''

new_footer = '''        /* Footer - Match Homepage EXACTLY */
        .footer {
            background: #fff;
            padding: 30px 40px;
            padding-bottom: calc(50px + env(safe-area-inset-bottom, 0px));
            border-top: 1px solid #eee;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            .footer {
                padding: 20px;
                padding-bottom: calc(60px + env(safe-area-inset-bottom, 0px));
            }
        }'''

content = content.replace(old_footer, new_footer)

# 修改 mobile 响应式中重复的 footer padding 设置
content = content.replace(
    '''            .footer { 
                padding: 20px;
                padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px));
            }''',
    '''            .footer { 
                padding: 20px;
                padding-bottom: calc(60px + env(safe-area-inset-bottom, 0px));
            }'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')