# Twitter/X 推文抓取设置指南

本脚本支持两种方式抓取知名足球记者的 Twitter/X 推文：

## 方式 1: 使用 snscrape（推荐，免费）

### 安装
```bash
pip install snscrape
```

### 使用方法
脚本会自动检测并使用 snscrape（如果已安装）。无需额外配置。

### 注意事项
- snscrape 是免费的开源库
- 由于 Twitter/X 政策变化，可能偶尔不稳定
- 如果 snscrape 失败，脚本会自动尝试 RapidAPI

---

## 方式 2: 使用 RapidAPI（备选方案）

如果 snscrape 不可用或失败，可以使用 RapidAPI 上的 Twitter API 服务。

### 步骤 1: 注册 RapidAPI 账号
1. 访问 [RapidAPI](https://rapidapi.com/)
2. 注册/登录账号
3. 在免费套餐下，大多数 Twitter API 都有一定的免费额度

### 步骤 2: 订阅 Twitter API 服务

推荐以下免费/低成本的 Twitter API 服务：

#### 选项 A: Twitter API 45
- 访问: https://rapidapi.com/omarmhaimdat/api/twitter-api45
- 免费套餐: 通常有每月免费请求额度
- 点击 "Subscribe to Test" 订阅

#### 选项 B: Twitter Scraper API
- 访问: https://rapidapi.com/rockapis-rockapis-default/api/twitter-scraper-api
- 免费套餐: 通常有每月免费请求额度
- 点击 "Subscribe to Test" 订阅

#### 选项 C: Twitter API v2
- 访问: https://rapidapi.com/twitter-api-v2/api/twitter-api-v2
- 可能需要付费，但功能更强大

### 步骤 3: 获取 API Key
1. 订阅服务后，在 RapidAPI 控制台找到你的 API Key
2. 设置环境变量：
```bash
export RAPIDAPI_KEY="your-rapidapi-key-here"
```

### 步骤 4: 启用 RapidAPI 模式
```bash
export USE_RAPIDAPI=true
```

### 步骤 5: 运行脚本
```bash
python fetch_football_news.py
```

---

## 配置记者列表

默认抓取以下记者：
- Fabrizio Romano (@FabrizioRomano)
- David Ornstein (@David_Ornstein)
- James Pearce (@JamesPearceLFC)
- Chris Wheatley (@ChrisWheatley_)
- Gianluca Di Marzio (@DiMarzio)

可以在 `fetch_football_news.py` 中修改 `JOURNALISTS` 字典来添加或修改记者。

---

## 测试 RapidAPI 连接

运行测试脚本：
```bash
python twitter_rapidapi_example.py
```

这会测试 RapidAPI 连接并显示获取的推文示例。

---

## 常见问题

### Q: snscrape 报错怎么办？
A: 设置 `USE_RAPIDAPI=true` 并使用 RapidAPI 作为替代方案。

### Q: RapidAPI 返回 401 错误？
A: 检查 API Key 是否正确设置，确保已订阅对应的 API 服务。

### Q: 如何知道哪个 API 可用？
A: 脚本会自动尝试多个 API。查看控制台输出可以看到哪个 API 成功。

### Q: 免费额度用完了怎么办？
A: 可以升级 RapidAPI 套餐，或者等待下个计费周期重置免费额度。

---

## 环境变量总结

```bash
# OpenAI API（用于翻译）
export OPENAI_API_KEY="your-openai-key"

# RapidAPI（可选，如果使用 RapidAPI）
export RAPIDAPI_KEY="your-rapidapi-key"
export USE_RAPIDAPI=true  # 强制使用 RapidAPI
```

