# GoalNews 项目维护纪要

> 本文档用于项目维护和跨对话使用，记录项目的关键信息、架构、配置和更新历史。

**最后更新**: 2024-12-15  
**项目版本**: 1.0.0  
**维护状态**: ✅ 活跃

---

## 📋 项目概述

**GoalNews** 是一个全栈足球新闻聚合平台，包含：
- **前端**: Next.js 14 + TypeScript + Tailwind CSS（The Athletic 风格深色模式）
- **后端脚本**: Python 3.9+ 新闻抓取和翻译系统
- **数据源**: RSS Feeds + Twitter/X 推文
- **自动化**: 定时任务调度器（每30分钟）

---

## 🏗️ 技术架构

### 前端技术栈
- **框架**: Next.js 14.0.4 (App Router)
- **语言**: TypeScript 5.x
- **样式**: Tailwind CSS 3.3.0
- **运行时**: React 18.2.0

### 后端/脚本技术栈
- **语言**: Python 3.9+
- **核心库**:
  - `feedparser` 6.0.12 - RSS 解析
  - `deep-translator` 1.11.4 - 免费翻译（Google Translate）
  - `openai` 2.11.0 - OpenAI API（可选）
  - `schedule` 1.2.2 - 定时任务
  - `snscrape` 0.7.0.20230622 - Twitter 抓取（可选）
  - `requests` 2.32.5 - HTTP 请求

---

## 📁 项目结构

```
goalnews/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # 根布局（深色模式）
│   ├── page.tsx                 # 主页面（新闻列表）
│   └── globals.css              # 全局样式（The Athletic 风格）
├── components/                   # React 组件
│   ├── Header.tsx               # 页面头部
│   ├── FilterBar.tsx           # 搜索和过滤栏
│   └── NewsCard.tsx             # 新闻卡片组件
├── public/                      # 静态文件
│   └── news.json               # 新闻数据（自动生成，已忽略）
├── fetch_football_news.py       # 主抓取脚本
├── scheduler.py                 # 定时任务调度器
├── start_scheduler.sh           # 启动脚本
├── twitter_rapidapi_example.py # RapidAPI 示例
├── requirements.txt             # Python 依赖
├── package.json                 # Node.js 依赖
└── [配置文件]
```

---

## 🔧 核心功能

### 1. 新闻抓取 (`fetch_football_news.py`)

**RSS 源**:
- Sky Sports Football
- BBC Sport Football
- The Guardian Football
- BBC Arsenal
- Sky Sports Arsenal

**Twitter 记者**:
- Fabrizio Romano (@FabrizioRomano)
- David Ornstein (@David_Ornstein)
- Charles Watts (@charles_watts) - 阿森纳
- James Benge (@jamesbenge) - 阿森纳
- Chris Wheatley (@ChrisWheatley_) - 阿森纳
- James Pearce (@JamesPearceLFC)
- Gianluca Di Marzio (@DiMarzio)

**功能**:
- ✅ RSS Feed 解析
- ✅ Twitter 推文抓取（snscrape / RapidAPI）
- ✅ 自动翻译（Google Translate / OpenAI）
- ✅ 转会新闻识别和标记
- ✅ 阿森纳新闻过滤

### 2. 翻译系统

**支持方式**:
1. **免费翻译**（默认，推荐）
   - Google Translate（通过 deep-translator）
   - 无需 API Key
   - 自动识别转会新闻并添加 emoji

2. **OpenAI API**（可选）
   - 使用 gpt-4o-mini
   - 需要 API Key
   - 更智能的转会新闻语气调整

**配置**:
```bash
# 使用免费翻译
export USE_FREE_TRANSLATOR=true

# 使用 OpenAI
export OPENAI_API_KEY="your-key"
```

### 3. 定时任务 (`scheduler.py`)

**功能**:
- 每30分钟自动执行新闻抓取
- 自动更新 `public/news.json`
- 后台运行支持
- 详细日志记录

**启动方式**:
```bash
./start_scheduler.sh
# 或
python3 scheduler.py
```

### 4. 前端网站

**功能**:
- 新闻列表展示
- 实时搜索
- 多维度过滤（全部/转会/推文/RSS）
- 移动端响应式设计
- 深色模式（The Athletic 风格）

---

## ⚙️ 环境变量配置

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `USE_FREE_TRANSLATOR` | 使用免费翻译 | `false` | 否 |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - | 否 |
| `FILTER_ARSENAL` | 只抓取阿森纳新闻 | `false` | 否 |
| `TRANSLATOR_TYPE` | 翻译服务（google/deepl/libre） | `google` | 否 |
| `USE_RAPIDAPI` | 使用 RapidAPI | `false` | 否 |
| `RAPIDAPI_KEY` | RapidAPI 密钥 | - | 否 |

---

## 📝 数据格式

### 新闻数据 JSON 结构

```json
{
  "source": "Sky Sports",
  "title": "English Title",
  "title_cn": "中文标题",
  "link": "https://example.com/news",
  "published": "2024-01-01T12:00:00",
  "published_raw": "Mon, 01 Jan 2024 12:00:00 GMT",
  "is_transfer": false,
  "tweet_id": "1234567890",
  "retweet_count": 10,
  "like_count": 50
}
```

### 字段说明

- `source`: 新闻来源（RSS 源名称或 "Twitter - @username"）
- `title`: 原始英文标题
- `title_cn`: 翻译后的中文标题
- `link`: 新闻链接
- `published`: ISO 格式发布时间
- `published_raw`: 原始发布时间字符串
- `is_transfer`: 是否为转会新闻（布尔值）
- `tweet_id`: Twitter 推文 ID（仅推文）
- `retweet_count`: 转发数（仅推文）
- `like_count`: 点赞数（仅推文）

---

## 🔑 关键文件说明

### Python 脚本

1. **`fetch_football_news.py`** - 主抓取脚本
   - 入口函数: `main(filter_arsenal=False)`
   - 输出文件: `football_news_translated.json`
   - 自动复制到: `public/news.json`

2. **`scheduler.py`** - 定时任务调度器
   - 执行频率: 每30分钟
   - 支持后台运行
   - 日志输出

3. **`twitter_rapidapi_example.py`** - RapidAPI 示例
   - 参考实现
   - 支持多个 API 端点

### 前端文件

1. **`app/page.tsx`** - 主页面
   - 加载 `public/news.json`
   - 搜索和过滤逻辑
   - 状态管理

2. **`components/NewsCard.tsx`** - 新闻卡片
   - 显示新闻信息
   - 转会新闻标记
   - 时间格式化

### 配置文件

1. **`tailwind.config.ts`** - Tailwind 配置
   - 深色模式主题
   - The Athletic 风格颜色

2. **`next.config.js`** - Next.js 配置
   - 基础配置

---

## 🚀 常用命令

### 开发

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 安装 Node.js 依赖
npm install

# 运行新闻抓取（使用免费翻译）
export USE_FREE_TRANSLATOR=true
python3 fetch_football_news.py

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
npm start
```

### 定时任务

```bash
# 启动定时任务
./start_scheduler.sh

# 后台运行
nohup python3 scheduler.py > scheduler.log 2>&1 &

# 查看日志
tail -f scheduler.log
```

### Git 操作

```bash
# 查看状态
git status

# 提交更改
git add .
git commit -m "描述"
git push
```

---

## 🐛 已知问题和限制

### 当前限制

1. **Twitter 抓取**
   - snscrape 可能不稳定（Twitter API 变化）
   - 建议使用 RapidAPI 作为备选

2. **翻译服务**
   - Google Translate 有速率限制
   - 脚本已添加延迟（0.3秒/条）

3. **数据文件**
   - `football_news_translated.json` 和 `public/news.json` 已忽略
   - 需要手动运行脚本生成

### 待优化项

- [ ] 添加数据库支持（替代 JSON 文件）
- [ ] 实现增量更新（避免重复翻译）
- [ ] 添加更多新闻源
- [ ] 优化移动端体验
- [ ] 添加新闻详情页
- [ ] 实现用户收藏功能

---

## 📊 更新历史

### v1.0.0 (2024-12-15)

**初始版本**

- ✅ Next.js 14 前端（The Athletic 风格）
- ✅ Python 新闻抓取脚本
- ✅ RSS Feed 支持（Sky Sports, BBC, Guardian）
- ✅ Twitter 推文抓取（snscrape / RapidAPI）
- ✅ 自动翻译功能（免费 + OpenAI）
- ✅ 定时任务调度器（每30分钟）
- ✅ 阿森纳新闻过滤
- ✅ 转会新闻识别和标记
- ✅ 搜索和过滤功能
- ✅ 移动端响应式设计

---

## 🔄 维护检查清单

### 定期检查（每周）

- [ ] 检查 RSS Feed 是否正常
- [ ] 验证翻译功能是否正常
- [ ] 检查定时任务是否运行
- [ ] 查看错误日志
- [ ] 更新依赖版本

### 每月检查

- [ ] 更新 Python 依赖
- [ ] 更新 Node.js 依赖
- [ ] 检查 API 服务状态
- [ ] 优化性能
- [ ] 备份数据

---

## 📚 相关文档

- `README.md` - 项目主文档
- `QUICK_START.md` - 快速开始指南
- `SCHEDULER_GUIDE.md` - 定时任务指南
- `TRANSLATION_GUIDE.md` - 翻译功能指南
- `TWITTER_SETUP.md` - Twitter 设置指南
- `GIT_SETUP.md` - Git 仓库设置指南

---

## 🔐 安全注意事项

### 已忽略的文件

- `.env` - 环境变量（包含 API Keys）
- `*.log` - 日志文件
- `node_modules/` - Node.js 依赖
- `football_news_translated.json` - 生成的数据
- `public/news.json` - 生成的数据

### 安全建议

1. **不要提交敏感信息**
   - API Keys
   - 环境变量文件
   - 个人配置

2. **使用环境变量**
   - 所有 API Keys 通过环境变量传递
   - 不要硬编码在代码中

3. **定期更新依赖**
   - 修复安全漏洞
   - 保持最新版本

---

## 🆘 故障排查

### 常见问题

1. **翻译不工作**
   - 检查 `USE_FREE_TRANSLATOR=true`
   - 检查网络连接
   - 查看错误日志

2. **定时任务不运行**
   - 检查进程是否运行
   - 查看日志文件
   - 验证 Python 环境

3. **网站不显示数据**
   - 检查 `public/news.json` 是否存在
   - 验证 JSON 格式
   - 查看浏览器控制台

4. **Twitter 抓取失败**
   - 尝试使用 RapidAPI
   - 检查 API Key
   - 查看错误信息

---

## 📞 联系和维护

**项目维护者**: [待填写]  
**GitHub 仓库**: [待填写]  
**问题反馈**: GitHub Issues

---

## 📝 更新日志模板

```markdown
### v1.x.x (YYYY-MM-DD)

**新增功能**
- 

**修复**
- 

**优化**
- 

**已知问题**
- 
```

---

**最后更新**: 2024-12-15  
**维护者**: [待填写]  
**状态**: ✅ 活跃维护中

