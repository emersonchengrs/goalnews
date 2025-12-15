import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GoalNews - 足球新闻聚合',
  description: '实时足球新闻，来自 Sky Sports、BBC Sport、The Guardian 和知名记者',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className="dark">
      <body className="antialiased">{children}</body>
    </html>
  )
}

