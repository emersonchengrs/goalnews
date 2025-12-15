# 定时任务使用指南

## 功能说明

定时任务调度器会每30分钟自动执行一次新闻抓取脚本，自动更新 `public/news.json` 文件。

## 安装依赖

```bash
pip3 install -r requirements.txt
```

## 使用方法

### 方法 1: 使用启动脚本（推荐）

```bash
./start_scheduler.sh
```

### 方法 2: 直接运行 Python 脚本

```bash
python3 scheduler.py
```

### 方法 3: 后台运行（使用 nohup）

```bash
nohup python3 scheduler.py > scheduler.log 2>&1 &
```

查看日志：
```bash
tail -f scheduler.log
```

### 方法 4: 使用 systemd（Linux）

创建服务文件 `/etc/systemd/system/goalnews.service`:

```ini
[Unit]
Description=GoalNews Scheduler
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/goalnews
ExecStart=/usr/bin/python3 /path/to/goalnews/scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable goalnews
sudo systemctl start goalnews
sudo systemctl status goalnews
```

## 配置选项

### 环境变量

在运行前设置环境变量：

```bash
# 使用免费翻译（默认）
export USE_FREE_TRANSLATOR=true

# 只抓取阿森纳相关新闻
export FILTER_ARSENAL=true

# 使用 OpenAI API（如果有）
export OPENAI_API_KEY="your-key-here"

# 使用 RapidAPI（如果需要）
export USE_RAPIDAPI=true
export RAPIDAPI_KEY="your-key-here"
```

### 只抓取阿森纳新闻

```bash
# 方法 1: 设置环境变量
export FILTER_ARSENAL=true
python3 scheduler.py

# 方法 2: 修改 scheduler.py 中的 filter_arsenal 参数
```

## 执行频率

默认每30分钟执行一次。如需修改，编辑 `scheduler.py`:

```python
# 改为每15分钟
schedule.every(15).minutes.do(run_news_fetch)

# 改为每小时
schedule.every().hour.do(run_news_fetch)

# 改为每天特定时间
schedule.every().day.at("10:30").do(run_news_fetch)
```

## 日志输出

调度器会输出以下信息：
- 每次执行的时间戳
- 执行结果（成功/失败）
- 错误信息（如果有）

## 停止服务

- 前台运行：按 `Ctrl+C`
- 后台运行：找到进程并终止
  ```bash
  ps aux | grep scheduler.py
  kill <PID>
  ```

## 故障排查

### 问题：脚本执行失败

1. 检查依赖是否安装完整
2. 检查网络连接
3. 查看错误日志

### 问题：数据未更新

1. 检查 `public/news.json` 文件权限
2. 检查脚本执行是否成功
3. 查看调度器日志

### 问题：翻译失败

1. 检查是否设置了 `USE_FREE_TRANSLATOR=true`
2. 检查网络是否能访问 Google Translate
3. 如果使用 OpenAI，检查 API Key 是否正确

## 阿森纳新闻源

已添加以下阿森纳相关新闻源：
- BBC Arsenal RSS Feed
- Sky Sports Arsenal RSS Feed
- 阿森纳相关记者（Charles Watts, James Benge, Chris Wheatley, David Ornstein）

## 注意事项

1. **资源消耗**：定时任务会持续运行，注意 CPU 和内存使用
2. **网络要求**：需要稳定的网络连接访问 RSS Feed 和翻译服务
3. **速率限制**：免费翻译服务可能有速率限制，脚本已添加延迟
4. **数据存储**：确保有足够的磁盘空间存储新闻数据

