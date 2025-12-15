# Git 仓库设置指南

## 📦 已完成的步骤

1. ✅ 初始化 Git 仓库
2. ✅ 创建 `.gitignore` 文件
3. ✅ 添加所有项目文件
4. ✅ 创建初始提交

## 🚀 推送到远程仓库

### 方法 1: GitHub（推荐）

1. **在 GitHub 创建新仓库**
   - 访问 https://github.com/new
   - 输入仓库名称（如 `goalnews`）
   - 选择 Public 或 Private
   - **不要**初始化 README、.gitignore 或 license（我们已经有了）

2. **添加远程仓库并推送**
   ```bash
   git remote add origin https://github.com/your-username/goalnews.git
   git branch -M main
   git push -u origin main
   ```

### 方法 2: GitLab

1. **在 GitLab 创建新项目**
   - 访问 https://gitlab.com/projects/new
   - 输入项目名称
   - 选择可见性级别

2. **添加远程仓库并推送**
   ```bash
   git remote add origin https://gitlab.com/your-username/goalnews.git
   git branch -M main
   git push -u origin main
   ```

### 方法 3: 其他 Git 托管服务

```bash
# 添加远程仓库
git remote add origin <your-repo-url>

# 推送代码
git branch -M main
git push -u origin main
```

## 🔐 使用 SSH（可选）

如果使用 SSH 密钥：

```bash
# 使用 SSH URL
git remote set-url origin git@github.com:your-username/goalnews.git

# 推送
git push -u origin main
```

## 📝 后续更新

推送新更改：

```bash
git add .
git commit -m "描述你的更改"
git push
```

## 🏷️ 创建 Release

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 📋 检查状态

```bash
# 查看远程仓库
git remote -v

# 查看提交历史
git log --oneline

# 查看状态
git status
```

## ⚠️ 注意事项

1. **不要提交敏感信息**
   - API Keys
   - 环境变量文件（`.env`）
   - 已添加到 `.gitignore`

2. **大文件**
   - `football_news_translated.json` 和 `public/news.json` 已忽略
   - 这些是生成的数据文件，不需要版本控制

3. **Node 模块**
   - `node_modules/` 已忽略
   - 用户需要运行 `npm install` 安装依赖

