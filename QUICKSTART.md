# 🎯 快速开始指南

## 步骤一：创建 GitHub 仓库

1. 登录你的 GitHub 账号
2. 点击右上角的 "+" 号，选择 "New repository"
3. 仓库名称填写: `tech-news-daily`（或其他你喜欢的名字）
4. 选择 "Public"
5. 不要勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

## 步骤二：上传项目文件

### 方式 1: 使用 Git 命令行（推荐）

```bash
# 1. 进入项目目录
cd tech-news-daily

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: Tech News Daily Aggregator"

# 5. 添加远程仓库（替换 yourusername 为你的 GitHub 用户名）
git remote add origin https://github.com/yourusername/tech-news-daily.git

# 6. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 方式 2: 使用 GitHub Desktop

1. 打开 GitHub Desktop
2. File -> Add Local Repository
3. 选择 tech-news-daily 文件夹
4. 点击 "Publish repository"

### 方式 3: 直接上传文件

1. 在 GitHub 仓库页面点击 "uploading an existing file"
2. 将所有文件拖拽到页面
3. 点击 "Commit changes"

## 步骤三：启用 GitHub Actions

1. 进入你的仓库
2. 点击 "Actions" 标签
3. 点击绿色按钮 "I understand my workflows, go ahead and enable them"

## 步骤四：配置 GitHub Pages

1. 点击仓库的 "Settings"（设置）
2. 左侧菜单找到 "Pages"
3. 在 "Source" 部分:
   - Branch: 选择 `main`
   - Folder: 选择 `/docs`
4. 点击 "Save"
5. 等待 1-2 分钟，页面顶部会显示你的网站地址

## 步骤五：手动触发第一次数据抓取

1. 点击 "Actions" 标签
2. 左侧选择 "Daily Tech News Crawler"
3. 右侧点击 "Run workflow" 下拉菜单
4. 点击绿色的 "Run workflow" 按钮
5. 等待 3-5 分钟，workflow 完成

## 步骤六：访问你的网站

访问: `https://yourusername.github.io/tech-news-daily/`

（记得替换 `yourusername` 为你的 GitHub 用户名）

## 🎉 大功告成！

现在你的科技资讯聚合网站已经上线了！

- ⏰ 每天 UTC 0:00（北京时间 8:00）自动更新
- 📊 自动抓取 GitHub Trending
- 📰 自动抓取 Hacker News
- 📡 自动抓取科技媒体 RSS

## 后续优化

### 1. 修改仓库名中的用户名

在以下文件中将 `yourusername` 替换为你的实际 GitHub 用户名：

- `README.md`
- `docs/index.html`（页脚部分）

### 2. 自定义抓取时间

编辑 `.github/workflows/daily-crawl.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # 修改这里
```

Cron 表达式说明：
- `0 0 * * *` - 每天 00:00 UTC（北京时间 8:00）
- `0 12 * * *` - 每天 12:00 UTC（北京时间 20:00）
- `0 */6 * * *` - 每 6 小时一次

### 3. 添加更多数据源

在 `src/crawlers/rss_feeds.py` 中添加你喜欢的 RSS 订阅源。

## 常见问题排查

### ❌ Actions 运行失败

1. 检查 Actions 日志，查看具体错误
2. 确认 Python 依赖都已正确安装
3. 检查网络连接是否正常

### ❌ 页面显示 404

1. 确认 GitHub Pages 已启用
2. 检查 Branch 选择的是 `main`，Folder 选择的是 `/docs`
3. 等待几分钟让 GitHub Pages 部署完成

### ❌ 数据不更新

1. 检查 Actions 是否成功运行
2. 查看最后一次 commit 是否包含数据文件
3. 确认 workflow 权限设置正确（Settings -> Actions -> General -> Workflow permissions -> Read and write permissions）

## 需要帮助？

创建一个 [Issue](https://github.com/yourusername/tech-news-daily/issues) 告诉我！
