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
  
  // 安全获取数值，避免 undefined
  const retweetCount = item.retweet_count ?? 0
  const likeCount = item.like_count ?? 0

  return (
    <a
      href={item.link}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-dark-card/50 backdrop-blur-sm border border-dark-border/50 rounded-xl p-5 hover:bg-dark-surface/50 hover:border-dark-accent/30 transition-all duration-300 group shadow-sm hover:shadow-xl hover:shadow-black/20"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* 来源和时间 */}
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-dark-surface/50 rounded-lg text-xs font-semibold text-dark-text-secondary border border-dark-border/30">
              <span className="text-sm">{getSourceIcon(item.source)}</span>
              <span className="truncate max-w-[120px]">{item.source}</span>
            </span>
            {item.is_transfer && (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-gradient-to-r from-dark-accent/20 to-orange-600/20 text-dark-accent text-xs font-bold rounded-lg border border-dark-accent/30">
                <span>🚨</span>
                <span>转会</span>
              </span>
            )}
            <span className="text-xs text-dark-text-muted font-medium px-2 py-1 bg-dark-surface/30 rounded-lg">
              {formatDate(item.published)}
            </span>
          </div>

          {/* 标题 */}
          <h2 className="text-lg font-bold text-dark-text-primary leading-tight group-hover:text-dark-accent transition-colors duration-200 mb-2">
            {displayTitle}
          </h2>

          {/* 原始英文标题（如果有中文翻译） */}
          {item.title_cn && item.title !== item.title_cn && (
            <p className="text-sm text-dark-text-secondary/80 mt-2.5 leading-relaxed line-clamp-2">
              {item.title}
            </p>
          )}

          {/* Twitter 互动数据 */}
          {isTwitter && (retweetCount > 0 || likeCount > 0) && (
            <div className="flex items-center gap-4 mt-4 pt-3 border-t border-dark-border/30">
              {retweetCount > 0 && (
                <span className="inline-flex items-center gap-1.5 text-xs text-dark-text-muted font-medium">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                  </svg>
                  <span>{retweetCount}</span>
                </span>
              )}
              {likeCount > 0 && (
                <span className="inline-flex items-center gap-1.5 text-xs text-dark-text-muted font-medium">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                  </svg>
                  <span>{likeCount}</span>
                </span>
              )}
            </div>
          )}
        </div>

        {/* 外部链接图标 */}
        <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-dark-surface/50 border border-dark-border/30 flex items-center justify-center text-dark-text-muted group-hover:text-dark-accent group-hover:bg-dark-accent/10 group-hover:border-dark-accent/30 transition-all duration-200">
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

