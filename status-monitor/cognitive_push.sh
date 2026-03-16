#!/bin/bash
# Cognitive Monitor GitHub 推送脚本 v2.0
# 优化：错峰推送 + 失败退避 + 变化检测

REPO_DIR="/root/.openclaw/workspace/portfolio-blog"
DATA_FILE="status-monitor/cognitive-data.json"
FAIL_COUNT_FILE="/tmp/cognitive_push_fail_count"
LAST_SCORE_FILE="/tmp/cognitive_last_score"
MIN_SCORE_CHANGE=5  # 认知评分变化阈值

# 检查数据文件是否存在
if [ ! -f "$REPO_DIR/$DATA_FILE" ]; then
    exit 0
fi

cd "$REPO_DIR" || exit 1

# 检查文件是否有变化
if git diff --quiet "$DATA_FILE" 2>/dev/null; then
    # 文件无变化，重置失败计数
    rm -f "$FAIL_COUNT_FILE"
    exit 0
fi

# 读取当前认知评分
current_score=$(grep -o '"cognitive_score":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
last_score=$(cat "$LAST_SCORE_FILE" 2>/dev/null || echo "0")

# 检查评分变化是否超过阈值
if [ -n "$current_score" ] && [ -n "$last_score" ]; then
    score_diff=$(echo "$current_score - $last_score" | bc)
    score_diff=${score_diff#-}  # 取绝对值
    
    if [ "$score_diff" -lt "$MIN_SCORE_CHANGE" ] && [ "$last_score" != "0" ]; then
        # 变化太小，跳过推送
        exit 0
    fi
fi

# 失败退避机制
if [ -f "$FAIL_COUNT_FILE" ]; then
    fail_count=$(cat "$FAIL_COUNT_FILE")
    if [ "$fail_count" -gt 3 ]; then
        # 连续失败超过3次，增加延迟（最多延迟2分钟）
        delay=$(( (fail_count - 3) * 30 ))
        [ "$delay" -gt 120 ] && delay=120
        sleep "$delay"
    fi
fi

# 添加文件
git add "$DATA_FILE"

# 提交（带时间戳和评分）
commit_msg="data: $(date '+%H:%M')"
if [ -n "$current_score" ]; then
    commit_msg="${commit_msg} score:${current_score}"
fi
git commit -m "$commit_msg"

# 推送（使用 HTTP/1.1 避免超时）
git config http.version HTTP/1.1
if git push origin main; then
    # 推送成功
    rm -f "$FAIL_COUNT_FILE"
    echo "$current_score" > "$LAST_SCORE_FILE"
    echo "[$(date)] ✅ 推送成功 score=${current_score}"
else
    # 推送失败
    fail_count=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo "0")
    echo $((fail_count + 1)) > "$FAIL_COUNT_FILE"
    echo "[$(date)] ❌ 推送失败 (第$((fail_count + 1))次)"
fi
