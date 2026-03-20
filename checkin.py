import os
from playwright.sync_api import sync_playwright

def run():
    # 从环境变量中获取账号和密码（为了安全，稍后会在 GitHub Secrets 中配置）
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")

    if not USERNAME or not PASSWORD:
        print("未找到账号或密码环境变量，请检查配置！")
        return

    with sync_playwright() as p:
        # 启动无头浏览器 (headless=True 表示不显示浏览器界面)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("正在访问登录页面...")
            page.goto("https://992236.xyz/login")

            # 1. 勾选用户协议同意 (请替换为实际的 CSS 选择器)
            # 例如：page.locator("#agreement-checkbox").click()
            print("勾选用户协议...")
            page.locator("替换为协议复选框的选择器").click()

            # 2. 选择登录方式 (请替换为实际的 CSS 选择器)
            # 例如：page.locator("text=账号密码登录").click()
            print("选择登录方式...")
            page.locator("替换为你要选择的登录方式的选择器").click()

            # 3. 输入账号和密码
            print("填写账号密码...")
            page.locator("替换为账号输入框的选择器").fill(USERNAME)
            page.locator("替换为密码输入框的选择器").fill(PASSWORD)

            # 4. 点击登录按钮
            print("点击登录...")
            page.locator("替换为登录按钮的选择器").click()

            # 等待页面跳转完成（或者等待某个登录成功后的元素出现）
            page.wait_for_load_state('networkidle')

            # 5. 跳转到签到页面
            print("正在跳转到个人中心页面...")
            page.goto("https://992236.xyz/console/personal")
            page.wait_for_load_state('networkidle')

            # 6. 点击签到按钮
            print("执行签到操作...")
            # 例如：page.locator("text=立即签到").click()
            page.locator("替换为签到按钮的选择器").click()
            
            # 等待几秒钟确保签到请求发送成功
            page.wait_for_timeout(3000)
            print("签到脚本执行完毕！")

        except Exception as e:
            print(f"执行过程中出现错误: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
