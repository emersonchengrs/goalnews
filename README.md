# GoalNews - 足球新闻聚合网站

一个现代化的足球新闻聚合网站，自动抓取、翻译并展示来自 Sky Sports、BBC Sport、The Guardian 和知名记者的最新足球新闻。

## ✨ 特性

- 🎨 **The Athletic 风格设计** - 深色模式，现代化 UI
- 📱 **完全响应式** - 移动端友好
- 🚨 **转会新闻高亮** - 自动识别并标记转会新闻
- 🔍 **实时搜索和过滤** - 支持按类型、关键词筛选
- 🐦 **Twitter/X 集成** - 抓取知名记者推文
- 🌐 **自动翻译** - 支持免费翻译（Google Translate）和 OpenAI API
- ⏰ **定时任务** - 每30分钟自动更新新闻
- 🔴 **阿森纳模式** - 可选的阿森纳新闻过滤

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd goalnews
```

### 2. 安装依赖

#### Python 依赖（新闻抓取）

```bash
pip3 install -r requirements.txt
```

#### Node.js 依赖（网站）

```bash
npm install
```

### 3. 运行新闻抓取脚本

```bash
# 使用免费翻译（推荐）
export USE_FREE_TRANSLATOR=true
python3 fetch_football_news.py

# 或使用 OpenAI API
export OPENAI_API_KEY="your-api-key"
python3 fetch_football_news.py
```

### 4. 启动网站

```bash
npm run dev
```

打开 [http://localhost:3000](http://localhost:3000) 查看网站。

## 📋 项目结构

```
goalnews/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   └── globals.css        # 全局样式
├── components/            # React 组件
│   ├── Header.tsx         # 页面头部
│   ├── FilterBar.tsx     # 过滤和搜索栏
│   └── NewsCard.tsx      # 新闻卡片
├── public/                # 静态文件
│   └── news.json         # 新闻数据（自动生成）
├── fetch_football_news.py # 新闻抓取脚本
├── scheduler.py           # 定时任务调度器
├── start_scheduler.sh     # 启动脚本
└── requirements.txt      # Python 依赖
```

## 🔧 功能详解

### 新闻抓取

脚本会自动抓取以下来源的新闻：

- **RSS Feeds**:
  - Sky Sports Football
  - BBC Sport Football
  - The Guardian Football
  - BBC Arsenal（阿森纳）
  - Sky Sports Arsenal（阿森纳）

- **Twitter/X 记者**:
  - Fabrizio Romano
  - David Ornstein
  - Charles Watts（阿森纳）
  - James Benge（阿森纳）
  - 更多...

### 翻译功能

支持两种翻译方式：

1. **免费翻译**（Google Translate，推荐）
   ```bash
   export USE_FREE_TRANSLATOR=true
   python3 fetch_football_news.py
   ```

2. **OpenAI API**（需要 API Key）
   ```bash
   export OPENAI_API_KEY="your-key"
   python3 fetch_football_news.py
   ```

### 定时任务

每30分钟自动抓取并更新新闻：

```bash
# 启动定时任务
./start_scheduler.sh

# 或直接运行
python3 scheduler.py

# 后台运行
nohup python3 scheduler.py > scheduler.log 2>&1 &
```

### 阿森纳模式

只抓取阿森纳相关新闻：

```bash
export FILTER_ARSENAL=true
python3 fetch_football_news.py
```

## 📖 使用指南

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `USE_FREE_TRANSLATOR` | 使用免费翻译 | `false` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `FILTER_ARSENAL` | 只抓取阿森纳新闻 | `false` |
| `TRANSLATOR_TYPE` | 翻译服务类型 | `google` |
| `USE_RAPIDAPI` | 使用 RapidAPI | `false` |
| `RAPIDAPI_KEY` | RapidAPI 密钥 | - |

### 命令行参数

```bash
# 只抓取阿森纳新闻
python3 fetch_football_news.py --arsenal
```

## 🛠️ 技术栈

### 前端
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **React Hooks** - 状态管理

### 后端/脚本
- **Python 3** - 脚本语言
- **feedparser** - RSS 解析
- **deep-translator** - 免费翻译
- **openai** - OpenAI API
- **schedule** - 定时任务
- **snscrape** - Twitter 抓取（可选）

## 📝 数据格式

新闻数据格式：

```json
{
  "source": "Sky Sports",
  "title": "English Title",
  "title_cn": "中文标题",
  "link": "https://example.com/news",
  "published": "2024-01-01T12:00:00",
  "is_transfer": false,
  "tweet_id": "1234567890",
  "retweet_count": 10,
  "like_count": 50
}
```

## 📚 文档

- [快速开始指南](QUICK_START.md)
- [定时任务指南](SCHEDULER_GUIDE.md)
- [翻译功能指南](TRANSLATION_GUIDE.md)
- [Twitter 设置指南](TWITTER_SETUP.md)

## 🚢 部署

### Vercel（推荐）

1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 设置环境变量（如需要）
4. 部署完成

### 其他平台

项目可以部署到任何支持 Next.js 的平台：
- Netlify
- Railway
- 自托管服务器

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 新闻来源：Sky Sports, BBC Sport, The Guardian
- 记者：Fabrizio Romano, David Ornstein 等
- 翻译服务：Google Translate, OpenAI

---

Made with ❤️ for football fans
