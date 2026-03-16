#!/bin/bash
# Cognitive Monitor GitHub 推送脚本
# 每 5 分钟推送 cognitive-data.json 到 GitHub Pages

cd /root/.openclaw/workspace/portfolio-blog

# 检查是否有更新
if git diff --quiet status-monitor/cognitive-data.json 2>/dev/null; then
    exit 0
fi

# 提交并推送
git add status-monitor/cognitive-data.json
git commit -m "data: $(date '+%H:%M') 认知监控数据更新"
git push origin main
