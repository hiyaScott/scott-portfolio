#!/bin/bash
# Cognitive Monitor 数据同步脚本 v3.0
# 修复：统一数据格式，确保前后端一致

REPO_DIR="/root/.openclaw/workspace/portfolio-blog"
DATA_FILE="status-monitor/cognitive-data.json"
FAIL_COUNT_FILE="/tmp/cognitive_push_fail_count"
LAST_HASH_FILE="/tmp/cognitive_last_hash"

# 检查数据文件是否存在
if [ ! -f "$REPO_DIR/$DATA_FILE" ]; then
    echo "[$(date)] 错误: 数据文件不存在"
    exit 1
fi

cd "$REPO_DIR" || exit 1

# 计算文件hash检查是否有实质变化
current_hash=$(md5sum "$DATA_FILE" | awk '{print $1}')
last_hash=$(cat "$LAST_HASH_FILE" 2>/dev/null || echo "")

if [ "$current_hash" = "$last_hash" ]; then
    # 无实质变化，跳过
    exit 0
fi

# 失败退避机制
if [ -f "$FAIL_COUNT_FILE" ]; then
    fail_count=$(cat "$FAIL_COUNT_FILE")
    if [ "$fail_count" -gt 3 ]; then
        delay=$(( (fail_count - 3) * 30 ))
        [ "$delay" -gt 120 ] && delay=120
        sleep "$delay"
    fi
fi

# 读取当前评分
score=$(grep -o '"cognitive_score":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
processing=$(grep -o '"processing_count":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)

# 添加文件
git add "$DATA_FILE"

# 提交（带时间戳和评分）
commit_msg="data: $(date '+%H:%M')"
if [ -n "$score" ]; then
    commit_msg="${commit_msg} score:${score}% proc:${processing}"
fi
git commit -m "$commit_msg"

# 推送（使用 HTTP/1.1 避免超时）
git config http.version HTTP/1.1
if git push origin main; then
    # 推送成功
    rm -f "$FAIL_COUNT_FILE"
    echo "$current_hash" > "$LAST_HASH_FILE"
    echo "[$(date)] ✅ 推送成功 score=${score}%"
else
    # 推送失败
    fail_count=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo "0")
    echo $((fail_count + 1)) > "$FAIL_COUNT_FILE"
    echo "[$(date)] ❌ 推送失败 (第$((fail_count + 1))次)"
fi
