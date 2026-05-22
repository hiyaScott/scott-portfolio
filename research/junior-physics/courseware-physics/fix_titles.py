#!/usr/bin/env python3
"""Fix all physics chapter titles to follow the rule:
- h1 = Chapter topic name (e.g., "第一章 测量")
- subtitle = English code · Lab name · Chapter X / 18
"""

import os, re

BASE = '/root/.openclaw/workspace/portfolio-blog/research/junior-physics/courseware-physics'

CHAPTERS = {
    'grade8-sem1-ch00': {
        'title': '序言',
        'code': 'INTRO',
        'lab': '物理特工总部',
        'chapter': '0',
    },
    'grade8-sem1-ch01': {
        'title': '第一章 测量',
        'code': 'MEASURE',
        'lab': '精密测量实验室',
        'chapter': '1',
    },
    'grade8-sem1-ch02': {
        'title': '第二章 机械运动',
        'code': 'MOTION',
        'lab': '运动分析实验室',
        'chapter': '2',
    },
    'grade8-sem1-ch03': {
        'title': '第三章 声',
        'code': 'ACOUSTICS',
        'lab': '声学实验室',
        'chapter': '3',
    },
    'grade8-sem1-ch04': {
        'title': '第四章 光',
        'code': 'OPTICS',
        'lab': '光学分析中心',
        'chapter': '4',
    },
    'grade8-sem1-ch05': {
        'title': '第五章 力与运动',
        'code': 'DYNAMICS',
        'lab': '力学分析中心',
        'chapter': '5',
    },
    'grade8-sem2-ch06': {
        'title': '第六章 密度与压强',
        'code': 'DENSITY',
        'lab': '流体力学实验室',
        'chapter': '6',
    },
    'grade8-sem2-ch07': {
        'title': '第七章 浮力',
        'code': 'BUOYANCY',
        'lab': '流体动力学实验室',
        'chapter': '7',
    },
    'grade8-sem2-ch08': {
        'title': '第八章 简单机械、功和能',
        'code': 'MECH',
        'lab': '机械工程实验室',
        'chapter': '8',
    },
    'grade8-sem2-ch09': {
        'title': '第九章 物态变化',
        'code': 'THERMO',
        'lab': '热学实验室',
        'chapter': '9',
    },
    'grade9-sem1-ch10': {
        'title': '第十章 内能',
        'code': 'THERMAL',
        'lab': '热力学实验室',
        'chapter': '10',
    },
    'grade9-sem1-ch11': {
        'title': '第十一章 静电与电流',
        'code': 'ELEC',
        'lab': '电路实验室',
        'chapter': '11',
    },
    'grade9-sem1-ch12': {
        'title': '第十二章 欧姆定律',
        'code': 'OHM',
        'lab': '电学实验室',
        'chapter': '12',
    },
    'grade9-sem1-ch13': {
        'title': '第十三章 电功与电功率',
        'code': 'POWER',
        'lab': '电力实验室',
        'chapter': '13',
    },
    'grade9-sem2-ch14': {
        'title': '第十四章 电与磁',
        'code': 'MAG',
        'lab': '电磁实验室',
        'chapter': '14',
    },
    'grade9-sem2-ch15': {
        'title': '第十五章 电磁波',
        'code': 'WAVE',
        'lab': '通信实验室',
        'chapter': '15',
    },
    'grade9-sem2-ch16': {
        'title': '第十六章 从原子到星系',
        'code': 'COSMOS',
        'lab': '宇宙实验室',
        'chapter': '16',
    },
    'grade9-sem2-ch17': {
        'title': '第十七章 能源',
        'code': 'ENERGY',
        'lab': '能源实验室',
        'chapter': '17',
    },
}

# Special case: ch00 is "序言" - no chapter number in subtitle

for dirname, info in CHAPTERS.items():
    path = os.path.join(BASE, dirname, 'tutorial.html')
    if not os.path.exists(path):
        print(f'SKIP (not found): {dirname}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # Fix <title>
    title_new = f'{info["title"]} · {info["code"]} · {info["lab"]}'
    content = re.sub(r'<title>[^<]*</title>', f'<title>{title_new}</title>', content, count=1)

    # Fix h1 - replace anything between <h1>...</h1> in title-bar
    # Match the title-bar h1 specifically
    content = re.sub(
        r'(<div class="title-bar">\s*)<h1>[^<]*</h1>',
        rf'\1<h1>{info["title"]}</h1>',
        content,
        count=1
    )
    # Also handle cases where title-bar div is on same line
    content = re.sub(
        r'(<div class="title-bar">)<h1>[^<]*</h1>',
        rf'\1<h1>{info["title"]}</h1>',
        content,
        count=1
    )

    # Fix subtitle
    if info['chapter'] == '0':
        sub_new = f'{info["code"]} · {info["lab"]}'
    else:
        sub_new = f'{info["code"]} · {info["lab"]} · 第 {info["chapter"]} / 18 章'

    content = re.sub(
        r'(<div class="title-bar">.*?)<div class="subtitle">[^<]*</div>',
        rf'\1<div class="subtitle">{sub_new}</div>',
        content,
        count=1,
        flags=re.DOTALL
    )

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'FIXED: {dirname} → h1="{info["title"]}" subtitle="{sub_new}"')
    else:
        print(f'NO CHANGE: {dirname}')

print('\nDone.')
