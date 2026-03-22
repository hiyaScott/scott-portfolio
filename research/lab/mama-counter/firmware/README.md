# 妈妈计数器 ESP32-S3 固件 v2.0

## 硬件要求

- **开发板**: 微雪 ESP32-S3 1.85寸 圆形LCD开发板
- **外设**: 板载I2S麦克风、QMI8658陀螺仪、2个实体按键
- **电源**: 3.7V锂电池，Type-C充电

## 快速开始

### 1. 安装开发环境

**Arduino IDE:**
1. 安装 ESP32 开发板支持 (版本 >= 2.0.0)
   - 文件 → 首选项 → 附加开发板管理器网址:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
2. 工具 → 开发板 → ESP32 Arduino → ESP32S3 Dev Module

**PlatformIO (推荐):**
```ini
[env:esp32-s3-devkitc-1]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200
```

### 2. 安装依赖库

在 Arduino IDE 中安装以下库:
- `ArduinoJson` by Benoit Blanchon (v6.x)
- `TFT_eSPI` by Bodmer (屏幕驱动)
- `ESP32-audioI2S` (I2S音频，可选)

### 3. 配置屏幕驱动

编辑 `TFT_eSPI/User_Setup.h`:
```cpp
#define USER_SETUP_INFO "ESP32-S3 GC9A01"

#define GC9A01_DRIVER

#define TFT_WIDTH  360
#define TFT_HEIGHT 360

#define TFT_MISO -1
#define TFT_MOSI 11
#define TFT_SCLK 12
#define TFT_CS   10
#define TFT_DC   9
#define TFT_RST  8

#define LOAD_GLCD
#define LOAD_FONT2
#define LOAD_FONT4
#define LOAD_FONT6
#define LOAD_FONT7
#define LOAD_FONT8
#define LOAD_GFXFF

#define SMOOTH_FONT
```

### 4. 烧录固件

1. 连接开发板到电脑 (Type-C)
2. 选择端口: 工具 → 端口 → COMx (Windows) 或 /dev/ttyUSBx (Linux/Mac)
3. 点击上传按钮

### 5. 首次配置

**方式一: Web配网 (推荐)**
1. 首次启动时，设备会创建一个WiFi热点: `MamaCounter-XXXX`
2. 用手机/电脑连接该热点
3. 浏览器访问 `192.168.4.1`
4. 在网页中选择你的WiFi网络并输入密码
5. 设备会自动重启并连接

**方式二: 串口配置**
1. 打开串口监视器 (115200 baud)
2. 发送命令: `WIFI:SSID:PASSWORD`
3. 设备会保存配置并重启

## 功能说明

### 实体按键操作

| 按键 | 短按 | 长按 |
|------|------|------|
| KEY1 (左侧) | 切换显示模式 | 进入/退出设置菜单 |
| KEY2 (右侧) | 确认/选择 | 开关机 |

### 显示模式

1. **计数模式** - 显示今日喊妈妈总次数
2. **今日统计** - 显示早/上/下/晚时段分布
3. **本周趋势** - 显示最近7天柱状图
4. **电池状态** - 显示电量和系统信息

### 设置菜单

1. **声纹录制** - 录制孩子的"妈妈"声纹样本
2. **WiFi配置** - 重新配置网络
3. **灵敏度调节** - 调整声音检测灵敏度
4. **查看设备ID** - 显示设备唯一标识
5. **恢复出厂** - 清除所有数据
6. **返回** - 退出设置菜单

## 数据同步

设备每5分钟自动同步数据到云端 (如果WiFi已连接)。

同步内容:
- 今日计数
- 时段分布
- 总使用次数
- 电池电量

## 设备ID

每个设备有唯一的ID，格式: `MC-XXXXXXXX`
- 基于ESP32芯片MAC地址生成
- 首次启动时自动生成并保存到Flash
- 用于云端数据关联

## 配网页面代码

`wifi_config.html` 需要放在 `data/` 目录下，烧录到SPIFFS。

详细配网代码见 `wifi_portal.ino` 示例。

## 调试

通过串口发送命令进行调试:
- `status` - 显示设备状态
- `reset` - 重置今日计数
- `trigger` - 模拟一次"妈妈"触发
- `wifi:clear` - 清除WiFi配置
- `sleep` - 进入深度睡眠

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法上传 | 按住BOOT键，点击RESET，然后上传 |
| WiFi连接失败 | 检查密码，尝试重新配网 |
| 屏幕不显示 | 检查TFT_eSPI配置是否正确 |
| 数据不同步 | 检查WiFi连接，查看串口日志 |
| 识别率低 | 重新录制声纹样本 |

## 文件说明

```
firmware/
├── MamaCounter_ESP32S3.ino    # 主程序
├── config.h                    # 配置常量
├── display.cpp/.h              # 屏幕显示模块
├── audio.cpp/.h                # 音频检测模块
├── wifi_manager.cpp/.h         # WiFi管理模块
├── buttons.cpp/.h              # 按键处理模块
└── wifi_config.html            # 配网页面
```

## 下一步开发

需要完成的部分 (标记为 TODO):
1. LCD屏幕绘制函数
2. I2S音频采集和关键词检测
3. 陀螺仪翻转检测
4. 完整的声纹录制流程
5. Web配网AP模式
6. NTP时间同步

## 许可

MIT License
