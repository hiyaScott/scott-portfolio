/*
 * 蓝牙语音输入器 - ESP32-S3 蓝牙HID键盘验证代码
 * 
 * 功能:
 * 1. 初始化BLE HID键盘设备
 * 2. 通过按键触发模拟键盘输入
 * 3. 支持发送字符串、按键组合
 * 4. 状态LED反馈
 * 
 * 硬件: ESP32-S3 DevKitC-1
 * 按键: GPIO 0 (Boot键，用于测试)
 * LED: GPIO 2 (板载LED)
 */

#include <BleKeyboard.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>

// ============ 引脚定义 ============
#define BUTTON_PIN    0    // Boot键，低电平触发
#define LED_PIN       2    // 板载LED
#define I2S_SD_PIN    4    // I2S麦克风数据
#define I2S_SCK_PIN   5    // I2S麦克风时钟
#define I2S_WS_PIN    6    // I2S麦克风字选

// ============ OLED屏幕 ============
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ============ 蓝牙键盘 ============
BleKeyboard bleKeyboard("语音输入器", "虾折腾", 100);

// ============ 状态变量 ============
enum DeviceState {
  STATE_INIT,       // 初始化
  STATE_PAIRING,    // 配对中
  STATE_STANDBY,    // 待机
  STATE_RECORDING,  // 录音中
  STATE_PROCESSING, // 处理中
  STATE_ERROR       // 错误
};

DeviceState currentState = STATE_INIT;
bool buttonPressed = false;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;

// 测试用的模拟语音识别结果
const char* testPhrases[] = {
  "你好，这是蓝牙语音输入器的测试。",
  "Hello, this is a Bluetooth voice input device test.",
  "今天天气真不错！",
  "ESP32-S3 is powerful and energy efficient.",
  "换行测试：\n第一行\n第二行\n第三行"
};
int testIndex = 0;

// ============ 函数声明 ============
void updateDisplay();
void setLED(uint8_t r, uint8_t g, uint8_t b);
void handleButton();
void sendText(const char* text);
void changeState(DeviceState newState);
void drawCenteredText(const char* text, int y, int size = 1);

// ============ 初始化 ============
void setup() {
  Serial.begin(115200);
  Serial.println("\n=================================");
  Serial.println("  蓝牙语音输入器 - HID键盘验证");
  Serial.println("=================================\n");
  
  // 初始化引脚
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // 初始化OLED
  Wire.setPins(8, 9);  // SDA=GPIO8, SCL=GPIO9 (ESP32-S3默认I2C)
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306初始化失败"));
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.display();
  
  // 显示启动画面
  drawCenteredText("语音输入器", 20, 2);
  drawCenteredText("虾折腾实验室", 45, 1);
  display.display();
  delay(1500);
  
  // 初始化蓝牙键盘
  Serial.println("正在启动蓝牙HID键盘...");
  display.clearDisplay();
  drawCenteredText("蓝牙启动中...", 28, 1);
  display.display();
  
  bleKeyboard.begin();
  changeState(STATE_PAIRING);
  
  Serial.println("初始化完成，等待蓝牙连接...");
  Serial.println("请打开电脑蓝牙设置，搜索并连接'语音输入器'");
}

// ============ 主循环 ============
void loop() {
  // 处理按键
  handleButton();
  
  // 检查蓝牙连接状态
  if (bleKeyboard.isConnected()) {
    if (currentState == STATE_PAIRING) {
      changeState(STATE_STANDBY);
      Serial.println("蓝牙已连接！");
    }
  } else {
    if (currentState != STATE_PAIRING && currentState != STATE_INIT) {
      changeState(STATE_PAIRING);
      Serial.println("蓝牙已断开，等待重新连接...");
    }
  }
  
  // 状态机处理
  switch (currentState) {
    case STATE_PAIRING:
      // 配对中: LED快闪蓝光
      digitalWrite(LED_PIN, (millis() / 250) % 2);
      break;
      
    case STATE_STANDBY:
      // 待机: LED熄灭或呼吸
      digitalWrite(LED_PIN, LOW);
      break;
      
    case STATE_RECORDING:
      // 录音中: LED常亮
      digitalWrite(LED_PIN, HIGH);
      break;
      
    case STATE_PROCESSING:
      // 处理中: LED闪烁
      digitalWrite(LED_PIN, (millis() / 500) % 2);
      break;
      
    default:
      break;
  }
  
  delay(10);
}

// ============ 按键处理 ============
void handleButton() {
  int reading = digitalRead(BUTTON_PIN);
  
  // 按键按下 (低电平)
  if (reading == LOW && !buttonPressed) {
    if (millis() - lastDebounceTime > debounceDelay) {
      buttonPressed = true;
      lastDebounceTime = millis();
      
      if (currentState == STATE_STANDBY) {
        // 开始录音
        changeState(STATE_RECORDING);
        Serial.println("开始录音...");
      }
    }
  }
  
  // 按键释放
  if (reading == HIGH && buttonPressed) {
    if (millis() - lastDebounceTime > debounceDelay) {
      buttonPressed = false;
      lastDebounceTime = millis();
      
      if (currentState == STATE_RECORDING) {
        // 停止录音，开始处理
        changeState(STATE_PROCESSING);
        Serial.println("录音结束，处理中...");
        
        // 模拟语音识别处理
        delay(800);  // 模拟处理时间
        
        // 发送测试文本
        if (bleKeyboard.isConnected()) {
          const char* textToSend = testPhrases[testIndex];
          sendText(textToSend);
          
          testIndex = (testIndex + 1) % 5;  // 循环测试语句
          changeState(STATE_STANDBY);
        } else {
          Serial.println("蓝牙未连接！");
          changeState(STATE_ERROR);
          delay(1000);
          changeState(STATE_STANDBY);
        }
      }
    }
  }
}

// ============ 发送文字 ============
void sendText(const char* text) {
  Serial.print("发送文字: ");
  Serial.println(text);
  
  // 在屏幕上显示发送内容
  display.clearDisplay();
  drawCenteredText("发送中...", 10, 1);
  
  // 显示要发送的文字（截断以适应屏幕）
  display.setCursor(0, 30);
  display.setTextSize(1);
  String displayText = String(text);
  if (displayText.length() > 21) {
    display.println(displayText.substring(0, 21));
    display.println(displayText.substring(21, 42));
  } else {
    display.println(displayText);
  }
  display.display();
  
  // 通过BLE发送文字
  bleKeyboard.print(text);
  
  // 发送成功反馈
  delay(200);
  display.clearDisplay();
  drawCenteredText("✓ 已发送", 28, 2);
  display.display();
  delay(800);
}

// ============ 状态切换 ============
void changeState(DeviceState newState) {
  currentState = newState;
  updateDisplay();
  
  switch (newState) {
    case STATE_PAIRING:
      Serial.println("[状态] 配对中...");
      break;
    case STATE_STANDBY:
      Serial.println("[状态] 待机");
      break;
    case STATE_RECORDING:
      Serial.println("[状态] 录音中");
      break;
    case STATE_PROCESSING:
      Serial.println("[状态] 处理中");
      break;
    case STATE_ERROR:
      Serial.println("[状态] 错误");
      break;
    default:
      break;
  }
}

// ============ 更新屏幕显示 ============
void updateDisplay() {
  display.clearDisplay();
  
  // 顶部状态栏
  display.setCursor(0, 0);
  display.setTextSize(1);
  
  // 蓝牙状态图标
  if (bleKeyboard.isConnected()) {
    display.print("[BLE✓]");
  } else {
    display.print("[BLE○]");
  }
  
  // 电量（模拟）
  display.setCursor(90, 0);
  display.print("85%");
  
  // 分隔线
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);
  
  // 主内容区
  switch (currentState) {
    case STATE_PAIRING:
      drawCenteredText("等待连接", 30, 2);
      drawCenteredText("请打开蓝牙设置", 50, 1);
      break;
      
    case STATE_STANDBY:
      drawCenteredText("准备就绪", 28, 2);
      drawCenteredText("按住按键开始录音", 50, 1);
      break;
      
    case STATE_RECORDING:
      drawCenteredText("● 录音中", 28, 2);
      // 模拟波形
      for (int i = 0; i < 100; i += 5) {
        int h = random(5, 15);
        display.drawLine(14 + i, 55 - h, 14 + i, 55 + h, SSD1306_WHITE);
      }
      break;
      
    case STATE_PROCESSING:
      drawCenteredText("处理中...", 28, 2);
      // 转圈动画
      static int angle = 0;
      angle = (angle + 30) % 360;
      int x = 64 + 15 * cos(radians(angle));
      int y = 55 + 15 * sin(radians(angle));
      display.fillCircle(x, y, 3, SSD1306_WHITE);
      break;
      
    case STATE_ERROR:
      drawCenteredText("✗ 错误", 28, 2);
      drawCenteredText("请检查蓝牙连接", 50, 1);
      break;
      
    default:
      break;
  }
  
  display.display();
}

// ============ 绘制居中文字 ============
void drawCenteredText(const char* text, int y, int size) {
  display.setTextSize(size);
  int16_t x1, y1;
  uint16_t w, h;
  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);
  display.setCursor((SCREEN_WIDTH - w) / 2, y);
  display.println(text);
}

// ============ 高级HID功能示例 ============

/*
 * 以下为扩展功能示例代码，可根据需要启用
 */

// 发送组合键 (例如 Ctrl+C)
void sendKeyCombination(uint8_t key, uint8_t modifier) {
  bleKeyboard.press(modifier);
  bleKeyboard.press(key);
  delay(100);
  bleKeyboard.releaseAll();
}

// 发送多媒体键
void sendMediaKey(uint8_t mediaKey) {
  bleKeyboard.write(mediaKey);
}

// 支持的按键常量参考
/*
 * 普通按键: KEY_LEFT_CTRL, KEY_LEFT_SHIFT, KEY_LEFT_ALT, KEY_LEFT_GUI
 *          KEY_RIGHT_CTRL, KEY_RIGHT_SHIFT, KEY_RIGHT_ALT, KEY_RIGHT_GUI
 *          KEY_UP_ARROW, KEY_DOWN_ARROW, KEY_LEFT_ARROW, KEY_RIGHT_ARROW
 *          KEY_BACKSPACE, KEY_TAB, KEY_RETURN, KEY_ESC, KEY_INSERT
 *          KEY_DELETE, KEY_PAGE_UP, KEY_PAGE_DOWN, KEY_HOME, KEY_END
 *          KEY_CAPS_LOCK, KEY_F1 ~ KEY_F12
 * 
 * 多媒体键: KEY_MEDIA_PLAY_PAUSE, KEY_MEDIA_STOP
 *          KEY_MEDIA_NEXT_TRACK, KEY_MEDIA_PREVIOUS_TRACK
 *          KEY_MEDIA_VOLUME_UP, KEY_MEDIA_VOLUME_DOWN, KEY_MEDIA_MUTE
 */

// 模拟完整的语音输入流程（测试用）
void simulateVoiceInput() {
  Serial.println("\n=== 模拟语音识别流程 ===");
  
  // 1. 开始录音
  changeState(STATE_RECORDING);
  delay(2000);  // 模拟2秒录音
  
  // 2. 处理中
  changeState(STATE_PROCESSING);
  delay(1000);  // 模拟处理
  
  // 3. 发送结果
  sendText("这是模拟的语音识别结果。");
  
  changeState(STATE_STANDBY);
  Serial.println("=== 流程结束 ===\n");
}
