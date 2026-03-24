#!/usr/bin/env python3
"""
移动端适配检查脚本
检查所有HTML文件的移动端适配情况
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# 工作目录
WORKSPACE = Path("/root/.openclaw/workspace/portfolio-blog")

# 检查结果
results = {
    "total_files": 0,
    "with_viewport": [],
    "without_viewport": [],
    "with_media_queries": [],
    "without_media_queries": [],
    "fixed_width_issues": [],
    "small_font_issues": [],
    "overflow_issues": [],
    "details": {}
}

def extract_head_content(content):
    """提取head标签内容"""
    match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else ""

def extract_style_content(content):
    """提取所有style标签内容"""
    styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    return '\n'.join(styles)

def check_viewport(content):
    """检查是否有viewport meta标签"""
    head = extract_head_content(content)
    viewport_pattern = r'<meta[^>]*name=["\']viewport["\'][^>]*>'
    return bool(re.search(viewport_pattern, head, re.IGNORECASE))

def check_media_queries(content):
    """检查是否有媒体查询"""
    style = extract_style_content(content)
    # 检查@media规则
    return bool(re.search(r'@media\s*\([^)]*\)', style, re.IGNORECASE))

def check_fixed_width_issues(content):
    """检查固定宽度问题"""
    issues = []
    style = extract_style_content(content)
    
    # 检查固定像素宽度（非max-width）
    fixed_width_patterns = [
        r'width:\s*(\d+)px',
        r'width:\s*([\d.]+)em',
        r'width=\"(\d+)\"',
    ]
    
    for pattern in fixed_width_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            try:
                val = int(float(match))
                if val > 400:  # 大于400px可能有问题
                    issues.append(f"固定宽度 {val}px")
            except:
                pass
    
    return issues

def check_small_fonts(content):
    """检查小字体问题"""
    issues = []
    style = extract_style_content(content)
    
    # 检查小于16px的字体
    font_patterns = [
        r'font-size:\s*(\d+)px',
        r'font-size:\s*([\d.]+)pt',
    ]
    
    for pattern in font_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            try:
                val = float(match)
                if val < 12:  # 小于12px
                    issues.append(f"字体大小 {val}px")
            except:
                pass
    
    return issues

def check_overflow_issues(content):
    """检查可能导致横向滚动的问题"""
    issues = []
    
    # 检查overflow-x: hidden（这是好的）
    if not re.search(r'overflow-x:\s*hidden', content, re.IGNORECASE):
        # 检查表格
        if '<table' in content.lower():
            if not re.search(r'overflow-x:\s*auto', content, re.IGNORECASE):
                if not re.search(r'@media.*table', content, re.DOTALL | re.IGNORECASE):
                    issues.append("表格可能没有响应式处理")
    
    # 检查pre标签
    if '<pre>' in content.lower() or '<pre ' in content.lower():
        if not re.search(r'pre\s*{[^}]*overflow', content, re.IGNORECASE):
            issues.append("pre标签可能没有overflow处理")
    
    return issues

def analyze_file(filepath):
    """分析单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}
    
    result = {
        "has_viewport": check_viewport(content),
        "has_media_queries": check_media_queries(content),
        "fixed_width_issues": check_fixed_width_issues(content),
        "small_font_issues": check_small_fonts(content),
        "overflow_issues": check_overflow_issues(content),
        "size_kb": round(len(content) / 1024, 2)
    }
    
    return result

def main():
    """主函数"""
    # 获取所有HTML文件
    html_files = sorted(WORKSPACE.rglob("*.html"))
    
    results["total_files"] = len(html_files)
    
    print(f"开始检查 {len(html_files)} 个HTML文件...\n")
    
    for i, filepath in enumerate(html_files, 1):
        rel_path = filepath.relative_to(WORKSPACE)
        analysis = analyze_file(filepath)
        
        results["details"][str(rel_path)] = analysis
        
        if analysis.get("has_viewport"):
            results["with_viewport"].append(str(rel_path))
        else:
            results["without_viewport"].append(str(rel_path))
        
        if analysis.get("has_media_queries"):
            results["with_media_queries"].append(str(rel_path))
        else:
            results["without_media_queries"].append(str(rel_path))
        
        if analysis.get("fixed_width_issues"):
            results["fixed_width_issues"].append({
                "file": str(rel_path),
                "issues": analysis["fixed_width_issues"]
            })
        
        if analysis.get("small_font_issues"):
            results["small_font_issues"].append({
                "file": str(rel_path),
                "issues": analysis["small_font_issues"]
            })
        
        if analysis.get("overflow_issues"):
            results["overflow_issues"].append({
                "file": str(rel_path),
                "issues": analysis["overflow_issues"]
            })
        
        if i % 20 == 0:
            print(f"  已检查 {i}/{len(html_files)} 个文件...")
    
    # 保存完整报告
    report_path = WORKSPACE / "mobile-check-report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 输出摘要
    print("\n" + "="*60)
    print("移动端适配检查报告")
    print("="*60)
    print(f"\n总文件数: {results['total_files']}")
    print(f"\n✓ 有 viewport meta 标签: {len(results['with_viewport'])}/{results['total_files']}")
    print(f"✗ 缺少 viewport meta 标签: {len(results['without_viewport'])}/{results['total_files']}")
    print(f"\n✓ 有媒体查询 (@media): {len(results['with_media_queries'])}/{results['total_files']}")
    print(f"✗ 缺少媒体查询: {len(results['without_media_queries'])}/{results['total_files']}")
    print(f"\n⚠ 固定宽度问题: {len(results['fixed_width_issues'])} 个文件")
    print(f"⚠ 小字体问题: {len(results['small_font_issues'])} 个文件")
    print(f"⚠ 溢出/滚动问题: {len(results['overflow_issues'])} 个文件")
    
    if results['without_viewport']:
        print("\n" + "-"*60)
        print("缺少 viewport 的文件:")
        for f in results['without_viewport'][:20]:
            print(f"  - {f}")
        if len(results['without_viewport']) > 20:
            print(f"  ... 还有 {len(results['without_viewport']) - 20} 个")
    
    print(f"\n详细报告已保存到: {report_path}")
    
    return results

if __name__ == "__main__":
    main()
