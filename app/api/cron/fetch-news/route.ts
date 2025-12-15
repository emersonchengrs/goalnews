import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  // 验证 Cron Secret（Vercel 会自动添加）
  const authHeader = request.headers.get('authorization')
  const cronSecret = process.env.CRON_SECRET
  
  if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // 注意：Vercel Serverless Functions 无法直接运行 Python 脚本
  // 建议使用 GitHub Actions 来定时运行脚本
  // 这个端点可以用于触发外部服务或作为 webhook
  
  return NextResponse.json({
    message: 'This endpoint is for Vercel Cron Jobs',
    note: 'For Python script execution, please use GitHub Actions',
    github_actions: 'https://github.com/emersonchengrs/goalnews/actions',
    manual_trigger: 'You can manually trigger the workflow in GitHub Actions',
  })
}

