"""
主程序 - 每日科技资讯聚合器
Tech News Daily Aggregator
"""
import json
import os
from datetime import datetime
from crawlers.github_trending import GitHubTrendingCrawler
from crawlers.hackernews import HackerNewsCrawler
from crawlers.rss_feeds import RSSFeedCrawler


class TechNewsAggregator:
    def __init__(self):
        self.github_crawler = GitHubTrendingCrawler()
        self.hn_crawler = HackerNewsCrawler()
        self.rss_crawler = RSSFeedCrawler()
        
        # 确保目录存在
        os.makedirs('data/archive', exist_ok=True)
        os.makedirs('docs/data', exist_ok=True)
    
    def crawl_all(self):
        """执行所有爬虫任务"""
        print("="*60)
        print("🚀 开始抓取科技资讯...")
        print("="*60)
        
        timestamp = datetime.now().isoformat()
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 1. 抓取 GitHub Trending
        print("\n📊 [1/3] GitHub Trending")
        print("-"*60)
        github_languages = ['python', 'javascript', 'go', 'rust', 'java', 'typescript']
        github_trending = self.github_crawler.get_multiple_languages(github_languages, 'daily')
        
        # 2. 抓取 Hacker News
        print("\n📰 [2/3] Hacker News")
        print("-"*60)
        hackernews = self.hn_crawler.get_top_stories(limit=30)
        
        # 3. 抓取 RSS 订阅源
        print("\n📡 [3/3] RSS Feeds")
        print("-"*60)
        rss_articles = self.rss_crawler.get_all_feeds(limit_per_feed=10, include_chinese=True)
        
        # 保存数据
        print("\n💾 保存数据...")
        self.save_data(timestamp, date_str, github_trending, hackernews, rss_articles)
        
        # 生成统计信息
        self.print_statistics(github_trending, hackernews, rss_articles)
        
        print("\n" + "="*60)
        print("✅ 所有任务完成!")
        print("="*60)
    
    def save_data(self, timestamp, date_str, github_trending, hackernews, rss_articles):
        """保存抓取的数据"""
        
        # 1. 保存 GitHub Trending
        github_data = {
            'timestamp': timestamp,
            'date': date_str,
            'data': github_trending
        }
        self._save_json('data/github_trending.json', github_data)
        
        # 2. 保存 Hacker News
        hn_data = {
            'timestamp': timestamp,
            'date': date_str,
            'data': hackernews
        }
        self._save_json('data/hackernews.json', hn_data)
        
        # 3. 保存 RSS 文章
        rss_data = {
            'timestamp': timestamp,
            'date': date_str,
            'data': rss_articles
        }
        self._save_json('data/rss_feeds.json', rss_data)
        
        # 4. 生成合并的最新数据（供前端使用）
        latest_data = {
            'updated_at': timestamp,
            'date': date_str,
            'github_trending': github_trending,
            'hackernews': hackernews[:20],  # 只保留前20条
            'rss_feeds': rss_articles[:30],  # 只保留前30条
            'statistics': {
                'github_repos': sum(len(repos) for repos in github_trending.values()),
                'hackernews_stories': len(hackernews),
                'rss_articles': len(rss_articles),
                'total': sum(len(repos) for repos in github_trending.values()) + len(hackernews) + len(rss_articles)
            }
        }
        
        # 保存到 data 目录
        self._save_json('data/latest.json', latest_data)
        
        # 同步到 docs 目录（供 GitHub Pages 使用）
        self._save_json('docs/data/latest.json', latest_data)
        
        # 5. 保存每日归档
        archive_file = f'data/archive/{date_str}.json'
        archive_data = {
            'date': date_str,
            'timestamp': timestamp,
            'github_trending': github_trending,
            'hackernews': hackernews,
            'rss_feeds': rss_articles
        }
        self._save_json(archive_file, archive_data)
        
        print(f"   ✓ 数据已保存")
        print(f"   ✓ 归档: {archive_file}")
    
    def _save_json(self, filepath, data):
        """保存 JSON 文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存文件失败 {filepath}: {e}")
    
    def print_statistics(self, github_trending, hackernews, rss_articles):
        """打印统计信息"""
        print("\n📈 统计信息")
        print("-"*60)
        
        github_total = sum(len(repos) for repos in github_trending.values())
        print(f"   GitHub Trending: {github_total} 个项目")
        for lang, repos in github_trending.items():
            print(f"      - {lang}: {len(repos)} 个")
        
        print(f"   Hacker News: {len(hackernews)} 条新闻")
        print(f"   RSS Feeds: {len(rss_articles)} 篇文章")
        
        # RSS 按来源统计
        rss_by_source = {}
        for article in rss_articles:
            source = article.get('source', 'Unknown')
            rss_by_source[source] = rss_by_source.get(source, 0) + 1
        
        for source, count in sorted(rss_by_source.items()):
            print(f"      - {source}: {count} 篇")
        
        total = github_total + len(hackernews) + len(rss_articles)
        print(f"   总计: {total} 条资讯")


def main():
    """主函数"""
    aggregator = TechNewsAggregator()
    aggregator.crawl_all()


if __name__ == '__main__':
    main()
