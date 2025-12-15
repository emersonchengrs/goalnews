# 部署和定时任务指南

## 🚀 部署方案

### 方案 1: Vercel + Cron Jobs（推荐）

Vercel 支持 Cron Jobs，可以定时执行 API 路由。

#### 设置步骤

1. **部署到 Vercel**
   ```bash
   # 安装 Vercel CLI
   npm i -g vercel
   
   # 部署
   vercel
   ```

2. **配置环境变量**
   在 Vercel 项目设置中添加：
   - `USE_FREE_TRANSLATOR=true`（使用免费翻译）
   - `CRON_SECRET=your-secret-key`（可选，用于保护 Cron 端点）

3. **Cron Job 自动配置**
   - `vercel.json` 已配置每30分钟执行一次
   - 路径：`/api/cron/fetch-news`
   - 自动读取并更新 `public/news.json`

#### 手动触发（测试）

```bash
curl https://your-domain.vercel.app/api/cron/fetch-news
```

---

### 方案 2: GitHub Actions（免费，推荐）

使用 GitHub Actions 定时运行脚本并自动提交更新。

#### 设置步骤

1. **启用 GitHub Actions**
   - 文件已创建：`.github/workflows/fetch-news.yml`
   - 自动每30分钟运行一次

2. **配置 Secrets（可选）**
   如果需要 OpenAI API：
   - Settings → Secrets → New secret
   - 添加 `OPENAI_API_KEY`

3. **首次运行**
   - 推送到 GitHub 后自动启用
   - 或手动触发：Actions → Fetch Football News → Run workflow

#### 工作流程

1. 每30分钟自动运行
2. 抓取新闻并翻译
3. 自动提交 `public/news.json` 到仓库
4. 触发 Vercel 重新部署（如果配置了）

---

### 方案 3: 外部 Cron 服务

使用外部服务（如 cron-job.org）定时调用 API。

#### 设置步骤

1. **部署到 Vercel/Netlify**
2. **在 cron-job.org 创建任务**
   - URL: `https://your-domain.vercel.app/api/cron/fetch-news`
   - 频率: 每30分钟
   - 方法: GET

---

## 📝 数据更新流程

### 当前流程

```
定时任务触发
  ↓
运行 fetch_football_news.py
  ↓
生成 football_news_translated.json
  ↓
复制到 public/news.json
  ↓
网站自动显示新数据
```

### GitHub Actions 流程

```
GitHub Actions 触发
  ↓
运行脚本
  ↓
提交 public/news.json 到仓库
  ↓
触发 Vercel 重新部署
  ↓
网站更新
```

---

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `USE_FREE_TRANSLATOR` | 使用免费翻译 | `false` |
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `FILTER_ARSENAL` | 只抓取阿森纳新闻 | `false` |
| `CRON_SECRET` | Cron 端点密钥 | - |

### Vercel Cron 配置

`vercel.json` 已配置：
```json
{
  "crons": [
    {
      "path": "/api/cron/fetch-news",
      "schedule": "*/30 * * * *"  // 每30分钟
    }
  ]
}
```

### GitHub Actions 配置

`.github/workflows/fetch-news.yml` 已配置：
- 每30分钟运行（UTC时间）
- 支持手动触发
- 自动提交更新

---

## 🧪 测试

### 本地测试 API 路由

```bash
# 启动开发服务器
npm run dev

# 在另一个终端测试
curl http://localhost:3000/api/cron/fetch-news
```

### 测试 GitHub Actions

1. 推送到 GitHub
2. 查看 Actions 标签页
3. 手动触发 "Fetch Football News" workflow

---

## ⚠️ 注意事项

1. **Python 环境**
   - Vercel 需要安装 Python 依赖
   - 可能需要使用 Serverless Functions
   - 考虑使用外部 API 服务

2. **GitHub Actions**
   - 免费账户有使用限制
   - 私有仓库有更多运行时间

3. **数据文件大小**
   - `public/news.json` 会被提交到 Git
   - 如果太大，考虑使用数据库

4. **API 速率限制**
   - 免费翻译服务有速率限制
   - 脚本已添加延迟

---

## 🔄 推荐方案

**最佳实践**：使用 **GitHub Actions**

- ✅ 完全免费
- ✅ 可靠稳定
- ✅ 自动提交更新
- ✅ 可以触发重新部署
- ✅ 有日志和通知

---

## 📚 相关文件

- `vercel.json` - Vercel Cron 配置
- `app/api/cron/fetch-news/route.ts` - Cron API 路由
- `.github/workflows/fetch-news.yml` - GitHub Actions 配置
- `fetch_football_news.py` - 新闻抓取脚本

