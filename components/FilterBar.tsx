'use client'

interface FilterBarProps {
  filter: 'all' | 'transfer' | 'twitter' | 'rss'
  onFilterChange: (filter: 'all' | 'transfer' | 'twitter' | 'rss') => void
  searchQuery: string
  onSearchChange: (query: string) => void
}

export default function FilterBar({ filter, onFilterChange, searchQuery, onSearchChange }: FilterBarProps) {
  const filters = [
    { id: 'all' as const, label: '全部', icon: '📰' },
    { id: 'transfer' as const, label: '转会', icon: '🚨' },
    { id: 'twitter' as const, label: '推文', icon: '🐦' },
    { id: 'rss' as const, label: 'RSS', icon: '📡' },
  ]

  return (
    <div className="space-y-4">
      {/* 搜索框 */}
      <div className="relative group">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-dark-text-muted group-focus-within:text-dark-accent transition-colors">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          type="text"
          placeholder="搜索新闻标题、来源..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full px-4 py-3.5 pl-12 bg-dark-card/50 border border-dark-border/50 rounded-xl text-dark-text-primary placeholder-dark-text-muted focus:outline-none focus:ring-2 focus:ring-dark-accent/50 focus:border-dark-accent/50 transition-all backdrop-blur-sm"
        />
        {searchQuery && (
          <button
            onClick={() => onSearchChange('')}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-dark-text-muted hover:text-dark-text-primary transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* 过滤器按钮 */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {filters.map((f) => (
          <button
            key={f.id}
            onClick={() => onFilterChange(f.id)}
            className={`px-4 py-2.5 rounded-xl text-sm font-semibold whitespace-nowrap transition-all duration-200 ${
              filter === f.id
                ? 'bg-gradient-to-r from-dark-accent to-orange-600 text-white shadow-lg shadow-dark-accent/30 scale-105'
                : 'bg-dark-card/50 text-dark-text-secondary hover:bg-dark-surface/50 border border-dark-border/50 hover:border-dark-border backdrop-blur-sm'
            }`}
          >
            <span className="mr-1.5">{f.icon}</span>
            {f.label}
          </button>
        ))}
      </div>
    </div>
  )
}

