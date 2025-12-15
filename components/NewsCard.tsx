'use client'

interface NewsItem {
  source: string
  title: string
  title_cn?: string
  link: string
  published: string
  is_transfer?: boolean
  tweet_id?: string
  retweet_count?: number
  like_count?: number
}

interface NewsCardProps {
  item: NewsItem
}

export default function NewsCard({ item }: NewsCardProps) {
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now.getTime() - date.getTime()
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      if (days < 7) return `${days}天前`
      
      return date.toLocaleDateString('zh-CN', { 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return dateString
    }
  }

  const getSourceIcon = (source: string) => {
    if (source.includes('Twitter')) return '🐦'
    if (source.includes('Sky Sports')) return '☁️'
    if (source.includes('BBC')) return '📻'
    if (source.includes('Guardian')) return '🛡️'
    return '📰'
  }

  const isTwitter = item.source?.includes('Twitter')
  const displayTitle = item.title_cn || item.title

  return (
    <a
      href={item.link}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-dark-card border border-dark-border rounded-lg p-4 hover:bg-dark-surface transition-all hover:border-dark-accent/50 group"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          {/* 来源和时间 */}
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className="text-xs font-medium text-dark-text-secondary flex items-center gap-1">
              <span>{getSourceIcon(item.source)}</span>
              <span className="truncate">{item.source}</span>
            </span>
            {item.is_transfer && (
              <span className="px-2 py-0.5 bg-dark-accent/20 text-dark-accent text-xs font-semibold rounded">
                🚨 转会
              </span>
            )}
            <span className="text-xs text-dark-text-muted">
              {formatDate(item.published)}
            </span>
          </div>

          {/* 标题 */}
          <h2 className="text-base font-semibold text-dark-text-primary leading-snug group-hover:text-dark-accent transition-colors">
            {displayTitle}
          </h2>

          {/* 原始英文标题（如果有中文翻译） */}
          {item.title_cn && item.title !== item.title_cn && (
            <p className="text-sm text-dark-text-secondary mt-2">
              {item.title}
            </p>
          )}

          {/* Twitter 互动数据 */}
          {isTwitter && (item.retweet_count || item.like_count) && (
            <div className="flex items-center gap-4 mt-3 text-xs text-dark-text-muted">
              {item.retweet_count > 0 && (
                <span className="flex items-center gap-1">
                  <span>🔄</span>
                  <span>{item.retweet_count}</span>
                </span>
              )}
              {item.like_count > 0 && (
                <span className="flex items-center gap-1">
                  <span>❤️</span>
                  <span>{item.like_count}</span>
                </span>
              )}
            </div>
          )}
        </div>

        {/* 外部链接图标 */}
        <div className="flex-shrink-0 text-dark-text-muted group-hover:text-dark-accent transition-colors">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </div>
      </div>
    </a>
  )
}

