import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // 尝试读取 news.json 文件
    const filePath = path.join(process.cwd(), 'public', 'news.json')
    
    if (fs.existsSync(filePath)) {
      const fileContents = fs.readFileSync(filePath, 'utf8')
      const newsData = JSON.parse(fileContents)
      return NextResponse.json(newsData)
    }
    
    // 如果文件不存在，返回示例数据
    return NextResponse.json([
      {
        source: "GoalNews",
        title: "Welcome to GoalNews",
        title_cn: "欢迎使用 GoalNews",
        link: "https://github.com/emersonchengrs/goalnews",
        published: new Date().toISOString(),
        is_transfer: false
      },
      {
        source: "GoalNews",
        title: "News data will be updated automatically",
        title_cn: "新闻数据将自动更新",
        link: "https://github.com/emersonchengrs/goalnews",
        published: new Date().toISOString(),
        is_transfer: false
      }
    ])
  } catch (error) {
    console.error('Error loading news:', error)
    return NextResponse.json(
      { error: 'Failed to load news' },
      { status: 500 }
    )
  }
}

