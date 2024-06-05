import os
from datetime import datetime, date
import time
from playwright.sync_api import Playwright, sync_playwright, expect

USERNAME = os.getenv('TIMETRACK_USERNAME')
PASSWORD = os.getenv('TIMETRACK_PASSWORD')
URL = os.getenv('TIMETRACK_URL')
def run(playwright: Playwright, buttontext:str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)
    time.sleep(2)
    page.get_by_role("button").click()
    time.sleep(1)
    page.get_by_test_id("login-id-form").fill(USERNAME)
    page.get_by_test_id("password-form").fill(PASSWORD)
    page.get_by_test_id("submit").click()
    time.sleep(1)
    page.get_by_text(buttontext).click()
    time.sleep(2)
    page.close()

    # ---------------------
    context.close()
    browser.close()

def auto_punch():
    atime = os.getenv('TIMETRACK_ATIME')
    lttime = os.getenv('TIMETRACK_LTTIME')
    ltime = os.getenv('TIMETRACK_LTIME')
    attendtime = datetime.combine(date.today(),datetime.strptime(atime,'%H%M').time())
    latetime = datetime.combine(date.today(), datetime.strptime(lttime,"%H%M").time())
    leavetime = datetime.combine(date.today(), datetime.strptime(ltime, '%H%M').time())
    nowtime = datetime.now()

    if nowtime < attendtime:
        # 出勤時間前
        waitsecs = (attendtime - nowtime).seconds
        print(f"will wait for {waitsecs} secs until {attendtime}.")
        time.sleep(waitsecs)
        with sync_playwright() as playwright:
            run(playwright,"出勤")
    elif nowtime < latetime:
        print(f"will attend now.")
        with sync_playwright() as playwright:
            run(playwright,"出勤")
    elif nowtime < leavetime:
        # 退勤予定
        waitsecs = (leavetime - nowtime).seconds
        print(f"will wait for {waitsecs} secs until {leavetime}.")
        time.sleep(waitsecs)
        with sync_playwright() as playwright:
            run(playwright, "退勤")
    else:
        print(f"will leave now.")
        with sync_playwright() as playwright:
            run(playwright,"退勤")
if __name__ == '__main__':
    auto_punch()
    print('done')