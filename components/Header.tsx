export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-dark-surface/95 backdrop-blur-md border-b border-dark-border/50 shadow-lg shadow-black/20">
      <div className="max-w-4xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-dark-accent to-orange-600 flex items-center justify-center shadow-lg shadow-dark-accent/20">
              <span className="text-xl">⚽</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-dark-text-primary tracking-tight">
                GoalNews
              </h1>
              <p className="text-xs text-dark-text-secondary mt-0.5 font-medium">
                实时足球新闻聚合
              </p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-dark-card border border-dark-border/50">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-xs text-dark-text-secondary font-medium">实时更新</span>
          </div>
        </div>
      </div>
    </header>
  )
}

