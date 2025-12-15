#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
足球新闻 RSS Feed 抓取脚本
抓取 Sky Sports Football, BBC Sport Football 和 The Guardian Football 的新闻
使用 OpenAI API 翻译标题并调整转会新闻的语气
"""

import feedparser
import json
import os
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
from openai import OpenAI

# 尝试导入 snscrape（如果可用）
try:
    import snscrape.modules.twitter as sntwitter
    SNSCRAPE_AVAILABLE = True
except ImportError:
    SNSCRAPE_AVAILABLE = False
    print("⚠️  snscrape 未安装，将使用 RapidAPI 作为替代方案")

# 尝试导入免费翻译库（如果可用）
try:
    from deep_translator import GoogleTranslator
    try:
        from deep_translator import DeepL
    except:
        DeepL = None
    try:
        from deep_translator import LibreTranslator
    except:
        LibreTranslator = None
    FREE_TRANSLATOR_AVAILABLE = True
except ImportError:
    FREE_TRANSLATOR_AVAILABLE = False
    GoogleTranslator = None
    DeepL = None
    LibreTranslator = None


# RSS Feed URLs
RSS_FEEDS = {
    'Sky Sports': 'https://www.skysports.com/rss/football',
    'BBC Sport': 'https://feeds.bbci.co.uk/sport/football/rss.xml',
    'The Guardian': 'https://www.theguardian.com/football/rss',
    # 阿森纳相关新闻源
    'BBC Arsenal': 'https://feeds.bbci.co.uk/sport/football/teams/arsenal/rss.xml',
    'Sky Sports Arsenal': 'https://www.skysports.com/arsenal/rss',
}

# 知名足球记者 Twitter 用户名
JOURNALISTS = {
    'Fabrizio Romano': 'FabrizioRomano',
    'David Ornstein': 'David_Ornstein',  # 阿森纳专家
    'James Pearce': 'JamesPearceLFC',
    'Chris Wheatley': 'ChrisWheatley_',  # 阿森纳记者
    'Gianluca Di Marzio': 'DiMarzio',
    'Charles Watts': 'charles_watts',  # 阿森纳记者
    'James Benge': 'jamesbenge',  # 阿森纳记者
    'Romano Fabrizio': 'FabrizioRomano',  # 备用
}


def parse_feed(url: str, source: str) -> List[Dict]:
    """
    解析 RSS Feed 并提取新闻信息
    
    Args:
        url: RSS Feed URL
        source: 新闻来源名称
    
    Returns:
        包含新闻信息的字典列表
    """
    try:
        feed = feedparser.parse(url)
        news_items = []
        
        for entry in feed.entries:
            # 提取标题
            title = entry.get('title', '无标题')
            
            # 提取链接
            link = entry.get('link', '')
            
            # 提取发布时间
            published_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                # 将时间元组转换为 datetime 对象
                published_time = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'published'):
                # 如果只有字符串格式的时间，尝试解析
                try:
                    published_time = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                except:
                    try:
                        published_time = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                    except:
                        published_time = entry.published  # 保留原始字符串
            
            news_item = {
                'source': source,
                'title': title,
                'link': link,
                'published': published_time.isoformat() if isinstance(published_time, datetime) else str(published_time),
                'published_raw': entry.get('published', '')
            }
            
            news_items.append(news_item)
        
        return news_items
    
    except Exception as e:
        print(f"解析 {source} 的 RSS Feed 时出错: {e}")
        return []


def fetch_all_news(filter_arsenal: bool = False) -> List[Dict]:
    """
    抓取所有 RSS Feed 的新闻
    
    Args:
        filter_arsenal: 是否只抓取阿森纳相关新闻
    
    Returns:
        所有新闻的列表
    """
    all_news = []
    
    # 阿森纳相关关键词
    arsenal_keywords = [
        'arsenal', 'gunners', 'emirates', 'arteta', 'saka', 'odegaard',
        'martinelli', 'jesus', 'saliba', 'white', 'ramsdale', '阿森纳'
    ]
    
    for source, url in RSS_FEEDS.items():
        print(f"正在抓取 {source} 的新闻...")
        news_items = parse_feed(url, source)
        
        # 如果设置了过滤，只保留阿森纳相关新闻
        if filter_arsenal:
            filtered_items = []
            for item in news_items:
                title_lower = item.get('title', '').lower()
                if any(keyword in title_lower for keyword in arsenal_keywords):
                    filtered_items.append(item)
            news_items = filtered_items
            print(f"  过滤后阿森纳相关新闻: {len(news_items)} 条")
        
        all_news.extend(news_items)
        print(f"从 {source} 获取了 {len(news_items)} 条新闻\n")
    
    # 按发布时间排序（最新的在前）
    all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    return all_news


def translate_title_free(title: str, is_transfer: bool = False, translator_type: str = 'google') -> Dict[str, str]:
    """
    使用免费翻译服务翻译标题
    
    Args:
        title: 原始英文标题
        is_transfer: 是否为转会新闻
        translator_type: 翻译服务类型 ('google', 'deepl', 'libre')
    
    Returns:
        包含翻译后标题和是否转会的字典
    """
    try:
        if not FREE_TRANSLATOR_AVAILABLE:
            return {
                'title_cn': title,
                'is_transfer': is_transfer
            }
        
        # 选择翻译服务
        if translator_type == 'google' and GoogleTranslator:
            translator = GoogleTranslator(source='en', target='zh-CN')
        elif translator_type == 'deepl' and DeepL:
            # DeepL 需要 API key，但这里尝试使用免费版本
            try:
                translator = DeepL(source='en', target='zh', use_free_api=True)
            except:
                if GoogleTranslator:
                    translator = GoogleTranslator(source='en', target='zh-CN')
                else:
                    raise Exception("无法使用 DeepL 或 Google Translator")
        elif translator_type == 'libre' and LibreTranslator:
            translator = LibreTranslator(source='en', target='zh')
        else:
            if GoogleTranslator:
                translator = GoogleTranslator(source='en', target='zh-CN')
            else:
                raise Exception("Google Translator 不可用")
        
        # 翻译标题（添加重试机制）
        max_retries = 3
        translated = None
        
        for attempt in range(max_retries):
            try:
                translated = translator.translate(title)
                if translated and translated.strip():
                    break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)  # 等待后重试
                    continue
                else:
                    raise e
        
        if not translated or not translated.strip():
            # 如果翻译失败，返回原标题
            translated = title
        
        # 如果是转会新闻，添加激动人心的表达
        if is_transfer and translated != title:
            # 检查是否已经包含激动人心的词汇，如果没有则添加
            if '🚨' not in translated and '重磅' not in translated and '官宣' not in translated:
                # 随机添加一些激动人心的前缀
                prefixes = ['🚨', '💥', '✅']
                import random
                prefix = random.choice(prefixes)
                translated = f"{prefix} {translated}"
        
        return {
            'title_cn': translated,
            'is_transfer': is_transfer
        }
    
    except Exception as e:
        # 静默失败，返回原标题
        return {
            'title_cn': title,
            'is_transfer': is_transfer
        }


def translate_title_with_ai(title: str, client: OpenAI) -> Dict[str, str]:
    """
    使用 OpenAI API 翻译标题并调整语气
    
    Args:
        title: 原始英文标题
        client: OpenAI 客户端
    
    Returns:
        包含翻译后标题和是否转会的字典
    """
    try:
        # 首先判断是否是转会新闻
        transfer_keywords = [
            'transfer', 'sign', 'signing', 'deal', 'move', 'join', 'leave',
            'departure', 'arrival', 'agreement', 'contract', 'loan', 'permanent',
            'here we go', 'medical', 'completed', 'announced', 'confirmed'
        ]
        
        title_lower = title.lower()
        is_transfer = any(keyword in title_lower for keyword in transfer_keywords)
        
        # 构建提示词
        if is_transfer:
            prompt = f"""请将以下足球转会新闻标题翻译成中文，并使用 Fabrizio Romano 的激动人心的风格。

Fabrizio Romano 的风格特点：
- 使用"Here we go!"、"重磅！"、"官宣！"等激动人心的表达
- 使用感叹号和emoji（如✅、🚨、💥等）
- 语气兴奋、直接、有冲击力
- 突出转会的重大性和确定性

原标题：{title}

请只返回翻译后的中文标题，不要添加其他解释。"""
        else:
            prompt = f"""请将以下足球新闻标题准确翻译成中文，保持原意和语气。

原标题：{title}

请只返回翻译后的中文标题，不要添加其他解释。"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的足球新闻翻译专家，擅长将英文足球新闻翻译成流畅的中文。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 if is_transfer else 0.3,
            max_tokens=200
        )
        
        translated_title = response.choices[0].message.content.strip()
        
        return {
            'title_cn': translated_title,
            'is_transfer': is_transfer
        }
    
    except Exception as e:
        print(f"翻译标题时出错: {e}")
        return {
            'title_cn': title,  # 出错时返回原标题
            'is_transfer': False
        }


def process_news_with_translation(news_items: List[Dict], 
                                  api_key: Optional[str] = None,
                                  use_free_translator: bool = False,
                                  translator_type: str = 'google') -> List[Dict]:
    """
    为所有新闻添加中文翻译
    
    Args:
        news_items: 新闻列表
        api_key: OpenAI API 密钥（如果为 None，则从环境变量读取）
        use_free_translator: 是否使用免费翻译服务（默认 False，使用 OpenAI）
        translator_type: 免费翻译服务类型 ('google', 'deepl', 'libre')
    
    Returns:
        包含翻译的新闻列表
    """
    print("\n开始翻译新闻标题...")
    
    # 判断是否是转会新闻的关键词
    transfer_keywords = [
        'transfer', 'sign', 'signing', 'deal', 'move', 'join', 'leave',
        'departure', 'arrival', 'agreement', 'contract', 'loan', 'permanent',
        'here we go', 'medical', 'completed', 'announced', 'confirmed'
    ]
    
    # 使用免费翻译
    if use_free_translator or not os.getenv('OPENAI_API_KEY'):
        if not FREE_TRANSLATOR_AVAILABLE:
            print("⚠️  免费翻译库未安装，跳过翻译步骤")
            print("   可以运行: pip install deep-translator")
            return news_items
        
        print(f"使用免费翻译服务: {translator_type}")
        total = len(news_items)
        
        for i, item in enumerate(news_items, 1):
            title_lower = item['title'].lower()
            is_transfer = any(keyword in title_lower for keyword in transfer_keywords)
            
            if i % 10 == 0 or i == 1:
                print(f"正在处理第 {i}/{total} 条: {item['title'][:50]}...")
            
            # 使用免费翻译
            translation_result = translate_title_free(item['title'], is_transfer, translator_type)
            
            # 添加到新闻项
            item['title_cn'] = translation_result['title_cn']
            item['is_transfer'] = is_transfer
            
            # 添加延迟以避免速率限制（免费服务通常有速率限制）
            if i < total:
                time.sleep(0.3)  # 每次请求间隔 0.3 秒
        
        print(f"\n完成！共翻译了 {total} 条新闻标题\n")
        return news_items
    
    # 使用 OpenAI API
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  未设置 OPENAI_API_KEY，切换到免费翻译服务")
        return process_news_with_translation(news_items, use_free_translator=True, translator_type=translator_type)
    
    client = OpenAI(api_key=api_key)
    total = len(news_items)
    
    for i, item in enumerate(news_items, 1):
        print(f"正在处理第 {i}/{total} 条: {item['title'][:50]}...")
        
        # 翻译标题
        translation_result = translate_title_with_ai(item['title'], client)
        
        # 添加到新闻项
        item['title_cn'] = translation_result['title_cn']
        item['is_transfer'] = translation_result['is_transfer']
        
        # 添加延迟以避免 API 速率限制
        if i < total:
            time.sleep(0.5)  # 每次请求间隔 0.5 秒
    
    print(f"\n完成！共翻译了 {total} 条新闻标题\n")
    
    return news_items


def save_to_json(news_items: List[Dict], filename: str = 'football_news.json'):
    """
    将新闻保存到 JSON 文件
    
    Args:
        news_items: 新闻列表
        filename: 输出文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    print(f"新闻已保存到 {filename}")


def fetch_tweets_with_snscrape(username: str, limit: int = 10) -> List[Dict]:
    """
    使用 snscrape 获取指定用户的最新推文
    
    Args:
        username: Twitter 用户名（不含 @）
        limit: 获取的推文数量
    
    Returns:
        推文列表
    """
    tweets = []
    try:
        scraper = sntwitter.TwitterUserScraper(username)
        for i, tweet in enumerate(scraper.get_items()):
            if i >= limit:
                break
            
            tweet_data = {
                'source': f'Twitter - {username}',
                'title': tweet.rawContent[:200] if hasattr(tweet, 'rawContent') else tweet.content[:200],
                'link': tweet.url if hasattr(tweet, 'url') else f'https://twitter.com/{username}/status/{tweet.id}',
                'published': tweet.date.isoformat() if hasattr(tweet, 'date') and tweet.date else datetime.now().isoformat(),
                'published_raw': str(tweet.date) if hasattr(tweet, 'date') else '',
                'tweet_id': str(tweet.id) if hasattr(tweet, 'id') else '',
                'retweet_count': tweet.retweetCount if hasattr(tweet, 'retweetCount') else 0,
                'like_count': tweet.likeCount if hasattr(tweet, 'likeCount') else 0,
            }
            tweets.append(tweet_data)
        
        return tweets
    except Exception as e:
        print(f"使用 snscrape 获取 {username} 的推文时出错: {e}")
        return []


def fetch_tweets_with_rapidapi(username: str, api_key: str, limit: int = 10, api_type: str = 'auto') -> List[Dict]:
    """
    使用 RapidAPI 的 Twitter API 获取指定用户的最新推文
    
    支持多个 RapidAPI Twitter API 服务，会自动尝试可用的 API
    
    Args:
        username: Twitter 用户名（不含 @）
        api_key: RapidAPI API Key
        limit: 获取的推文数量
        api_type: API 类型 ('auto', 'api45', 'scraper', 'v2')，auto 会依次尝试
    
    Returns:
        推文列表
    """
    tweets = []
    
    # 定义多个 API 配置
    api_configs = []
    
    if api_type == 'auto':
        # 自动模式：尝试所有可用的 API
        api_configs = [
            {
                'name': 'Twitter API 45',
                'url': 'https://twitter-api45.p.rapidapi.com/timeline.php',
                'host': 'twitter-api45.p.rapidapi.com',
                'params': {'screenname': username, 'count': str(limit)},
                'parse_key': 'timeline'
            },
            {
                'name': 'Twitter Scraper',
                'url': 'https://twitter-scraper-api.p.rapidapi.com/user',
                'host': 'twitter-scraper-api.p.rapidapi.com',
                'params': {'username': username, 'count': str(limit)},
                'parse_key': 'tweets'
            },
        ]
    elif api_type == 'api45':
        api_configs = [{
            'name': 'Twitter API 45',
            'url': 'https://twitter-api45.p.rapidapi.com/timeline.php',
            'host': 'twitter-api45.p.rapidapi.com',
            'params': {'screenname': username, 'count': str(limit)},
            'parse_key': 'timeline'
        }]
    elif api_type == 'scraper':
        api_configs = [{
            'name': 'Twitter Scraper',
            'url': 'https://twitter-scraper-api.p.rapidapi.com/user',
            'host': 'twitter-scraper-api.p.rapidapi.com',
            'params': {'username': username, 'count': str(limit)},
            'parse_key': 'tweets'
        }]
    
    # 尝试每个 API 配置
    for config in api_configs:
        try:
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": config['host']
            }
            
            response = requests.get(config['url'], headers=headers, params=config['params'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # 解析数据
                tweet_list = data.get(config['parse_key'], [])
                
                for tweet_data in tweet_list[:limit]:
                    # 提取推文文本
                    text = tweet_data.get('text') or tweet_data.get('full_text') or tweet_data.get('content', '')
                    
                    # 提取推文 ID
                    tweet_id = str(tweet_data.get('id', ''))
                    
                    # 构建链接
                    link = tweet_data.get('url') or f"https://twitter.com/{username}/status/{tweet_id}"
                    
                    # 提取时间
                    created_at = tweet_data.get('created_at') or tweet_data.get('date', datetime.now().isoformat())
                    
                    tweet = {
                        'source': f'Twitter - {username}',
                        'title': text[:200] if text else '',
                        'link': link,
                        'published': created_at if isinstance(created_at, str) else created_at.isoformat() if hasattr(created_at, 'isoformat') else datetime.now().isoformat(),
                        'published_raw': str(created_at),
                        'tweet_id': tweet_id,
                        'retweet_count': tweet_data.get('retweet_count', tweet_data.get('retweets', 0)),
                        'like_count': tweet_data.get('favorite_count', tweet_data.get('like_count', tweet_data.get('likes', 0))),
                    }
                    tweets.append(tweet)
                
                if tweets:
                    print(f"  ✅ 使用 {config['name']} 成功获取推文")
                    return tweets
            else:
                if api_type == 'auto':
                    continue  # 尝试下一个 API
                else:
                    print(f"  ❌ {config['name']} 请求失败，状态码: {response.status_code}")
        
        except Exception as e:
            if api_type == 'auto':
                continue  # 尝试下一个 API
            else:
                print(f"  ❌ 使用 {config['name']} 时出错: {e}")
    
    return tweets


def fetch_journalist_tweets(journalists: Optional[Dict[str, str]] = None, 
                            limit_per_journalist: int = 5,
                            use_rapidapi: bool = False,
                            rapidapi_key: Optional[str] = None) -> List[Dict]:
    """
    获取多个知名记者的最新推文
    
    Args:
        journalists: 记者字典 {显示名称: Twitter用户名}，如果为 None 则使用默认列表
        limit_per_journalist: 每个记者获取的推文数量
        use_rapidapi: 是否使用 RapidAPI（如果 snscrape 不可用或失败）
        rapidapi_key: RapidAPI API Key（如果使用 RapidAPI）
    
    Returns:
        所有推文的列表
    """
    if journalists is None:
        journalists = JOURNALISTS
    
    all_tweets = []
    
    print(f"\n开始抓取记者推文...")
    print(f"使用方式: {'RapidAPI' if use_rapidapi or not SNSCRAPE_AVAILABLE else 'snscrape'}\n")
    
    for display_name, username in journalists.items():
        print(f"正在获取 {display_name} (@{username}) 的推文...")
        
        tweets = []
        
        # 优先尝试 snscrape（如果可用且未强制使用 RapidAPI）
        if SNSCRAPE_AVAILABLE and not use_rapidapi:
            tweets = fetch_tweets_with_snscrape(username, limit_per_journalist)
            
            # 如果 snscrape 失败，尝试 RapidAPI
            if not tweets and rapidapi_key:
                print(f"  snscrape 失败，尝试使用 RapidAPI...")
                tweets = fetch_tweets_with_rapidapi(username, rapidapi_key, limit_per_journalist)
        elif use_rapidapi or not SNSCRAPE_AVAILABLE:
            if not rapidapi_key:
                rapidapi_key = os.getenv('RAPIDAPI_KEY')
            
            if rapidapi_key:
                tweets = fetch_tweets_with_rapidapi(username, rapidapi_key, limit_per_journalist)
            else:
                print(f"  ⚠️  未提供 RapidAPI Key，跳过 {display_name}")
        
        if tweets:
            all_tweets.extend(tweets)
            print(f"  ✅ 获取了 {len(tweets)} 条推文")
        else:
            print(f"  ❌ 未能获取推文")
        
        # 添加延迟避免请求过快
        time.sleep(1)
    
    # 按发布时间排序（最新的在前）
    all_tweets.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    print(f"\n总共获取了 {len(all_tweets)} 条推文\n")
    
    return all_tweets


def print_news(news_items: List[Dict], limit: int = 10):
    """
    打印新闻到控制台
    
    Args:
        news_items: 新闻列表
        limit: 显示的数量限制
    """
    print(f"\n{'='*80}")
    print(f"最新足球新闻 (显示前 {min(limit, len(news_items))} 条)")
    print(f"{'='*80}\n")
    
    for i, item in enumerate(news_items[:limit], 1):
        transfer_mark = "🚨 [转会]" if item.get('is_transfer', False) else ""
        print(f"{i}. [{item['source']}] {transfer_mark}")
        print(f"   英文: {item['title']}")
        print(f"   中文: {item.get('title_cn', '未翻译')}")
        print(f"   链接: {item['link']}")
        print(f"   发布时间: {item['published']}")
        print()


def main(filter_arsenal: bool = False):
    """
    主函数
    
    Args:
        filter_arsenal: 是否只抓取阿森纳相关新闻
    """
    print("开始抓取足球新闻...\n")
    if filter_arsenal:
        print("🔴 仅抓取阿森纳相关新闻\n")
    
    # 抓取所有新闻
    all_news = fetch_all_news(filter_arsenal=filter_arsenal)
    
    # 抓取记者推文
    try:
        # 检查是否使用 RapidAPI
        use_rapidapi = os.getenv('USE_RAPIDAPI', 'false').lower() == 'true'
        rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        journalist_tweets = fetch_journalist_tweets(
            limit_per_journalist=5,
            use_rapidapi=use_rapidapi,
            rapidapi_key=rapidapi_key
        )
        
        # 将推文添加到新闻列表（格式统一）
        all_news.extend(journalist_tweets)
        
        # 重新排序
        all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        
    except Exception as e:
        print(f"\n⚠️  抓取记者推文时出错: {e}")
        print("继续处理其他新闻...")
    
    # 打印统计信息
    print(f"\n总共获取了 {len(all_news)} 条新闻/推文")
    print(f"来源分布:")
    for source in RSS_FEEDS.keys():
        count = sum(1 for item in all_news if item['source'] == source)
        if count > 0:
            print(f"  - {source}: {count} 条")
    
    twitter_count = sum(1 for item in all_news if 'Twitter' in item.get('source', ''))
    if twitter_count > 0:
        print(f"  - Twitter 推文: {twitter_count} 条")
    
    # 翻译标题（优先使用免费翻译，如果没有设置 OpenAI API Key）
    use_free = os.getenv('USE_FREE_TRANSLATOR', 'false').lower() == 'true'
    translator_type = os.getenv('TRANSLATOR_TYPE', 'google')  # google, deepl, libre
    
    # 如果没有 OpenAI API Key，自动使用免费翻译
    if not os.getenv('OPENAI_API_KEY') or use_free:
        use_free = True
        if not os.getenv('OPENAI_API_KEY'):
            print(f"\n未设置 OPENAI_API_KEY，自动使用免费翻译服务: {translator_type}")
        else:
            print(f"\n使用免费翻译服务: {translator_type}")
    
    try:
        all_news = process_news_with_translation(
            all_news, 
            use_free_translator=use_free,
            translator_type=translator_type
        )
        
        # 统计转会新闻数量
        transfer_count = sum(1 for item in all_news if item.get('is_transfer', False))
        print(f"\n统计信息:")
        print(f"  - 总新闻数: {len(all_news)}")
        print(f"  - 转会新闻: {transfer_count} 条")
        print(f"  - 其他新闻: {len(all_news) - transfer_count} 条")
        
    except ValueError as e:
        print(f"\n⚠️  警告: {e}")
        print("跳过翻译步骤，仅保存原始新闻数据")
    except Exception as e:
        print(f"\n❌ 翻译过程中出错: {e}")
        print("跳过翻译步骤，仅保存原始新闻数据")
    
    # 显示前 10 条新闻
    print_news(all_news, limit=10)
    
    # 保存到 JSON 文件
    save_to_json(all_news, 'football_news_translated.json')
    
    # 自动复制到 public 目录供网站使用
    try:
        import shutil
        public_file = 'public/news.json'
        if os.path.exists('public'):
            shutil.copy2('football_news_translated.json', public_file)
            print(f"✅ 数据已自动更新到 {public_file}")
    except Exception as e:
        print(f"⚠️  复制到 public 目录失败: {e}")
    
    return all_news


if __name__ == '__main__':
    import sys
    # 检查命令行参数，是否只抓取阿森纳新闻
    filter_arsenal = '--arsenal' in sys.argv or os.getenv('FILTER_ARSENAL', 'false').lower() == 'true'
    main(filter_arsenal=filter_arsenal)

