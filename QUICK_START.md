# 快速开始指南

## 🚀 启动定时任务（每30分钟自动抓取）

### 方法 1: 使用启动脚本（最简单）

```bash
./start_scheduler.sh
```

### 方法 2: 直接运行 Python 脚本

```bash
python3 scheduler.py
```

### 方法 3: 后台运行

```bash
nohup python3 scheduler.py > scheduler.log 2>&1 &
```

查看日志：
```bash
tail -f scheduler.log
```

## 🔴 只抓取阿森纳新闻

设置环境变量：

```bash
export FILTER_ARSENAL=true
python3 scheduler.py
```

或在启动脚本中取消注释：
```bash
# export FILTER_ARSENAL=true  # 取消注释这行
./start_scheduler.sh
```

## 📝 配置选项

### 使用免费翻译（推荐）

```bash
export USE_FREE_TRANSLATOR=true
python3 scheduler.py
```

### 使用 OpenAI API（如果有）

```bash
export OPENAI_API_KEY="your-key-here"
python3 scheduler.py
```

## 📊 已添加的阿森纳新闻源

- ✅ BBC Arsenal RSS Feed
- ✅ Sky Sports Arsenal RSS Feed  
- ✅ 阿森纳相关记者：
  - Charles Watts (@charles_watts)
  - James Benge (@jamesbenge)
  - Chris Wheatley (@ChrisWheatley_)
  - David Ornstein (@David_Ornstein)

## ⏰ 执行频率

默认：每30分钟执行一次

修改频率：编辑 `scheduler.py` 中的：
```python
schedule.every(30).minutes.do(run_news_fetch)
```

## 📁 输出文件

- `football_news_translated.json` - 原始输出文件
- `public/news.json` - 网站使用的文件（自动更新）

## 🛑 停止服务

- 前台运行：按 `Ctrl+C`
- 后台运行：
  ```bash
  ps aux | grep scheduler.py
  kill <PID>
  ```

## ✅ 验证

1. 检查日志输出
2. 查看 `public/news.json` 文件是否更新
3. 刷新网站查看最新新闻

