# 組み込み開発ガイド
# My-devin for Embedded Systems & RTOS

My-devinを使った組み込みシステム開発とリアルタイムOS（RTOS）開発の完全ガイドです。

---

## 目次

1. [概要](#1-概要)
2. [対応RTOS](#2-対応rtos)
3. [対応マイコン](#3-対応マイコン)
4. [セットアップ](#4-セットアップ)
5. [基本的な使い方](#5-基本的な使い方)
6. [コード生成例](#6-コード生成例)
7. [ベストプラクティス](#7-ベストプラクティス)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. 概要

### 1.1 My-devinの組み込み開発支援機能

My-devinは、**C++を中心とした組み込みシステム開発**に特化したLLM開発支援ツールです。

**主な特徴:**
- ✅ FreeRTOS/Zephyr等の主要RTOS対応
- ✅ STM32, ESP32, nRF52等の人気マイコン対応
- ✅ MISRA C++, CERT C++等の安全規格準拠
- ✅ メモリ制約を考慮したコード生成
- ✅ リアルタイム性を保証するコード設計
- ✅ ペリフェラル制御コード自動生成
- ✅ 割り込み処理・タスク管理コード

### 1.2 想定ユースケース

- **IoTデバイス開発**: センサーデータ収集・クラウド送信
- **産業機器制御**: モーター制御・PLCプログラミング
- **ウェアラブルデバイス**: 低消費電力・BLE通信
- **ロボティクス**: センサーフュージョン・モーション制御
- **車載システム**: AUTOSAR準拠・CAN通信
- **医療機器**: IEC 62304準拠・安全性重視

---

## 2. 対応RTOS

### 2.1 FreeRTOS（最優先対応）

**特徴:**
- 最も広く使われているRTOS
- 多数のマイコンベンダーが公式サポート
- MIT/Apacheライセンス（商用利用可）
- AWS IoT Core統合（AWS FreeRTOS）

**対応バージョン:** 10.5.x, 10.6.x, 11.x

**主要API:**
```cpp
// タスク管理
xTaskCreate(), xTaskCreateStatic(), vTaskDelete()
vTaskDelay(), vTaskDelayUntil()

// キュー
xQueueCreate(), xQueueSend(), xQueueReceive()

// セマフォ
xSemaphoreCreateBinary(), xSemaphoreGive(), xSemaphoreTake()

// ミューテックス
xSemaphoreCreateMutex()

// タイマー
xTimerCreate(), xTimerStart()
```

### 2.2 Zephyr

**特徴:**
- Linux Foundation主導のモダンRTOS
- デバイスツリーベースの設定
- 豊富なネットワークスタック
- Bluetoothスタック内蔵

**対応バージョン:** 3.x

### 2.3 Mbed OS

**特徴:**
- ARM公式RTOS
- C++ベースのAPI
- ハイレベル抽象化

**対応バージョン:** 6.x

### 2.4 その他

- **RIOT OS**: Linux風API、モジュラー設計
- **Azure RTOS (ThreadX)**: Microsoft製、組み込みLinux代替
- **RT-Thread**: 中国発、豊富な日本語ドキュメント

---

## 3. 対応マイコン

### 3.1 STMicroelectronics STM32

**対応シリーズ:**
- **STM32F0**: エントリーレベル（Cortex-M0）
- **STM32F1**: 汎用（Cortex-M3）
- **STM32F4**: ハイパフォーマンス（Cortex-M4F）
- **STM32F7**: 超高速（Cortex-M7）
- **STM32H7**: 最高性能（Cortex-M7, 480MHz）
- **STM32L4**: 低消費電力（Cortex-M4F）
- **STM32G4**: アナログ強化

**開発環境:**
- STM32CubeMX（初期設定生成）
- STM32CubeIDE（Eclipse+GCC）
- HAL（Hardware Abstraction Layer）

### 3.2 Espressif ESP32/ESP8266

**特徴:**
- Wi-Fi/Bluetooth内蔵
- 低価格・高性能
- Arduino互換

**対応フレームワーク:**
- ESP-IDF（推奨）
- Arduino Framework
- PlatformIO

### 3.3 Nordic Semiconductor nRF52/nRF53

**特徴:**
- Bluetooth Low Energy特化
- 超低消費電力
- SoftDevice（BLEスタック）

**シリーズ:**
- nRF52832: BLE 5.0
- nRF52840: BLE 5.1, USB, NFC
- nRF5340: デュアルコア（M33）

### 3.4 Raspberry Pi Pico (RP2040)

**特徴:**
- デュアルCortex-M0+
- PIO（Programmable I/O）
- 低価格（$4）

**SDK:**
- Pico SDK（C/C++）
- MicroPython

### 3.5 その他

- **Texas Instruments**: MSP430, CC26xx (Sub-1GHz/BLE)
- **NXP**: i.MX RT, LPCシリーズ
- **Renesas**: RX, RAシリーズ
- **Microchip**: SAM, PIC32

---

## 4. セットアップ

### 4.1 環境変数設定

`.env`ファイルに組み込み開発設定を追加:

```bash
# 組み込み開発モード有効化
EMBEDDED_MODE=true

# ターゲットRTOS
DEFAULT_RTOS=freertos

# ターゲットマイコン
TARGET_MCU=stm32f4

# C++標準
CPP_STANDARD=c++17

# 最適化レベル
OPTIMIZATION=O2
```

### 4.2 config/default.yaml設定

```yaml
embedded_development:
  default_rtos: freertos

  targets:
    default: stm32

    stm32:
      series: "STM32F4"
      hal_version: "1.27.1"

  memory:
    flash_size: 512  # KB
    ram_size: 128    # KB

  peripherals:
    uart:
      enabled: true
      default_baudrate: 115200

    i2c:
      enabled: true
      speed: "fast"  # 400kHz
```

### 4.3 ツールチェーンインストール

#### macOS (Homebrew)

```bash
# ARM GCC Toolchain
brew install --cask gcc-arm-embedded

# または最新版
brew tap ArmMbed/homebrew-formulae
brew install arm-none-eabi-gcc

# OpenOCD（デバッグ）
brew install open-ocd

# ST-Link（STM32専用）
brew install stlink
```

#### 確認

```bash
arm-none-eabi-gcc --version
# arm-none-eabi-gcc (GNU Arm Embedded Toolchain 10.3-2021.10) 10.3.1

openocd --version
# Open On-Chip Debugger 0.12.0
```

---

## 5. 基本的な使い方

### 5.1 CLIからコード生成

#### FreeRTOSタスク生成

```bash
my-devin generate \
  "FreeRTOSでLEDを1秒ごとに点滅させるタスクを作成" \
  --language cpp \
  --rtos freertos \
  --target stm32f4
```

**生成されるコード例:**

```cpp
#include "FreeRTOS.h"
#include "task.h"
#include "stm32f4xx_hal.h"

// タスク設定
constexpr size_t LED_TASK_STACK_SIZE = 128;
constexpr UBaseType_t LED_TASK_PRIORITY = tskIDLE_PRIORITY + 1;

// 静的割り当て
static StackType_t ledTaskStack[LED_TASK_STACK_SIZE];
static StaticTask_t ledTaskBuffer;

// LEDタスク
void ledTask(void* params) {
    // LED初期化（PA5ピン）
    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_InitTypeDef GPIO_InitStruct = {};
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    while (1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        vTaskDelay(pdMS_TO_TICKS(1000));  // 1秒待機
    }
}

// タスク作成関数
void createLedTask() {
    TaskHandle_t handle = xTaskCreateStatic(
        ledTask,
        "LED",
        LED_TASK_STACK_SIZE,
        nullptr,
        LED_TASK_PRIORITY,
        ledTaskStack,
        &ledTaskBuffer
    );
    configASSERT(handle != nullptr);
}
```

#### UART通信コード生成

```bash
my-devin generate \
  "STM32F4でUART2（115200bps）を使ってHello Worldを送信" \
  --language cpp \
  --target stm32f4
```

#### I2Cセンサー読み取り

```bash
my-devin generate \
  "STM32F4のI2C1を使ってBME280温度センサーからデータ読み取り" \
  --language cpp \
  --target stm32f4 \
  --peripheral i2c
```

### 5.2 対話モードで開発

```bash
my-devin chat --mode embedded
```

**対話例:**

```
User: FreeRTOSで3つのタスクを作成したい。LED点滅、UART送信、ADC読み取り。