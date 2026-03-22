# 妈妈计数器 固件与代码

## 📦 固件代码

### 主程序
**文件**: [`MamaCounter_ESP32S3.ino`](MamaCounter_ESP32S3.ino)

主要功能:
- 实体按键处理 (KEY1/KEY2 短按/长按)
- 4种显示模式切换
- 时段统计 (早/上/下/晚)
- WiFi连接和数据同步
- 设备唯一ID生成
- 本地数据缓存 (Flash存储)

**TODO (硬件到了后开发):**
- LCD屏幕驱动 (GC9A01)
- I2S麦克风音频采集
- "妈妈"关键词检测 (ESP-SR库)
- QMI8658陀螺仪翻转检测

---

### WiFi配网
**文件**: [`wifi_portal.ino`](wifi_portal.ino)

功能: 首次启动时创建AP热点，提供Web页面配置WiFi

配网页面预览:
```
┌─────────────────────────────┐
│           👩‍👧               │
│       妈妈计数器             │
│        WiFi配置              │
├─────────────────────────────┤
│  设备ID: MC-A1B2C3D4        │
├─────────────────────────────┤
│  📶 选择WiFi网络             │
│  🔄 刷新列表                 │
│                             │
│  ● HomeWiFi    ●●●          │
│  ● OfficeNet   ●●○          │
│  ● Guest       ●○○          │
│                             │
│  密码: [____________]       │
│                             │
│  [    连接网络    ]         │
└─────────────────────────────┘
```

---

## 📚 技术文档

### 1. 编译烧录指南
**文件**: [`README.md`](README.md)

包含:
- Arduino IDE / PlatformIO 配置
- 依赖库安装
- TFT_eSPI屏幕驱动配置
- 烧录步骤
- 故障排除

### 2. API接口文档
**文件**: [`API.md`](API.md)

REST API接口:
- 设备注册: `POST /devices/register`
- 数据同步: `POST /devices/{id}/sync`
- 统计查询: `GET /devices/{id}/stats/daily`
- 声纹管理: `POST /devices/{id}/voice-samples`
- 分享功能: `POST /devices/{id}/shares`

### 3. 架构设计
**文件**: [`ARCHITECTURE.md`](ARCHITECTURE.md)

内容:
- 前后端如何匹配
- 设备身份识别机制
- 多设备数据隔离方案
- 权限控制 (Owner/Admin/Viewer/Guest)
- 实际部署建议

---

## 🚀 快速开始

### 硬件准备
- 微雪 ESP32-S3 1.85寸 圆形LCD开发板
- Type-C数据线
- 3.7V锂电池 (可选，用于便携)

### 软件准备
1. 安装 [Arduino IDE](https://www.arduino.cc/en/software)
2. 添加 ESP32 开发板支持
3. 安装库: `ArduinoJson`, `TFT_eSPI`

### 烧录步骤
1. 下载 [`MamaCounter_ESP32S3.ino`](MamaCounter_ESP32S3.ino)
2. 用Arduino IDE打开
3. 选择开发板: `ESP32S3 Dev Module`
4. 选择端口 (COMx 或 /dev/ttyUSBx)
5. 点击上传

### 首次使用
1. 设备启动后会创建WiFi热点: `MamaCounter-XXXX`
2. 手机连接热点，访问 `192.168.4.1`
3. 选择你的WiFi网络，输入密码
4. 设备自动重启并连接
5. 访问 [Web应用](../web-app/) 查看数据

---

## 📋 功能实现状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 按键驱动 | ✅ | GPIO中断处理 |
| WiFi连接 | ✅ | Station模式 + SmartConfig备选 |
| Web配网 | ✅ | AP模式 + Web服务器 |
| 数据同步 | ✅ | HTTP POST到云端 |
| 本地存储 | ✅ | Preferences库持久化 |
| 屏幕显示 | ⏳ | 等待GC9A01驱动 |
| 音频采集 | ⏳ | 等待I2S麦克风驱动 |
| 关键词检测 | ⏳ | 等待ESP-SR集成 |
| 陀螺仪 | ⏳ | 等待QMI8658驱动 |

---

## 🔧 开发计划

**Phase 1: 基础功能 (硬件到后1周内)**
- [ ] 屏幕驱动 (显示计数界面)
- [ ] 音频采集 + 简单阈值检测
- [ ] 基本计数功能

**Phase 2: 完整体验 (第2-3周)**
- [ ] 4种显示模式
- [ ] 时段统计
- [ ] 陀螺仪翻转静音

**Phase 3: 智能化 (第4周)**
- [ ] ESP-SR关键词识别
- [ ] 声纹录制
- [ ] 远程配置更新

---

## 📞 问题反馈

如有固件问题，请记录:
- 设备ID (屏幕显示或串口输出)
- 串口日志 (115200 baud)
- 复现步骤

---

*固件版本: v2.0.0-beta*  
*最后更新: 2026-03-22*
