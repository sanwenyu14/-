#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
import time
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class AutoCheckIn:
    def __init__(self):
        # 从环境变量获取敏感信息（GitHub Secrets）
        self.username = os.getenv('CHECKIN_USERNAME', '')
        self.password = os.getenv('CHECKIN_PASSWORD', '')
        self.cookie = os.getenv('CHECKIN_COOKIE', '')
        self.token = os.getenv('CHECKIN_TOKEN', '')
        
        # 签到配置（需要根据实际网站修改）
        self.config = {
            'login_url': os.getenv('LOGIN_URL', 'https://example.com/login'),
            'checkin_url': os.getenv('CHECKIN_URL', 'https://example.com/checkin'),
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def login(self):
        """登录示例（根据实际网站修改）"""
        if not self.config['login_url'] or self.config['login_url'] == 'https://example.com/login':
            logger.info("跳过登录（使用预设cookie/token）")
            return True
            
        try:
            payload = {
                'username': self.username,
                'password': self.password
            }
            
            headers = {
                'User-Agent': self.config['user_agent'],
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(
                self.config['login_url'],
                data=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("登录成功")
                # 提取并保存cookie/token
                # self.cookie = response.cookies.get_dict()
                return True
            else:
                logger.error(f"登录失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"登录异常: {str(e)}")
            return False
    
    def check_in(self):
        """执行签到"""
        try:
            # 构建请求头
            headers = {
                'User-Agent': self.config['user_agent'],
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            
            # 添加认证信息（根据实际情况选择一种）
            if self.cookie:
                headers['Cookie'] = self.cookie
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            
            # 请求参数（根据实际API修改）
            payload = {
                'action': 'checkin',
                'timestamp': int(time.time())
            }
            
            logger.info(f"开始签到: {self.config['checkin_url']}")
            
            # 发送签到请求
            response = requests.post(
                self.config['checkin_url'],
                json=payload,
                headers=headers,
                timeout=30
            )
            
            result = {
                'success': False,
                'status_code': response.status_code,
                'response': None,
                'message': ''
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['response'] = data
                    result['success'] = True
                    result['message'] = data.get('msg', '签到成功')
                    logger.info(f"签到成功: {result['message']}")
                except:
                    result['message'] = response.text[:200]
                    logger.info(f"签到返回: {result['message']}")
            else:
                result['message'] = f"HTTP {response.status_code}: {response.text[:200]}"
                logger.error(f"签到失败: {result['message']}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"请求异常: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
    
    def send_notification(self, result):
        """发送结果通知（可选）"""
        # 这里可以集成邮件、Server酱、Telegram、钉钉等通知
        webhook_url = os.getenv('NOTIFICATION_WEBHOOK')
        if not webhook_url:
            return
        
        try:
            notification = {
                'title': '自动签到结果',
                'content': f"""
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
状态: {'✅ 成功' if result['success'] else '❌ 失败'}
详情: {result.get('message', '无详细信息')}
                """.strip()
            }
            
            requests.post(webhook_url, json=notification, timeout=10)
            logger.info("通知发送成功")
        except:
            logger.warning("通知发送失败")

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始执行自动签到任务")
    logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checker = AutoCheckIn()
    
    # 如果需要登录，先登录
    if checker.username and checker.password:
        if not checker.login():
            logger.error("登录失败，退出")
            return
    
    # 执行签到
    result = checker.check_in()
    
    # 发送通知
    checker.send_notification(result)
    
    logger.info("自动签到任务完成")
    logger.info("=" * 50)
    
    # 如果失败，抛出异常让GitHub Actions标记为失败
    if not result['success']:
        raise Exception(f"签到失败: {result.get('message', '未知错误')}")

if __name__ == '__main__':
    main()
