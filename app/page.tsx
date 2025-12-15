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
    fetch('/news.json')
      .then(res => res.json())
      .then(data => {
        setNews(data)
        setFilteredNews(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('加载新闻失败:', err)
        setLoading(false)
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
          <div className="w-12 h-12 border-4 border-dark-border border-t-dark-accent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-dark-text-secondary">加载中...</p>
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
            <div className="text-center py-12">
              <p className="text-dark-text-secondary text-lg">暂无新闻</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredNews.map((item, index) => (
                <NewsCard key={`${item.link}-${index}`} item={item} />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

