# FaceTime 自动拨号实现方案

## 项目概述

本项目实现了一个自动化解决方案，可以通过命令行自动发起 FaceTime 视频通话。通过获取窗口位置、计算按钮坐标、模拟鼠标点击等步骤，实现全程自动化拨号。

## 核心技术点

### 1. URL Scheme 启动 FaceTime

macOS 提供了 URL Scheme 来启动应用并传递参数：

```bash
open "facetime:hgdemail@icloud.com"
```

**重要提示**：必须使用 iCloud 邮箱或其他已注册 FaceTime 的邮箱，Hotmail 邮箱无法使用。

### 2. 获取窗口信息

使用 AppleScript 获取 FaceTime 窗口的位置和大小：

```bash
# 获取窗口位置 (左上角坐标)
osascript -e 'tell application "System Events" to tell process "FaceTime" to get position of window 1'
# 返回格式: x, y (如: 113, 222)

# 获取窗口大小
osascript -e 'tell application "System Events" to tell process "FaceTime" to get size of window 1'
# 返回格式: width, height (如: 980, 612)
```

### 3. 计算通话按钮坐标

FaceTime 窗口中的"通话"按钮位于左下角，位置计算公式：

```
button_x = window_x + 200
button_y = window_y + window_height - 20
```

### 4. 模拟鼠标点击

使用 cliclick 工具进行鼠标点击：

```bash
cliclick c:200,790
```

cliclick 是 macOS 上的命令行鼠标控制工具，可以通过 Homebrew 安装：

```bash
brew install cliclick
```

### 5. 验证通话状态

通过截图并使用 AI 分析图片来确认通话是否成功：

```bash
# 截图
screencapture ~/Desktop/facetiming.png

# 使用 mcporter + MiniMax 分析图片
mcporter call coding-plan-mcp.understand_image prompt="FaceTime是在通话中吗？" image_source="~/Desktop/facetiming.png"
```

## 完整 Python 实现代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FaceTime 自动拨号脚本
功能：自动打开 FaceTime 并发起视频通话到指定联系人
"""

import subprocess
import time
import os

# ============== 配置区 ==============
TARGET_CONTACT = "hgdemail@icloud.com"  # 必须是 iCloud 邮箱

def run_command(cmd):
    """执行系统命令并返回结果"""
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True
    )
    return result.stdout.strip()

def open_facetime(contact):
    """步骤1: 使用 URL Scheme 打开 FaceTime"""
    print(f"正在打开 FaceTime，呼叫: {contact}")
    run_command(f'open "facetime:{contact}"')
    time.sleep(2)  # 等待 FaceTime 加载

def get_window_position():
    """步骤2: 获取 FaceTime 窗口位置"""
    pos_str = run_command(
        'osascript -e \'tell application "System Events" to tell process "FaceTime" to get position of window 1\''
    )
    x, y = map(int, pos_str.split(', '))
    return {'x': x, 'y': y}

def get_window_size():
    """步骤3: 获取 FaceTime 窗口大小"""
    size_str = run_command(
        'osascript -e \'tell application "System Events" to tell process "FaceTime" to get size of window 1\''
    )
    width, height = map(int, size_str.split(', '))
    return {'width': width, 'height': height}

def calculate_call_button_position(window_pos, window_size):
    """
    步骤4: 计算通话按钮的点击坐标
    按钮位于窗口左下角
    """
    button_x = window_pos['x'] + 200
    button_y = window_pos['y'] + window_size['height'] - 20
    return button_x, button_y

def click_at(x, y):
    """步骤5: 使用 cliclick 点击指定坐标"""
    run_command(f'cliclick c:{x},{y}')

def main():
    """主函数：执行完整的 FaceTime 拨号流程"""
    # 1. 打开 FaceTime
    open_facetime(TARGET_CONTACT)
    
    # 2. 获取窗口信息
    window_pos = get_window_position()
    window_size = get_window_size()
    
    # 3. 计算按钮位置并点击
    button_x, button_y = calculate_call_button_position(window_pos, window_size)
    click_at(button_x, button_y)
    
    print("通话已发起!")

if __name__ == "__main__":
    main()
```

## 流程图

```
开始
  │
  ▼
配置联系人 (hgdemail@icloud.com)
  │
  ▼
打开 FaceTime (open "facetime:xxx")
  │
  ▼
等待 2 秒
  │
  ▼
获取窗口位置 (osascript position)
  │
  ▼
获取窗口大小 (osascript size)
  │
  ▼
计算按钮坐标 (x=win_x+200, y=win_y+win_h-20)
  │
  ▼
点击通话按钮 (cliclick c:x,y)
  │
  ▼
截图验证
  │
  ▼
┌───────┴───────┐
│   通话成功?   │
└───────┬───────┘
    │
    ├── 是 ──► 通话中 ✅
    │
    └── 否 ──► 显示错误? ──► 报错：检查联系人 ❌
```

## 所需工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| cliclick | 命令行鼠标控制 | `brew install cliclick` |
| osascript | 执行 AppleScript | macOS 内置 |
| mcporter | AI 图片分析 | `npm i -g mcporter` |

## 常见问题

### Q1: 点击按钮无效怎么办？
- 确保 FaceTime 窗口已完全加载
- 尝试调整坐标偏移量

### Q2: 提示"无法用于 FaceTime 通话"？
- 检查目标邮箱是否为 iCloud 邮箱
- 确认对方已开通 FaceTime

### Q3: 如何自动接听来电？
- 可以设置 FaceTime 自动接听（需在系统偏好设置中配置）

## 项目文件

- 脚本文件：`~/Documents/aiwork/scripts/facetime_auto_dial.py`
- AppleScript：`~/Documents/aiwork/FaceTime.scpt`
- Skill配置：`~/.openclaw/skills/facetime-call/SKILL.md`

## 作者

Gordon | 2026-02-24
