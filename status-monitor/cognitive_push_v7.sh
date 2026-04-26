#!/bin/bash
# Cognitive Monitor 推送脚本 v7.1 - 推送到独立 data 仓库
# 修复：添加数据复制步骤，从 portfolio-blog 复制到 scott-portfolio-data

SOURCE_DIR="/root/.openclaw/workspace/portfolio-blog/status-monitor"
REPO_DIR="/root/.openclaw/workspace/scott-portfolio-data"
DATA_FILE="status-monitor/cognitive-data.json"
HISTORY_FILE="status-monitor/cognitive-history.jsonl"
TREND_FILE="status-monitor/trend-data.json"
FAIL_COUNT_FILE="/tmp/cognitive_push_fail_count"
HEALTH_LOG="/var/log/cognitive_health.log"

# 检查源数据文件是否存在
if [ ! -f "$SOURCE_DIR/cognitive-data.json" ]; then
    echo "[$(date)] ❌ 源数据文件不存在: $SOURCE_DIR/cognitive-data.json" >> "$HEALTH_LOG"
    exit 1
fi

# 复制数据文件到 data 仓库
cp "$SOURCE_DIR/cognitive-data.json" "$REPO_DIR/$DATA_FILE"
cp "$SOURCE_DIR/cognitive-history.jsonl" "$REPO_DIR/$HISTORY_FILE" 2>/dev/null

# 进入仓库目录
cd "$REPO_DIR" || exit 1

# 检查是否有更改
if git diff --quiet HEAD -- "$DATA_FILE" "$HISTORY_FILE" 2>/dev/null; then
    echo "[$(date)] ⏸️ 数据未变化，跳过推送" >> "$HEALTH_LOG"
    exit 0
fi

# 添加更改
git add "$DATA_FILE" "$HISTORY_FILE" 2>/dev/null

# 提交
time_str=$(date '+%H:%M')
score=$(grep -o '"cognitive_score":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
status=$(grep -o '"status_text":"[^"]*"' "$DATA_FILE" | head -1 | cut -d'"' -f4)

git commit -m "data: update cognitive status at ${time_str} (score:${score}%, ${status})" >> "$HEALTH_LOG" 2>&1

# 推送
if git push origin master >> "$HEALTH_LOG" 2>&1; then
    echo "[$(date)] ✅ 推送成功 score=${score}%" >> "$HEALTH_LOG"
    rm -f "$FAIL_COUNT_FILE"
    exit 0
else
    echo "[$(date)] ❌ 推送失败" >> "$HEALTH_LOG"
    exit 1
fi
