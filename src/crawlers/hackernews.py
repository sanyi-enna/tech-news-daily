"""
Hacker News API 爬虫
抓取 Hacker News 热门新闻
"""
import requests
from datetime import datetime
import time


class HackerNewsCrawler:
    def __init__(self):
        self.base_url = 'https://hacker-news.firebaseio.com/v0'
        self.session = requests.Session()
    
    def get_top_stories(self, limit=30):
        """
        获取热门故事
        
        Args:
            limit: 返回数量
        
        Returns:
            list: 故事列表
        """
        try:
            print(f"📡 正在抓取 Hacker News Top Stories...")
            
            # 获取故事 ID 列表
            stories_url = f'{self.base_url}/topstories.json'
            response = self.session.get(stories_url, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            stories = []
            for i, story_id in enumerate(story_ids):
                try:
                    story = self.get_story(story_id)
                    if story:
                        stories.append(story)
                    
                    # 显示进度
                    if (i + 1) % 10 == 0:
                        print(f"   已抓取 {i + 1}/{len(story_ids)}")
                    
                    # 避免请求过快
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"⚠️  获取故事 {story_id} 失败: {e}")
                    continue
            
            print(f"✅ 成功抓取 {len(stories)} 条 Hacker News")
            return stories
            
        except Exception as e:
            print(f"❌ 抓取 Hacker News 失败: {e}")
            return []
    
    def get_story(self, story_id):
        """
        获取单个故事详情
        
        Args:
            story_id: 故事 ID
        
        Returns:
            dict: 故事信息
        """
        try:
            story_url = f'{self.base_url}/item/{story_id}.json'
            response = self.session.get(story_url, timeout=10)
            response.raise_for_status()
            story = response.json()
            
            if not story:
                return None
            
            # 只返回 story 类型的内容
            if story.get('type') != 'story':
                return None
            
            # 格式化时间
            timestamp = story.get('time', 0)
            published_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                'id': story.get('id'),
                'title': story.get('title', 'No Title'),
                'url': story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                'score': story.get('score', 0),
                'author': story.get('by', 'unknown'),
                'time': published_time,
                'timestamp': timestamp,
                'comments': story.get('descendants', 0),
                'hn_url': f'https://news.ycombinator.com/item?id={story_id}'
            }
            
        except Exception as e:
            print(f"⚠️  获取故事 {story_id} 详情失败: {e}")
            return None
    
    def get_best_stories(self, limit=30):
        """获取最佳故事"""
        try:
            print(f"📡 正在抓取 Hacker News Best Stories...")
            stories_url = f'{self.base_url}/beststories.json'
            response = self.session.get(stories_url, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            stories = []
            for story_id in story_ids:
                story = self.get_story(story_id)
                if story:
                    stories.append(story)
                time.sleep(0.1)
            
            print(f"✅ 成功抓取 {len(stories)} 条 Best Stories")
            return stories
            
        except Exception as e:
            print(f"❌ 抓取 Best Stories 失败: {e}")
            return []
    
    def get_new_stories(self, limit=30):
        """获取最新故事"""
        try:
            print(f"📡 正在抓取 Hacker News New Stories...")
            stories_url = f'{self.base_url}/newstories.json'
            response = self.session.get(stories_url, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            stories = []
            for story_id in story_ids:
                story = self.get_story(story_id)
                if story:
                    stories.append(story)
                time.sleep(0.1)
            
            print(f"✅ 成功抓取 {len(stories)} 条 New Stories")
            return stories
            
        except Exception as e:
            print(f"❌ 抓取 New Stories 失败: {e}")
            return []


if __name__ == '__main__':
    # 测试代码
    crawler = HackerNewsCrawler()
    
    # 测试 Top Stories
    stories = crawler.get_top_stories(10)
    print(f"\n📰 Hacker News Top Stories: {len(stories)} 条")
    
    if stories:
        print(f"\n示例新闻:")
        print(f"标题: {stories[0]['title']}")
        print(f"评分: {stories[0]['score']} points")
        print(f"评论: {stories[0]['comments']}")
        print(f"作者: {stories[0]['author']}")
