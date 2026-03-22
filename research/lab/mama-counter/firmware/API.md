# 妈妈计数器 API 接口文档 v1.0

## 基础信息

- **基础URL**: `https://your-api-server.com/api/v1`
- **数据格式**: JSON
- **认证方式**: Device ID (设备唯一标识)

---

## 设备注册与认证

### 设备首次激活

```http
POST /devices/register
```

**请求体:**
```json
{
    "device_id": "MC-A1B2C3D4",
    "model": "MC-ESP32S3-185",
    "firmware_version": "2.0.0",
    "mac_address": "A1:B2:C3:D4:E5:F6"
}
```

**响应:**
```json
{
    "success": true,
    "device": {
        "device_id": "MC-A1B2C3D4",
        "status": "active",
        "created_at": "2026-03-22T10:00:00Z"
    },
    "config": {
        "sync_interval": 300,
        "audio_threshold": 5000,
        "voice_model": "default"
    }
}
```

---

## 数据同步

### 设备上报数据

```http
POST /devices/{device_id}/sync
```

**请求体:**
```json
{
    "timestamp": 1711098000,
    "today_count": 23,
    "total_count": 156,
    "battery": 78,
    "periods": {
        "morning": 5,
        "forenoon": 8,
        "afternoon": 6,
        "evening": 4
    },
    "firmware_version": "2.0.0"
}
```

**响应:**
```json
{
    "success": true,
    "server_time": 1711098005,
    "config_update": {
        "audio_threshold": 5200
    },
    "notifications": []
}
```

---

## Web端数据查询

### 获取设备列表

```http
GET /user/devices
Authorization: Bearer {user_token}
```

**响应:**
```json
{
    "devices": [
        {
            "device_id": "MC-A1B2C3D4",
            "name": "小宝的计数器",
            "status": "online",
            "last_seen": "2026-03-22T15:30:00Z",
            "today_count": 23,
            "battery": 78
        }
    ]
}
```

### 获取每日统计

```http
GET /devices/{device_id}/stats/daily?date=2026-03-22
Authorization: Bearer {user_token}
```

**响应:**
```json
{
    "date": "2026-03-22",
    "total": 59,
    "periods": {
        "morning": 12,
        "forenoon": 18,
        "afternoon": 15,
        "evening": 14
    },
    "hourly": [2,3,4,3,0,0,1,2,3,4,5,4,3,4,5,3,2,1,2,3,4,3,2,1]
}
```

### 获取日期范围统计

```http
GET /devices/{device_id}/stats/range?start=2026-03-15&end=2026-03-22
Authorization: Bearer {user_token}
```

**响应:**
```json
{
    "start": "2026-03-15",
    "end": "2026-03-22",
    "days": [
        {"date": "2026-03-15", "total": 37},
        {"date": "2026-03-16", "total": 42},
        {"date": "2026-03-17", "total": 39},
        {"date": "2026-03-18", "total": 51},
        {"date": "2026-03-19", "total": 48},
        {"date": "2026-03-20", "total": 44},
        {"date": "2026-03-21", "total": 58},
        {"date": "2026-03-22", "total": 59}
    ],
    "summary": {
        "total": 378,
        "average": 47.25,
        "max": 59,
        "min": 37
    }
}
```

---

## 声纹管理

### 上传声纹样本

```http
POST /devices/{device_id}/voice-samples
Content-Type: multipart/form-data
Authorization: Bearer {user_token}
```

**参数:**
- `audio`: 音频文件 (WAV格式)
- `label`: 标签 (可选)

**响应:**
```json
{
    "success": true,
    "sample_id": "vs_123456",
    "quality_score": 0.94,
    "status": "trained"
}
```

### 获取声纹样本列表

```http
GET /devices/{device_id}/voice-samples
Authorization: Bearer {user_token}
```

**响应:**
```json
{
    "samples": [
        {
            "id": "vs_123456",
            "created_at": "2026-03-22T10:00:00Z",
            "quality": "good",
            "score": 0.94
        }
    ],
    "model_status": "active",
    "accuracy": 0.94
}
```

### 下发声纹模型到设备

```http
POST /devices/{device_id}/voice-model/deploy
Authorization: Bearer {user_token}
```

**响应:**
```json
{
    "success": true,
    "model_url": "https://.../model.bin",
    "version": "20260322-001"
}
```

---

## 设备管理

### 更新设备信息

```http
PUT /devices/{device_id}
Authorization: Bearer {user_token}
```

**请求体:**
```json
{
    "name": "小宝的计数器",
    "settings": {
        "audio_threshold": 5200,
        "flip_mute": true
    }
}
```

### 绑定设备到用户

```http
POST /devices/{device_id}/bind
Authorization: Bearer {user_token}
```

**请求体:**
```json
{
    "ownership": "owner"  // 或 "shared"
}
```

---

## 分享功能

### 创建分享链接

```http
POST /devices/{device_id}/shares
Authorization: Bearer {user_token}
```

**请求体:**
```json
{
    "expires_in": 86400,  // 24小时
    "permissions": ["read"]
}
```

**响应:**
```json
{
    "share_id": "shr_abc123",
    "url": "https://.../share/shr_abc123",
    "expires_at": "2026-03-23T15:30:00Z"
}
```

### 通过分享链接访问

```http
GET /shares/{share_id}
```

**响应:**
```json
{
    "device_name": "小宝的计数器",
    "owner_name": "爸爸",
    "today_count": 23,
    "last_updated": "2026-03-22T15:30:00Z"
}
```

---

## 用户认证

### 用户登录 (Web端)

```http
POST /auth/login
```

**请求体:**
```json
{
    "username": "user@example.com",
    "password": "********"
}
```

**响应:**
```json
{
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": "usr_123",
        "name": "爸爸",
        "email": "user@example.com"
    }
}
```

### 微信扫码登录

```http
POST /auth/wechat/login
{
    "code": "wx_auth_code"
}
```

---

## 错误码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | 成功 | 请求处理成功 |
| 400 | 请求错误 | 参数错误或缺少必要字段 |
| 401 | 未授权 | Token无效或过期 |
| 403 | 禁止访问 | 无权访问该资源 |
| 404 | 未找到 | 设备或资源不存在 |
| 429 | 请求过多 | 超出API限流 |
| 500 | 服务器错误 | 内部错误 |

---

## 数据结构

### 设备对象

```json
{
    "device_id": "MC-A1B2C3D4",
    "name": "小宝的计数器",
    "model": "MC-ESP32S3-185",
    "firmware_version": "2.0.0",
    "status": "online",
    "last_seen": "2026-03-22T15:30:00Z",
    "owner_id": "usr_123",
    "created_at": "2026-03-22T10:00:00Z",
    "settings": {
        "audio_threshold": 5000,
        "flip_mute": true,
        "sync_interval": 300
    }
}
```

### 统计对象

```json
{
    "date": "2026-03-22",
    "device_id": "MC-A1B2C3D4",
    "total": 59,
    "periods": {
        "morning": 12,
        "forenoon": 18,
        "afternoon": 15,
        "evening": 14
    },
    "hourly": [2,3,4,3,0,0,1,2,3,4,5,4,3,4,5,3,2,1,2,3,4,3,2,1],
    "synced_at": "2026-03-22T23:59:59Z"
}
```
