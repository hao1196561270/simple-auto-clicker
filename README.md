# 鼠标连点器（简易自动点击工具）

一个使用 Python + tkinter 制作的简单自动连点工具，支持：

- 自定义点击间隔（毫秒级）
- 同时支持左/中/右键（可多选）
- 可选同时按下指定键盘按键
- 两种启动方式：  
  - F6 按住即连点（松开即停止）  
  - F7 一键切换开/关

适合游戏刷图、重复点击、自动化测试等场景。

## 功能截图（建议自己运行后截图放上来）

（可放 1-3 张界面截图）

## 系统要求

- Windows 10 / 11（推荐）  
- Python 3.8 ~ 3.11  
- 需要管理员权限运行（部分游戏/软件会检测非管理员点击）

## 依赖安装

```bash
# 强烈建议新建虚拟环境
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS/Linux

# 安装所需库
pip install pynput tkinter
