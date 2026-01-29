"""
GitHub Trending 爬虫
抓取 GitHub 每日热门项目
"""
import requests
from bs4 import BeautifulSoup
import time


class GitHubTrendingCrawler:
    def __init__(self):
        self.base_url = 'https://github.com/trending'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def get_trending(self, language='', since='daily', max_repos=25):
        """
        获取 GitHub Trending 项目
        
        Args:
            language: 编程语言，如 'python', 'javascript'
            since: 时间范围 'daily', 'weekly', 'monthly'
            max_repos: 最多返回项目数
        
        Returns:
            list: 项目列表
        """
        try:
            url = f'{self.base_url}/{language}?since={since}'
            print(f"📡 正在抓取: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            repos = []
            articles = soup.find_all('article', class_='Box-row')
            
            for article in articles[:max_repos]:
                try:
                    repo = self._parse_repo(article)
                    if repo:
                        repos.append(repo)
                except Exception as e:
                    print(f"⚠️  解析项目失败: {e}")
                    continue
            
            print(f"✅ 成功抓取 {len(repos)} 个 {language or 'All'} 项目")
            return repos
            
        except Exception as e:
            print(f"❌ 抓取失败 [{language}]: {e}")
            return []
    
    def _parse_repo(self, article):
        """解析单个仓库信息"""
        # 获取仓库名称和链接
        h2 = article.find('h2', class_='h3')
        if not h2:
            return None
        
        repo_link = h2.find('a')
        if not repo_link:
            return None
        
        repo_name = repo_link.get('href', '').strip('/')
        repo_url = f"https://github.com{repo_link.get('href', '')}"
        
        # 获取描述
        description_elem = article.find('p', class_='col-9')
        description = description_elem.get_text(strip=True) if description_elem else ''
        
        # 获取语言
        language_elem = article.find('span', itemprop='programmingLanguage')
        language = language_elem.get_text(strip=True) if language_elem else 'Unknown'
        
        # 获取 stars 数量
        stars = self._extract_number(article, 'octicon-star')
        
        # 获取 forks 数量
        forks = self._extract_number(article, 'octicon-repo-forked')
        
        # 获取今日 stars
        stars_today_elem = article.find('span', class_='d-inline-block float-sm-right')
        stars_today = '0'
        if stars_today_elem:
            stars_today_text = stars_today_elem.get_text(strip=True)
            # 提取数字，例如 "123 stars today" -> "123"
            import re
            match = re.search(r'([\d,]+)', stars_today_text)
            if match:
                stars_today = match.group(1)
        
        return {
            'name': repo_name,
            'url': repo_url,
            'description': description,
            'language': language,
            'stars': stars,
            'forks': forks,
            'stars_today': stars_today
        }
    
    def _extract_number(self, article, icon_class):
        """提取数字信息（stars, forks 等）"""
        svg = article.find('svg', class_=icon_class)
        if svg and svg.parent:
            text = svg.parent.get_text(strip=True)
            # 移除逗号，例如 "1,234" -> "1234"
            return text.replace(',', '')
        return '0'
    
    def get_multiple_languages(self, languages, since='daily'):
        """
        获取多个语言的 trending
        
        Args:
            languages: 语言列表
            since: 时间范围
        
        Returns:
            dict: {language: [repos]}
        """
        result = {}
        for lang in languages:
            result[lang] = self.get_trending(lang, since)
            # 避免请求过快
            time.sleep(2)
        
        return result


if __name__ == '__main__':
    # 测试代码
    crawler = GitHubTrendingCrawler()
    
    # 测试单个语言
    python_repos = crawler.get_trending('python', 'daily')
    print(f"\n🐍 Python Trending 项目数: {len(python_repos)}")
    if python_repos:
        print(f"示例项目: {python_repos[0]['name']}")
    
    # 测试多个语言
    languages = ['python', 'javascript', 'go']
    all_trending = crawler.get_multiple_languages(languages)
    print(f"\n📊 总计抓取 {sum(len(repos) for repos in all_trending.values())} 个项目")
