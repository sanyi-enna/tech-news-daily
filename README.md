# 🚀 每日科技资讯聚合器

[![Daily Update](https://github.com/yourusername/tech-news-daily/actions/workflows/daily-crawl.yml/badge.svg)](https://github.com/yourusername/tech-news-daily/actions)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-success)](https://yourusername.github.io/tech-news-daily/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

每日自动聚合全球科技资讯，包括 GitHub Trending、Hacker News 和主流科技媒体 RSS。

🌐 **在线访问**: [https://yourusername.github.io/tech-news-daily/](https://yourusername.github.io/tech-news-daily/)

## ✨ 特性

- 📊 **GitHub Trending** - 每日热门开源项目（Python/JavaScript/Go/Rust/Java/TypeScript）
- 📰 **Hacker News** - 技术社区热门讨论
- 📡 **RSS Feeds** - TechCrunch、The Verge、36氪、少数派等科技媒体
- 🤖 **自动更新** - GitHub Actions 每日定时抓取
- 📱 **响应式设计** - 支持桌面和移动设备
- 🆓 **完全免费** - 基于 GitHub Pages 托管

## 🏗️ 项目结构

```
tech-news-daily/
├── .github/
│   └── workflows/
│       └── daily-crawl.yml      # GitHub Actions 配置
├── src/
│   ├── crawlers/
│   │   ├── github_trending.py   # GitHub Trending 爬虫
│   │   ├── hackernews.py        # Hacker News 爬虫
│   │   └── rss_feeds.py         # RSS 订阅源爬虫
│   └── main.py                  # 主程序
├── data/
│   ├── archive/                 # 历史数据归档
│   ├── github_trending.json     # GitHub 数据
│   ├── hackernews.json          # Hacker News 数据
│   ├── rss_feeds.json           # RSS 数据
│   └── latest.json              # 最新聚合数据
├── docs/                        # GitHub Pages 根目录
│   ├── data/
│   │   └── latest.json          # 前端数据文件
│   ├── css/
│   │   └── style.css            # 样式文件
│   ├── js/
│   │   └── app.js               # 前端逻辑
│   └── index.html               # 主页
├── requirements.txt             # Python 依赖
└── README.md                    # 项目说明
```

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮，将项目 fork 到你的 GitHub 账户。

### 2. 启用 GitHub Actions

1. 进入你 fork 的仓库
2. 点击 "Actions" 标签
3. 点击 "I understand my workflows, go ahead and enable them"

### 3. 配置 GitHub Pages

1. 进入仓库的 "Settings"
2. 点击左侧的 "Pages"
3. 在 "Source" 下选择:
   - Branch: `main`
   - Folder: `/docs`
4. 点击 "Save"
5. 等待几分钟，你的网站就会发布到：`https://yourusername.github.io/tech-news-daily/`

### 4. 手动触发第一次抓取

1. 进入 "Actions" 标签
2. 点击左侧的 "Daily Tech News Crawler"
3. 点击 "Run workflow" 按钮
4. 点击绿色的 "Run workflow" 确认

等待几分钟，数据抓取完成后，访问你的 GitHub Pages 网址即可查看！

## 🔧 本地开发

### 环境要求

- Python 3.9+
- pip

### 安装依赖

```bash
git clone https://github.com/yourusername/tech-news-daily.git
cd tech-news-daily
pip install -r requirements.txt
```

### 运行爬虫

```bash
python src/main.py
```

### 本地预览

```bash
cd docs
python -m http.server 8000
```

访问 `http://localhost:8000` 查看页面。

## ⚙️ 配置说明

### 修改抓取时间

编辑 `.github/workflows/daily-crawl.yml`：

```yaml
on:
  schedule:
    # 修改这里的 cron 表达式
    # 格式: 分钟 小时 日 月 星期
    # 示例: '0 0 * * *' 表示每天 UTC 0:00 (北京时间 8:00)
    - cron: '0 0 * * *'
```

### 添加/删除编程语言

编辑 `src/main.py`：

```python
# 修改这里的语言列表
github_languages = ['python', 'javascript', 'go', 'rust', 'java', 'typescript', 'cpp']
```

同时修改前端 `docs/index.html` 中的语言标签。

### 添加/删除 RSS 订阅源

编辑 `src/crawlers/rss_feeds.py`：

```python
self.feeds = {
    'TechCrunch': 'https://techcrunch.com/feed/',
    'Your Site': 'https://yoursite.com/feed/',  # 添加新的源
}
```

## 📊 数据说明

### 数据文件

- `data/latest.json` - 最新聚合数据（供前端使用）
- `data/github_trending.json` - GitHub Trending 完整数据
- `data/hackernews.json` - Hacker News 完整数据
- `data/rss_feeds.json` - RSS 文章完整数据
- `data/archive/YYYY-MM-DD.json` - 每日归档数据

### 数据格式

```json
{
  "updated_at": "2024-01-30T08:00:00",
  "github_trending": {
    "python": [...],
    "javascript": [...]
  },
  "hackernews": [...],
  "rss_feeds": [...]
}
```

## 🎨 自定义样式

修改 `docs/css/style.css` 中的 CSS 变量：

```css
:root {
    --primary-color: #667eea;      /* 主色调 */
    --secondary-color: #764ba2;    /* 次要色 */
    --text-color: #2d3748;         /* 文字颜色 */
    --bg-color: #f7fafc;           /* 背景色 */
}
```

## 📝 常见问题

### Q: 为什么数据没有更新？

A: 检查以下几点：
1. GitHub Actions 是否已启用
2. 查看 Actions 标签页是否有错误日志
3. 确认 workflow 文件的 cron 表达式正确

### Q: 如何修改抓取数量？

A: 编辑 `src/main.py` 中的 limit 参数：

```python
hackernews = self.hn_crawler.get_top_stories(limit=50)  # 修改这里
```

### Q: 爬虫被反爬了怎么办？

A: 可以：
1. 增加请求间隔时间
2. 使用代理 IP
3. 修改 User-Agent

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [GitHub Trending](https://github.com/trending)
- [Hacker News API](https://github.com/HackerNews/API)
- 所有 RSS 订阅源提供者

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [Your Name](https://github.com/yourusername)
