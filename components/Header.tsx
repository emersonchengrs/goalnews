export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-dark-surface/95 backdrop-blur-sm border-b border-dark-border">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-dark-text-primary">
              GoalNews
            </h1>
            <p className="text-sm text-dark-text-secondary mt-1">
              实时足球新闻聚合
            </p>
          </div>
          <div className="text-xs text-dark-text-muted">
            ⚽
          </div>
        </div>
      </div>
    </header>
  )
}

