'use client'

import { useState, useEffect } from 'react'
import NewsCard from '@/components/NewsCard'
import Header from '@/components/Header'
import FilterBar from '@/components/FilterBar'

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

export default function Home() {
  const [news, setNews] = useState<NewsItem[]>([])
  const [filteredNews, setFilteredNews] = useState<NewsItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'transfer' | 'twitter' | 'rss'>('all')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    // 优先尝试 API 路由，如果失败则回退到静态文件
    fetch('/api/news')
      .then(res => {
        if (!res.ok) {
          // 如果 API 失败，尝试静态文件
          return fetch('/news.json')
        }
        return res
      })
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setNews(data)
          setFilteredNews(data)
        } else {
          console.error('Invalid data format:', data)
          setNews([])
          setFilteredNews([])
        }
        setLoading(false)
      })
      .catch(err => {
        console.error('加载新闻失败:', err)
        // 最后尝试静态文件
        fetch('/news.json')
          .then(res => res.json())
          .then(data => {
            setNews(data)
            setFilteredNews(data)
            setLoading(false)
          })
          .catch(() => {
            setLoading(false)
          })
      })
  }, [])

  useEffect(() => {
    let filtered = news

    // 按类型过滤
    if (filter === 'transfer') {
      filtered = filtered.filter(item => item.is_transfer === true)
    } else if (filter === 'twitter') {
      filtered = filtered.filter(item => item.source?.includes('Twitter'))
    } else if (filter === 'rss') {
      filtered = filtered.filter(item => !item.source?.includes('Twitter'))
    }

    // 按搜索关键词过滤
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(item => 
        item.title?.toLowerCase().includes(query) ||
        item.title_cn?.toLowerCase().includes(query) ||
        item.source?.toLowerCase().includes(query)
      )
    }

    setFilteredNews(filtered)
  }, [news, filter, searchQuery])

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-16 h-16 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-dark-border/30 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-transparent border-t-dark-accent rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl">⚽</span>
            </div>
          </div>
          <p className="text-dark-text-secondary font-medium">加载新闻中...</p>
          <p className="text-dark-text-muted text-sm mt-2">请稍候</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-6 pb-20">
        <FilterBar 
          filter={filter} 
          onFilterChange={setFilter}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
        />
        
        <div className="mt-6">
          {filteredNews.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-dark-surface/50 flex items-center justify-center border border-dark-border/30">
                <span className="text-4xl">📰</span>
              </div>
              <p className="text-dark-text-secondary text-lg font-semibold mb-2">暂无新闻</p>
              <p className="text-dark-text-muted text-sm">尝试调整搜索条件或过滤器</p>
            </div>
          ) : (
            <>
              <div className="mb-4 flex items-center justify-between">
                <p className="text-sm text-dark-text-secondary font-medium">
                  共找到 <span className="text-dark-accent font-bold">{filteredNews.length}</span> 条新闻
                </p>
              </div>
              <div className="space-y-3">
                {filteredNews.map((item, index) => (
                  <div
                    key={`${item.link}-${index}`}
                    className="animate-fade-in"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <NewsCard item={item} />
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  )
}

