#!/bin/bash
# Cognitive Monitor 推送脚本 v5.0 - 数据仓库分离版
# 更新: 使用独立数据仓库 scott-portfolio-data，通过GitHub API推送

REPO_DIR="/root/.openclaw/workspace/scott-portfolio-data"
DATA_FILE="status-monitor/cognitive-data.json"
HISTORY_FILE="status-monitor/cognitive-history.jsonl"
TREND_FILE="status-monitor/trend-data.json"
FAIL_COUNT_FILE="/tmp/cognitive_push_fail_count"
LAST_HASH_FILE="/tmp/cognitive_last_hash"
HEALTH_LOG="/var/log/cognitive_health.log"

# GitHub 配置
# 从环境变量读取Token，避免硬编码
GITHUB_TOKEN="${GITHUB_TOKEN_DATA_REPO:-${GITHUB_TOKEN:-}}"
GITHUB_API="https://api.github.com/repos/hiyaScott/scott-portfolio-data"

# 检查Token是否设置
if [ -z "$GITHUB_TOKEN" ]; then
    echo "[$(date)] ❌ 错误: GITHUB_TOKEN 未设置" >> "$HEALTH_LOG"
    exit 1
fi

# ============ 熔断机制 ============
MAX_CONSECUTIVE_FAILURES=5
CIRCUIT_BREAKER_FILE="/tmp/cognitive_circuit_breaker"

# 检查熔断器
if [ -f "$CIRCUIT_BREAKER_FILE" ]; then
    breaker_time=$(cat "$CIRCUIT_BREAKER_FILE")
    now=$(date +%s)
    elapsed=$((now - breaker_time))
    
    # 熔断30分钟后自动恢复
    if [ "$elapsed" -lt 1800 ]; then
        echo "[$(date)] ⚠️ 熔断器开启，跳过推送 ($((1800-elapsed))秒后恢复)" >> "$HEALTH_LOG"
        exit 0
    else
        echo "[$(date)] ✅ 熔断器自动关闭" >> "$HEALTH_LOG"
        rm -f "$CIRCUIT_BREAKER_FILE"
    fi
fi

# 检查数据文件
if [ ! -f "$REPO_DIR/$DATA_FILE" ]; then
    echo "[$(date)] ❌ 错误: 数据文件不存在" >> "$HEALTH_LOG"
    exit 1
fi

cd "$REPO_DIR" || exit 1

# 计算文件hash检查是否有实质变化
data_hash=$(md5sum "$DATA_FILE" | awk '{print $1}')
trend_hash=$(md5sum "$TREND_FILE" 2>/dev/null | awk '{print $1}')
last_data_hash=$(cat "$LAST_HASH_FILE" 2>/dev/null | head -1 || echo "")
last_trend_hash=$(cat "$LAST_HASH_FILE" 2>/dev/null | tail -1 || echo "")

if [ "$data_hash" = "$last_data_hash" ] && [ "$trend_hash" = "$last_trend_hash" ]; then
    exit 0
fi

# 失败退避机制
if [ -f "$FAIL_COUNT_FILE" ]; then
    fail_count=$(cat "$FAIL_COUNT_FILE")
    if [ "$fail_count" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
        echo "[$(date)] 🔴 连续失败$fail_count次，触发熔断器！" >> "$HEALTH_LOG"
        date +%s > "$CIRCUIT_BREAKER_FILE"
        exit 1
    fi
    
    if [ "$fail_count" -gt 3 ]; then
        delay=$(( (fail_count - 3) * 60 ))
        [ "$delay" -gt 300 ] && delay=300
        echo "[$(date)] ⏳ 退避延迟: ${delay}秒" >> "$HEALTH_LOG"
        sleep "$delay"
    fi
fi

# 读取当前评分和其他指标
score=$(grep -o '"cognitive_score":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
processing=$(grep -o '"processing_count":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
pending=$(grep -o '"pending_count":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
sessions=$(grep -o '"active_sessions":[0-9]*' "$DATA_FILE" | head -1 | cut -d: -f2)
status=$(grep -o '"status_text":"[^"]*"' "$DATA_FILE" | head -1 | cut -d'"' -f4)

# 构建commit message
time_str=$(date '+%H:%M')
commit_msg="data: update cognitive status at ${time_str}"

# ============ 使用 GitHub API 推送 ============

# 获取当前文件的SHA（用于更新）
get_file_sha() {
    local filepath=$1
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "$GITHUB_API/contents/$filepath" 2>/dev/null | grep -o '"sha":"[^"]*"' | head -1 | cut -d'"' -f4
}

# 上传文件到GitHub (使用Python工具避免参数过长)
upload_file() {
    local filepath=$1
    local message=$2
    
    python3 "/root/.openclaw/workspace/portfolio-blog/status-monitor/github_upload.py" "$filepath" "$message" "$GITHUB_TOKEN" "$REPO_DIR"
}

# 上传数据文件
data_result=$(upload_file "$DATA_FILE" "$commit_msg")
trend_result=$(upload_file "$TREND_FILE" "$commit_msg - trend")

# 检查推送结果
if [ "$data_result" = "success" ] && [ "$trend_result" = "success" ]; then
    # 推送成功
    rm -f "$FAIL_COUNT_FILE"
    echo "$data_hash" > "$LAST_HASH_FILE"
    echo "$trend_hash" >> "$LAST_HASH_FILE"
    echo "[$(date)] ✅ 推送成功 score=${score}%, trend=$(cat "$REPO_DIR/$TREND_FILE" 2>/dev/null | grep -o '"count":[0-9]*' | cut -d: -f2 || echo '0')" >> "$HEALTH_LOG"
    exit 0
else
    # 推送失败
    fail_count=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo "0")
    new_count=$((fail_count + 1))
    echo "$new_count" > "$FAIL_COUNT_FILE"
    echo "[$(date)] ❌ 推送失败 (第${new_count}次) data:$data_result trend:$trend_result" >> "$HEALTH_LOG"
    
    if [ "$new_count" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
        echo "[$(date)] 🔴 即将触发熔断器！" >> "$HEALTH_LOG"
    fi
    exit 1
fi
