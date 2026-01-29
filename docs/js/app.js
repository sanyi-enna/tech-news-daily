/**
 * 每日科技资讯 - 前端逻辑
 * Daily Tech News Aggregator - Frontend
 */

// 全局状态
let appData = {
    github_trending: {},
    hackernews: [],
    rss_feeds: [],
    updated_at: null,
    currentLang: 'python',
    currentSource: 'all'
};

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    showLoading();
    await loadData();
    setupEventListeners();
    renderCurrentView();
}

// 加载数据
async function loadData() {
    try {
        const response = await fetch('data/latest.json');
        const data = await response.json();
        
        appData.github_trending = data.github_trending || {};
        appData.hackernews = data.hackernews || [];
        appData.rss_feeds = data.rss_feeds || [];
        appData.updated_at = data.updated_at;
        
        // 更新统计信息
        updateStats(data.statistics);
        
        // 更新时间
        updateTime(data.updated_at);
        
        // 初始化 RSS 来源按钮
        initRSSSources();
        
        console.log('✅ 数据加载成功', data);
        
    } catch (error) {
        console.error('❌ 数据加载失败:', error);
        showError('数据加载失败，请稍后重试');
    }
}

// 显示加载状态
function showLoading() {
    const sections = ['github-list', 'hackernews-list', 'rss-list'];
    sections.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.innerHTML = '<div class="loading">正在加载数据</div>';
        }
    });
}

// 显示错误
function showError(message) {
    const sections = ['github-list', 'hackernews-list', 'rss-list'];
    sections.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.innerHTML = `<div class="loading">${message}</div>`;
        }
    });
}

// 更新统计信息
function updateStats(stats) {
    if (stats) {
        document.getElementById('stat-github').textContent = stats.github_repos || 0;
        document.getElementById('stat-hn').textContent = stats.hackernews_stories || 0;
        document.getElementById('stat-rss').textContent = stats.rss_articles || 0;
    }
}

// 更新时间
function updateTime(timestamp) {
    if (!timestamp) return;
    
    const date = new Date(timestamp);
    const formatted = date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
    
    document.getElementById('update-time').textContent = `最后更新: ${formatted}`;
}

// 初始化 RSS 来源按钮
function initRSSSources() {
    const sources = new Set(['all']);
    appData.rss_feeds.forEach(article => {
        if (article.source) {
            sources.add(article.source);
        }
    });
    
    const container = document.getElementById('rss-sources');
    container.innerHTML = Array.from(sources).map(source => `
        <button class="source-btn ${source === 'all' ? 'active' : ''}" data-source="${source}">
            ${source === 'all' ? '全部' : source}
        </button>
    `).join('');
}

// 设置事件监听
function setupEventListeners() {
    // 导航按钮
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = e.target.dataset.section;
            switchSection(section);
        });
    });
    
    // 语言标签
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const lang = e.target.dataset.lang;
            switchLanguage(lang);
        });
    });
    
    // RSS 来源过滤（使用事件委托）
    document.getElementById('rss-sources').addEventListener('click', (e) => {
        if (e.target.classList.contains('source-btn')) {
            const source = e.target.dataset.source;
            switchRSSSource(source);
        }
    });
}

// 切换区域
function switchSection(section) {
    // 更新导航按钮状态
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // 显示对应内容区域
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(`${section}-section`).classList.add('active');
    
    // 渲染对应内容
    renderCurrentView();
}

// 切换编程语言
function switchLanguage(lang) {
    appData.currentLang = lang;
    
    // 更新按钮状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderGitHub();
}

// 切换 RSS 来源
function switchRSSSource(source) {
    appData.currentSource = source;
    
    // 更新按钮状态
    document.querySelectorAll('.source-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderRSS();
}

// 渲染当前视图
function renderCurrentView() {
    const activeSection = document.querySelector('.content-section.active');
    if (!activeSection) return;
    
    const sectionId = activeSection.id;
    
    if (sectionId === 'github-section') {
        renderGitHub();
    } else if (sectionId === 'hackernews-section') {
        renderHackerNews();
    } else if (sectionId === 'rss-section') {
        renderRSS();
    }
}

// 渲染 GitHub Trending
function renderGitHub() {
    const container = document.getElementById('github-list');
    const repos = appData.github_trending[appData.currentLang] || [];
    
    if (repos.length === 0) {
        container.innerHTML = '<div class="loading">暂无数据</div>';
        return;
    }
    
    container.innerHTML = repos.map(repo => `
        <div class="card">
            <h3 class="card-title">
                <a href="${repo.url}" target="_blank" rel="noopener noreferrer">
                    ${escapeHtml(repo.name)}
                </a>
            </h3>
            <p class="card-description">${escapeHtml(repo.description || '暂无描述')}</p>
            <div class="card-meta">
                <span>⭐ ${repo.stars}</span>
                <span>📈 ${repo.stars_today} today</span>
                ${repo.forks !== '0' ? `<span>🔀 ${repo.forks}</span>` : ''}
                <span>💻 ${repo.language}</span>
            </div>
        </div>
    `).join('');
}

// 渲染 Hacker News
function renderHackerNews() {
    const container = document.getElementById('hackernews-list');
    const stories = appData.hackernews;
    
    if (stories.length === 0) {
        container.innerHTML = '<div class="loading">暂无数据</div>';
        return;
    }
    
    container.innerHTML = stories.map(story => `
        <div class="card">
            <h3 class="card-title">
                <a href="${story.url}" target="_blank" rel="noopener noreferrer">
                    ${escapeHtml(story.title)}
                </a>
            </h3>
            <div class="card-meta">
                <span>👍 ${story.score} points</span>
                <span>💬 <a href="${story.hn_url}" target="_blank" rel="noopener noreferrer">${story.comments} comments</a></span>
                <span>👤 ${escapeHtml(story.author)}</span>
            </div>
            <p class="card-time">📅 ${story.time}</p>
        </div>
    `).join('');
}

// 渲染 RSS Feeds
function renderRSS() {
    const container = document.getElementById('rss-list');
    let articles = appData.rss_feeds;
    
    // 按来源过滤
    if (appData.currentSource !== 'all') {
        articles = articles.filter(a => a.source === appData.currentSource);
    }
    
    if (articles.length === 0) {
        container.innerHTML = '<div class="loading">暂无数据</div>';
        return;
    }
    
    container.innerHTML = articles.map(article => `
        <div class="card">
            <span class="card-source">${escapeHtml(article.source)}</span>
            <h3 class="card-title">
                <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                    ${escapeHtml(article.title)}
                </a>
            </h3>
            ${article.summary ? `<p class="card-description">${escapeHtml(article.summary)}</p>` : ''}
            <div class="card-meta">
                ${article.author !== 'Unknown' ? `<span>👤 ${escapeHtml(article.author)}</span>` : ''}
                <span>📅 ${article.published}</span>
            </div>
        </div>
    `).join('');
}

// HTML 转义（防止 XSS）
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// 调试函数
window.debugApp = () => {
    console.log('App Data:', appData);
    console.log('GitHub Repos:', Object.keys(appData.github_trending).reduce((sum, lang) => 
        sum + appData.github_trending[lang].length, 0));
    console.log('Hacker News:', appData.hackernews.length);
    console.log('RSS Articles:', appData.rss_feeds.length);
};
