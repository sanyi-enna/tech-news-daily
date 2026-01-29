"""
RSS 订阅源爬虫
抓取各大科技媒体的 RSS Feed
"""
import feedparser
from datetime import datetime
import time


class RSSFeedCrawler:
    def __init__(self):
        # 英文科技媒体
        self.feeds = {
            'TechCrunch': 'https://techcrunch.com/feed/',
            'The Verge': 'https://www.theverge.com/rss/index.xml',
            'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
            'Wired': 'https://www.wired.com/feed/rss',
            'MIT Technology Review': 'https://www.technologyreview.com/feed/',
        }
        
        # 中文科技媒体
        self.chinese_feeds = {
            '36氪': 'https://36kr.com/feed',
            '少数派': 'https://sspai.com/feed',
            'InfoQ': 'https://www.infoq.cn/feed',
        }
    
    def parse_feed(self, url, source_name, limit=10):
        """
        解析单个 RSS Feed
        
        Args:
            url: RSS Feed URL
            source_name: 来源名称
            limit: 返回数量
        
        Returns:
            list: 文章列表
        """
        try:
            print(f"📡 正在抓取 {source_name}...")
            
            feed = feedparser.parse(url)
            
            if feed.bozo:  # 解析错误
                print(f"⚠️  RSS 解析警告: {source_name}")
            
            articles = []
            for entry in feed.entries[:limit]:
                try:
                    article = {
                        'title': entry.get('title', 'No Title'),
                        'url': entry.get('link', ''),
                        'source': source_name,
                        'published': self._format_time(entry),
                        'summary': self._get_summary(entry),
                        'author': entry.get('author', 'Unknown'),
                    }
                    articles.append(article)
                except Exception as e:
                    print(f"⚠️  解析条目失败: {e}")
                    continue
            
            print(f"✅ {source_name}: {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取 {source_name} 失败: {e}")
            return []
    
    def _format_time(self, entry):
        """格式化发布时间"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                dt = datetime(*entry.published_parsed[:6])
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        if hasattr(entry, 'published'):
            return entry.published
        
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _get_summary(self, entry):
        """获取摘要"""
        # 尝试多个可能的摘要字段
        if hasattr(entry, 'summary'):
            # 移除 HTML 标签
            summary = entry.summary
            from html.parser import HTMLParser
            
            class MLStripper(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.reset()
                    self.fed = []
                def handle_data(self, d):
                    self.fed.append(d)
                def get_data(self):
                    return ''.join(self.fed)
            
            s = MLStripper()
            s.feed(summary)
            clean_summary = s.get_data()
            
            # 限制长度
            return clean_summary[:200] + '...' if len(clean_summary) > 200 else clean_summary
        
        if hasattr(entry, 'description'):
            return entry.description[:200] + '...' if len(entry.description) > 200 else entry.description
        
        return ''
    
    def get_all_feeds(self, limit_per_feed=10, include_chinese=True):
        """
        获取所有订阅源
        
        Args:
            limit_per_feed: 每个源的文章数量
            include_chinese: 是否包含中文源
        
        Returns:
            list: 所有文章列表
        """
        all_articles = []
        
        # 抓取英文源
        for source, url in self.feeds.items():
            articles = self.parse_feed(url, source, limit_per_feed)
            all_articles.extend(articles)
            time.sleep(1)  # 避免请求过快
        
        # 抓取中文源
        if include_chinese:
            for source, url in self.chinese_feeds.items():
                articles = self.parse_feed(url, source, limit_per_feed)
                all_articles.extend(articles)
                time.sleep(1)
        
        print(f"\n✅ 总计抓取 {len(all_articles)} 篇文章")
        return all_articles
    
    def get_feeds_by_category(self, category='english', limit=10):
        """
        按类别获取订阅源
        
        Args:
            category: 'english' 或 'chinese'
            limit: 每个源的数量
        
        Returns:
            dict: {source: [articles]}
        """
        result = {}
        feeds = self.feeds if category == 'english' else self.chinese_feeds
        
        for source, url in feeds.items():
            result[source] = self.parse_feed(url, source, limit)
            time.sleep(1)
        
        return result


if __name__ == '__main__':
    # 测试代码
    crawler = RSSFeedCrawler()
    
    # 测试单个源
    articles = crawler.parse_feed(
        'https://techcrunch.com/feed/',
        'TechCrunch',
        5
    )
    print(f"\n📰 TechCrunch 文章: {len(articles)} 篇")
    if articles:
        print(f"示例标题: {articles[0]['title']}")
    
    # 测试所有源
    all_articles = crawler.get_all_feeds(limit_per_feed=5, include_chinese=False)
    print(f"\n📊 总计: {len(all_articles)} 篇文章")
