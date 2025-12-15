#!/bin/bash
# 启动定时任务调度器

echo "🚀 启动足球新闻定时抓取服务..."
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

# 进入脚本目录
cd "$(dirname "$0")"

# 检查是否安装依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境（如果存在）
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# 安装依赖
echo "📦 检查并安装依赖..."
pip3 install -q -r requirements.txt

# 设置环境变量（可选）
# export USE_FREE_TRANSLATOR=true
# export FILTER_ARSENAL=true  # 如果只想抓取阿森纳新闻

# 启动调度器
echo "✅ 启动定时任务调度器..."
echo "   执行频率: 每30分钟"
echo "   按 Ctrl+C 停止"
echo ""

python3 scheduler.py

