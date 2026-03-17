#!/usr/bin/env python3
"""
梦幻模拟战角色数据库勘误工具
从HTML文件中提取角色数据，并与B站Wiki进行对比
"""

from html.parser import HTMLParser
import re
import json
from pathlib import Path

class LangrisserHeroParser(HTMLParser):
    """解析HTML中的梦幻模拟战角色数据"""
    
    def __init__(self):
        super().__init__()
        self.heroes = []
        self.current_hero = None
        self.in_langrisser_section = False
        self.in_hero_cell = False
        self.current_cell_type = None  # 'name', 'talent', 'skill1', 'skill2', 'ult', 'tags'
        self.current_data = {}
        self.cell_count = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # 检测是否进入梦幻模拟战部分
        if tag == 'div' and attrs_dict.get('data-game') == 'langrisser':
            self.in_langrisser_section = True
            
        if not self.in_langrisser_section:
            return
            
        # 检测英雄行
        if tag == 'tr' and self.in_langrisser_section:
            self.current_data = {}
            self.cell_count = 0
            
        # 检测单元格类型
        if tag == 'td':
            self.cell_count += 1
            if self.cell_count == 1:
                self.current_cell_type = 'hero_info'
            elif self.cell_count == 2:
                self.current_cell_type = 'talent'
            elif self.cell_count == 3:
                self.current_cell_type = 'skill1'
            elif self.cell_count == 4:
                self.current_cell_type = 'skill2'
            elif self.cell_count == 5:
                self.current_cell_type = 'ult'
            elif self.cell_count == 6:
                self.current_cell_type = 'tags'
                
    def handle_endtag(self, tag):
        if tag == 'tr' and self.current_data and self.in_langrisser_section:
            if self.current_data.get('name'):
                self.heroes.append(self.current_data.copy())
                
        # 离开梦幻模拟战部分
        if tag == 'div' and self.in_langrisser_section:
            # 检查是否是section结束
            pass
            
    def handle_data(self, data):
        if not self.in_langrisser_section:
            return
            
        data = data.strip()
        if not data:
            return
            
        # 解析英雄名称和元信息
        if self.current_cell_type == 'hero_info':
            # 提取英雄名称（去掉T0/T1/T2标签）
            if 'hero-name' in str(self.get_starttag_text()):
                # 清理T标签
                clean_name = re.sub(r'\s*T[012]\s*', '', data)
                self.current_data['name'] = clean_name
            # 提取元信息 (SSR·光辉·步兵 等)
            elif 'hero-meta' in str(self.get_starttag_text()):
                self.current_data['meta'] = data
                # 解析阵营、职业等信息
                parts = data.split('·')
                if len(parts) >= 3:
                    self.current_data['rarity'] = parts[0]
                    self.current_data['faction'] = parts[1]
                    self.current_data['class'] = parts[2]
                    
        # 解析天赋/特性
        elif self.current_cell_type == 'talent':
            if 'skill-name' in str(self.get_starttag_text()):
                self.current_data['talent_name'] = data
            elif 'skill-desc' in str(self.get_starttag_text()):
                self.current_data['talent_desc'] = data
                
        # 解析主动技能1
        elif self.current_cell_type == 'skill1':
            if 'skill-name' in str(self.get_starttag_text()):
                self.current_data['skill1_name'] = data
            elif 'skill-desc' in str(self.get_starttag_text()):
                self.current_data['skill1_desc'] = data
                
        # 解析主动技能2
        elif self.current_cell_type == 'skill2':
            if 'skill-name' in str(self.get_starttag_text()):
                self.current_data['skill2_name'] = data
            elif 'skill-desc' in str(self.get_starttag_text()):
                self.current_data['skill2_desc'] = data
                
        # 解析超绝/大招
        elif self.current_cell_type == 'ult':
            if 'skill-name' in str(self.get_starttag_text()):
                self.current_data['ult_name'] = data
            elif 'skill-desc' in str(self.get_starttag_text()):
                self.current_data['ult_desc'] = data
                
    def get_starttag_text(self):
        # 辅助方法，返回当前处理的标签信息
        return ""


def parse_html_file(file_path):
    """解析HTML文件，提取梦幻模拟战角色"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取梦幻模拟战部分
    # 找到梦幻模拟战section的开始和结束
    langrisser_match = re.search(
        r'<div class="section game-section" data-game="langrisser">(.*?)</div>\s*</div>\s*<!--\s*(?:铃兰之剑|三国志)',
        content,
        re.DOTALL
    )
    
    if not langrisser_match:
        # 尝试另一种匹配方式
        langrisser_match = re.search(
            r'<div class="section game-section" data-game="langrisser">(.*?)<!--',
            content,
            re.DOTALL
        )
    
    if not langrisser_match:
        print("未找到梦幻模拟战部分")
        return []
    
    langrisser_content = langrisser_match.group(1)
    
    # 提取所有英雄行
    heroes = []
    
    # 匹配每个<tr>行
    row_pattern = re.compile(
        r'<tr>\s*<td class="hero-cell">(.*?)</td>\s*<td class="skill-cell">(.*?)</td>\s*<td class="skill-cell">(.*?)</td>\s*<td class="skill-cell">(.*?)</td>\s*<td class="skill-cell">(.*?)</td>\s*<td class="tags-cell">(.*?)</td>\s*</tr>',
        re.DOTALL
    )
    
    for match in row_pattern.finditer(langrisser_content):
        hero_cell, talent_cell, skill1_cell, skill2_cell, ult_cell, tags_cell = match.groups()
        
        hero_data = {}
        
        # 解析英雄名称和元信息
        name_match = re.search(r'<div class="hero-name">(.*?)<span', hero_cell)
        if name_match:
            hero_data['name'] = re.sub(r'<[^>]+>', '', name_match.group(1)).strip()
        
        meta_match = re.search(r'<div class="hero-meta">(.*?)</div>', hero_cell)
        if meta_match:
            hero_data['meta'] = meta_match.group(1).strip()
            parts = hero_data['meta'].split('·')
            if len(parts) >= 3:
                hero_data['rarity'] = parts[0]
                hero_data['faction'] = parts[1] 
                hero_data['class'] = parts[2]
        
        # 解析技能单元格
        def parse_skill_cell(cell):
            """解析技能单元格，提取名称和描述"""
            name_match = re.search(r'<div class="skill-name">(.*?)</div>', cell)
            desc_match = re.search(r'<div class="skill-desc">(.*?)</div>', cell)
            return {
                'name': re.sub(r'<[^>]+>', '', name_match.group(1)).strip() if name_match else '',
                'desc': re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ''
            }
        
        hero_data['talent'] = parse_skill_cell(talent_cell)
        hero_data['skill1'] = parse_skill_cell(skill1_cell)
        hero_data['skill2'] = parse_skill_cell(skill2_cell)
        hero_data['ult'] = parse_skill_cell(ult_cell)
        
        # 解析标签
        tags = re.findall(r'<span class="tag[^"]*">([^<]+)</span>', tags_cell)
        hero_data['tags'] = tags
        
        if hero_data.get('name'):
            heroes.append(hero_data)
    
    return heroes


if __name__ == '__main__':
    file_path = '/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/character-skills-enumeration.html'
    
    heroes = parse_html_file(file_path)
    
    print(f"共提取到 {len(heroes)} 位梦幻模拟战角色")
    
    # 保存为JSON以便后续处理
    output_path = '/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_heroes.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    
    print(f"角色数据已保存到: {output_path}")
    
    # 显示前10个角色作为示例
    print("\n前10个角色示例:")
    for i, hero in enumerate(heroes[:10]):
        print(f"{i+1}. {hero['name']} ({hero.get('faction', '未知阵营')})")
