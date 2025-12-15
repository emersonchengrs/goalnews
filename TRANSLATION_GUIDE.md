# 免费翻译使用指南

脚本现在支持多种免费翻译方案，无需 OpenAI API Key！

## 支持的免费翻译服务

### 1. Google Translate（推荐，默认）
- ✅ 完全免费
- ✅ 无需 API Key
- ✅ 翻译质量好
- ⚠️ 可能有速率限制

### 2. DeepL（可选）
- ✅ 翻译质量极高
- ⚠️ 免费版本有使用限制
- ⚠️ 可能需要配置

### 3. LibreTranslate（可选）
- ✅ 开源免费
- ✅ 可自托管
- ⚠️ 翻译质量中等

## 使用方法

### 方法 1: 自动使用免费翻译（推荐）

如果没有设置 `OPENAI_API_KEY`，脚本会自动使用 Google Translate：

```bash
python3 fetch_football_news.py
```

### 方法 2: 强制使用免费翻译

即使有 OpenAI API Key，也可以强制使用免费翻译：

```bash
export USE_FREE_TRANSLATOR=true
python3 fetch_football_news.py
```

### 方法 3: 选择不同的翻译服务

```bash
# 使用 Google Translate（默认）
export TRANSLATOR_TYPE=google
python3 fetch_football_news.py

# 使用 DeepL
export TRANSLATOR_TYPE=deepl
python3 fetch_football_news.py

# 使用 LibreTranslate
export TRANSLATOR_TYPE=libre
python3 fetch_football_news.py
```

## 安装依赖

```bash
pip3 install deep-translator
```

或使用 requirements.txt：

```bash
pip3 install -r requirements.txt
```

## 功能特点

- ✅ **自动识别转会新闻**：转会新闻会自动添加激动人心的 emoji（🚨、💥、✅）
- ✅ **智能回退**：如果某个翻译服务失败，可以尝试其他服务
- ✅ **速率限制处理**：自动添加延迟避免触发限制
- ✅ **完全免费**：无需任何 API Key

## 翻译质量对比

| 服务 | 质量 | 速度 | 免费额度 | 推荐度 |
|------|------|------|----------|--------|
| Google Translate | ⭐⭐⭐⭐ | 快 | 无限制 | ⭐⭐⭐⭐⭐ |
| DeepL | ⭐⭐⭐⭐⭐ | 快 | 有限制 | ⭐⭐⭐⭐ |
| LibreTranslate | ⭐⭐⭐ | 中等 | 无限制 | ⭐⭐⭐ |

## 注意事项

1. **速率限制**：免费服务可能有速率限制，脚本已自动添加延迟
2. **网络要求**：需要能够访问 Google/DeepL 等服务
3. **翻译准确性**：免费翻译可能不如 OpenAI，但对于新闻标题通常足够

## 示例输出

使用免费翻译后，新闻标题会显示为：

```json
{
  "title": "Manchester United sign new striker",
  "title_cn": "🚨 曼联签下新前锋",
  "is_transfer": true
}
```

转会新闻会自动添加 emoji 标记，让重要新闻更醒目！

