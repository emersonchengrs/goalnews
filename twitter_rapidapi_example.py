#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RapidAPI Twitter API 使用示例
如果 snscrape 不可用，可以使用这个文件作为参考来配置 RapidAPI
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime


def fetch_tweets_rapidapi_twitter_scraper(username: str, api_key: str, limit: int = 10) -> List[Dict]:
    """
    使用 RapidAPI 的 "Twitter Scraper" API
    API 端点: https://rapidapi.com/rockapis-rockapis-default/api/twitter-scraper-api
    
    Args:
        username: Twitter 用户名（不含 @）
        api_key: RapidAPI API Key
        limit: 获取的推文数量
    
    Returns:
        推文列表
    """
    url = "https://twitter-scraper-api.p.rapidapi.com/user"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "twitter-scraper-api.p.rapidapi.com"
    }
    
    params = {
        "username": username,
        "count": str(limit)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            tweets = []
            
            # 根据实际 API 响应格式解析
            if 'tweets' in data:
                for tweet_data in data['tweets'][:limit]:
                    tweet = {
                        'source': f'Twitter - {username}',
                        'title': tweet_data.get('text', tweet_data.get('full_text', ''))[:200],
                        'link': tweet_data.get('url', f"https://twitter.com/{username}/status/{tweet_data.get('id', '')}"),
                        'published': tweet_data.get('created_at', datetime.now().isoformat()),
                        'published_raw': tweet_data.get('created_at', ''),
                        'tweet_id': str(tweet_data.get('id', '')),
                        'retweet_count': tweet_data.get('retweet_count', 0),
                        'like_count': tweet_data.get('favorite_count', tweet_data.get('like_count', 0)),
                    }
                    tweets.append(tweet)
            
            return tweets
        else:
            print(f"API 请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return []
    
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return []


def fetch_tweets_rapidapi_twitter_api_v2(username: str, api_key: str, limit: int = 10) -> List[Dict]:
    """
    使用 RapidAPI 的 "Twitter API v2" 
    API 端点: https://rapidapi.com/twitter-api-v2/api/twitter-api-v2
    
    Args:
        username: Twitter 用户名（不含 @）
        api_key: RapidAPI API Key
        limit: 获取的推文数量
    
    Returns:
        推文列表
    """
    # 首先获取用户 ID
    user_url = "https://twitter-api-v2.p.rapidapi.com/user/by_username"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "twitter-api-v2.p.rapidapi.com"
    }
    
    params = {"username": username}
    
    try:
        # 获取用户信息
        user_response = requests.get(user_url, headers=headers, params=params, timeout=15)
        
        if user_response.status_code != 200:
            print(f"获取用户信息失败: {user_response.status_code}")
            return []
        
        user_data = user_response.json()
        user_id = user_data.get('data', {}).get('id')
        
        if not user_id:
            print(f"无法获取用户 ID")
            return []
        
        # 获取用户推文
        tweets_url = "https://twitter-api-v2.p.rapidapi.com/user/tweets"
        tweets_params = {
            "id": user_id,
            "max_results": str(limit)
        }
        
        tweets_response = requests.get(tweets_url, headers=headers, params=tweets_params, timeout=15)
        
        if tweets_response.status_code == 200:
            tweets_data = tweets_response.json()
            tweets = []
            
            if 'data' in tweets_data:
                for tweet_data in tweets_data['data'][:limit]:
                    tweet = {
                        'source': f'Twitter - {username}',
                        'title': tweet_data.get('text', '')[:200],
                        'link': f"https://twitter.com/{username}/status/{tweet_data.get('id', '')}",
                        'published': tweet_data.get('created_at', datetime.now().isoformat()),
                        'published_raw': tweet_data.get('created_at', ''),
                        'tweet_id': str(tweet_data.get('id', '')),
                        'retweet_count': tweet_data.get('public_metrics', {}).get('retweet_count', 0),
                        'like_count': tweet_data.get('public_metrics', {}).get('like_count', 0),
                    }
                    tweets.append(tweet)
            
            return tweets
        else:
            print(f"获取推文失败: {tweets_response.status_code}")
            return []
    
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return []


def fetch_tweets_rapidapi_twitter_api_45(username: str, api_key: str, limit: int = 10) -> List[Dict]:
    """
    使用 RapidAPI 的 "Twitter API 45" 
    API 端点: https://rapidapi.com/omarmhaimdat/api/twitter-api45
    
    Args:
        username: Twitter 用户名（不含 @）
        api_key: RapidAPI API Key
        limit: 获取的推文数量
    
    Returns:
        推文列表
    """
    url = "https://twitter-api45.p.rapidapi.com/timeline.php"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
    }
    
    params = {
        "screenname": username,
        "count": str(limit)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            tweets = []
            
            if 'timeline' in data:
                for tweet_data in data['timeline'][:limit]:
                    tweet = {
                        'source': f'Twitter - {username}',
                        'title': tweet_data.get('text', tweet_data.get('full_text', ''))[:200],
                        'link': tweet_data.get('url', f"https://twitter.com/{username}/status/{tweet_data.get('id', '')}"),
                        'published': tweet_data.get('created_at', datetime.now().isoformat()),
                        'published_raw': tweet_data.get('created_at', ''),
                        'tweet_id': str(tweet_data.get('id', '')),
                        'retweet_count': tweet_data.get('retweet_count', 0),
                        'like_count': tweet_data.get('favorite_count', tweet_data.get('like_count', 0)),
                    }
                    tweets.append(tweet)
            
            return tweets
        else:
            print(f"API 请求失败，状态码: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return []


# 使用示例
if __name__ == '__main__':
    # 从环境变量获取 API Key
    api_key = os.getenv('RAPIDAPI_KEY')
    
    if not api_key:
        print("请设置 RAPIDAPI_KEY 环境变量")
        print("export RAPIDAPI_KEY='your-api-key-here'")
    else:
        # 测试获取 Fabrizio Romano 的推文
        print("测试获取 Fabrizio Romano 的推文...")
        
        # 尝试不同的 API（根据你订阅的 RapidAPI 服务选择）
        tweets = fetch_tweets_rapidapi_twitter_api_45('FabrizioRomano', api_key, limit=5)
        
        if tweets:
            print(f"\n成功获取 {len(tweets)} 条推文:")
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. {tweet['title']}")
                print(f"   链接: {tweet['link']}")
                print(f"   发布时间: {tweet['published']}")
        else:
            print("未能获取推文，请检查 API Key 和网络连接")

