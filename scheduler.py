#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
每半小时自动执行一次新闻抓取脚本
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_news_fetch(filter_arsenal=False):
    """
    执行新闻抓取脚本
    
    Args:
        filter_arsenal: 是否只抓取阿森纳相关新闻
    """
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行新闻抓取任务")
    if filter_arsenal:
        print("🔴 仅抓取阿森纳相关新闻")
    print(f"{'='*60}\n")
    
    try:
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, 'fetch_football_news.py')
        
        # 构建命令
        cmd = [sys.executable, script_path]
        
        # 如果设置了环境变量，传递给子进程
        env = os.environ.copy()
        
        # 执行脚本
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )
        
        if result.returncode == 0:
            print(f"\n✅ 新闻抓取完成 ({datetime.now().strftime('%H:%M:%S')})")
            # 复制文件到 public 目录（如果存在）
            output_file = os.path.join(script_dir, 'football_news_translated.json')
            public_file = os.path.join(script_dir, 'public', 'news.json')
            
            if os.path.exists(output_file):
                import shutil
                shutil.copy2(output_file, public_file)
                print(f"✅ 数据已更新到 public/news.json")
        else:
            print(f"\n❌ 新闻抓取失败 (退出码: {result.returncode})")
            if result.stderr:
                print(f"错误信息: {result.stderr[:500]}")
    
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  新闻抓取超时（超过10分钟）")
    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
    
    print(f"{'='*60}\n")


def main():
    """主函数"""
    print("="*60)
    print("📰 足球新闻定时抓取服务")
    print("="*60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("执行频率: 每30分钟")
    
    # 检查是否只抓取阿森纳新闻
    filter_arsenal = os.getenv('FILTER_ARSENAL', 'false').lower() == 'true'
    if filter_arsenal:
        print("🔴 模式: 仅抓取阿森纳相关新闻")
    else:
        print("📰 模式: 抓取所有足球新闻")
    
    print("="*60)
    print("\n等待执行... (按 Ctrl+C 停止)\n")
    
    # 立即执行一次
    run_news_fetch(filter_arsenal=filter_arsenal)
    
    # 设置定时任务：每30分钟执行一次
    schedule.every(30).minutes.do(run_news_fetch, filter_arsenal=filter_arsenal)
    
    # 保持运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n\n程序已停止")
        sys.exit(0)


if __name__ == '__main__':
    main()

