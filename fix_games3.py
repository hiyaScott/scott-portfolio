import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改方块效果
content = content.replace('rgba(250, 250, 250,', 'rgba(252, 252, 252,')
content = content.replace(
    'const alpha = 1.0 - (this.scale - 1) * 1.0;  // scale 1→1.2, alpha 1.0→0.8',
    'const alpha = 0.8 + (this.scale - 1) * 1.0;  // scale 1→1.2, alpha 0.8→1.0'
)
content = content.replace('// ALPHA: base 1.0 → hover 0.8', '// ALPHA: base 0.8 → hover 1.0')

# 2. 修改导航链接颜色 - 白色背景下使用深色文字
content = content.replace(
    '''.nav-link {
            color: rgba(255, 255, 255, 0.8);''',
    '''.nav-link {
            color: rgba(255, 255, 255, 0.9);'''
)
content = content.replace(
    '''.nav-link:hover, .nav-link.active { color: #fff; }''',
    '''.nav-link:hover, .nav-link.active { color: #fff; font-weight: 400; }'''
)

# 3. 修改 social link 颜色
content = content.replace(
    '''.social-link {
            color: rgba(255, 255, 255, 0.6);''',
    '''.social-link {
            color: rgba(255, 255, 255, 0.7);'''
)

# 4. 修改卡片结构 - 上下两层设计
old_card = '''/* Game Card - Updated to match homepage specs */
        .game-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            backdrop-filter: blur(20px);
        }
        
        .game-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }'''

new_card = '''/* Game Card - Two layer design */
        .game-card {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .game-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.15), 0 4px 8px rgba(0,0,0,0.08);
        }
        
        /* Card Image - Top layer with color */
        .card-image {
            width: 100%;
            height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            position: relative;
        }
        
        .game-card:nth-child(2) .card-image {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .game-card:nth-child(3) .card-image {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }'''

# 移除旧的 card-image 样式并替换卡片样式
content = content.replace(old_card, new_card)

# 删除旧的 card-image 样式
old_card_image = '''/* Card Image - Match homepage 180px height */
        .card-image {
            width: 100%;
            height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
            position: relative;
        }'''
content = content.replace(old_card_image, '')

# 5. 修改 card-content 为白色背景
content = content.replace(
    '''/* Card Content - Match homepage specs */
        .card-content {
            padding: 20px;
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #333;
        }
        
        .card-meta {
            font-size: 13px;
            color: rgba(255,255,255,0.5);
            margin-bottom: 0;
        }''',
    '''/* Card Content - White bottom layer */
        .card-content {
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #1a1a1a;
        }
        
        .card-meta {
            font-size: 13px;
            color: #666;
            margin-bottom: 0;
        }'''
)

# 6. 修改 status badge 颜色适配新设计
content = content.replace(
    '''.status-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            font-size: 10px;
            font-weight: 700;
            padding: 5px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(0,0,0,0.6);
            color: #333;
            border: 1px solid rgba(255,255,255,0.2);
            z-index: 2;
        }''',
    '''.status-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            font-size: 10px;
            font-weight: 700;
            padding: 5px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(255,255,255,0.95);
            color: #333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 2;
        }'''
)

# 7. 修改 platform tag
content = content.replace(
    '''.platform-tag {
            position: absolute;
            top: 12px;
            right: 12px;
            font-size: 10px;
            color: rgba(255,255,255,0.8);
            background: rgba(0,0,0,0.4);
            padding: 5px 10px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 2;
        }''',
    '''.platform-tag {
            position: absolute;
            top: 12px;
            right: 12px;
            font-size: 10px;
            color: #fff;
            background: rgba(0,0,0,0.5);
            padding: 5px 10px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
            z-index: 2;
        }'''
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')