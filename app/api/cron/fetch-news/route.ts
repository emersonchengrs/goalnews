import { NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs'
import path from 'path'

const execAsync = promisify(exec)

export async function GET(request: Request) {
  // 验证 Cron Secret（Vercel 会自动添加）
  const authHeader = request.headers.get('authorization')
  const cronSecret = process.env.CRON_SECRET
  
  if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    // 运行 Python 脚本
    const scriptPath = path.join(process.cwd(), 'fetch_football_news.py')
    const publicPath = path.join(process.cwd(), 'public', 'news.json')
    
    // 检查脚本是否存在
    if (!fs.existsSync(scriptPath)) {
      return NextResponse.json({ 
        error: 'Script not found',
        message: 'fetch_football_news.py not found in project root'
      }, { status: 404 })
    }

    // 执行 Python 脚本
    const { stdout, stderr } = await execAsync(
      `python3 ${scriptPath}`,
      {
        cwd: process.cwd(),
        env: {
          ...process.env,
          USE_FREE_TRANSLATOR: 'true',
        },
        timeout: 300000 // 5分钟超时
      }
    )

    // 检查输出文件是否存在
    const outputFile = path.join(process.cwd(), 'football_news_translated.json')
    if (fs.existsSync(outputFile)) {
      // 复制到 public 目录
      const data = fs.readFileSync(outputFile, 'utf8')
      fs.writeFileSync(publicPath, data, 'utf8')
      
      const newsData = JSON.parse(data)
      
      return NextResponse.json({
        success: true,
        message: 'News fetched successfully',
        count: newsData.length,
        stdout: stdout.substring(0, 500), // 限制输出长度
      })
    } else {
      return NextResponse.json({
        success: false,
        message: 'Script ran but no output file found',
        stdout: stdout.substring(0, 500),
        stderr: stderr.substring(0, 500),
      }, { status: 500 })
    }
  } catch (error: any) {
    console.error('Cron job error:', error)
    return NextResponse.json({
      success: false,
      error: error.message,
      stderr: error.stderr?.substring(0, 500),
    }, { status: 500 })
  }
}

