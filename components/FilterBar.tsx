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
      <div className="relative">
        <input
          type="text"
          placeholder="搜索新闻..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full px-4 py-3 pl-10 bg-dark-card border border-dark-border rounded-lg text-dark-text-primary placeholder-dark-text-muted focus:outline-none focus:ring-2 focus:ring-dark-accent focus:border-transparent"
        />
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-muted">
          🔍
        </div>
      </div>

      {/* 过滤器按钮 */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {filters.map((f) => (
          <button
            key={f.id}
            onClick={() => onFilterChange(f.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
              filter === f.id
                ? 'bg-dark-accent text-white'
                : 'bg-dark-card text-dark-text-secondary hover:bg-dark-surface border border-dark-border'
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

