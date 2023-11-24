import os
import re
from playwright.async_api import Playwright, async_playwright
import time
from ConstText import *
from ConstURLs import *
from Utils import *

class XG_Uploader():
    def __init__(self,basePath):
        super(XG_Uploader, self).__init__()
        self._basePath = basePath
        self._cookiePath = os.path.join(basePath,'xgCookie.json')

    async def upload(self, playwright: Playwright, filePath:str) -> None:
        browser = await playwright.chromium.launch(
            executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=False)
        context = None

        no_cookie = False

        if os.path.exists(self._cookiePath):
            context = await browser.new_context(
                storage_state=self._cookiePath,
                geolocation={'latitude':31,'longitude':121}
                )
        else:
            context = await browser.new_context()
            no_cookie = True
        page = await context.new_page()
        await page.goto("https://studio.ixigua.com/upload?from=post_article")

        if no_cookie:
            time.sleep(20)
            await context.storage_state(path=self._cookiePath)

        print("Step GoTo")

        time.sleep(2)

        file_input = page.locator('input[type=file]')
        await file_input.set_input_files(filePath)
        page.wait_for_timeout(5000)        
        print("Step set file")
        time.sleep(20)

        v_title,v_screenMode,v_desc = filePath_Infos(filePath)
        print("to fill title")       
        await page.locator("div").filter(has_text=re.compile(r"^5-30个字符，标题含有关键词，可以被更多人看到0/30$")).get_by_role("combobox").fill(v_title)
        time.sleep(1)

        print("to fill tag")
        for tag in c_XG_Tags:
            tag_input = page.locator('xpath=//*[@id="js-video-list-content"]/div/div[2]/div[4]/div[2]/div/div/div/div[1]/div/div/div[1]/input')
            print(f'fill tag:{tag}')
            await tag_input.type(f" {tag}")
            time.sleep(1)
            await tag_input.press('Enter')
            # await tag_input.press('Enter')
            time.sleep(1)
        

        print('to upload cover')
        await page.locator("div").filter(has_text=re.compile(r"^上传封面$")).nth(2).click()
        time.sleep(1)
        await page.locator(".byte-slider").click()
        time.sleep(1)
        await page.get_by_text("下一步").click()
        time.sleep(1)
        await page.get_by_role("button", name="确定").click()
        time.sleep(1)
        await page.get_by_role("button", name="确定").nth(1).click()

        time.sleep(2)

        print('to select 原创')
        await page.locator("label").filter(has_text="原创").locator("div").click()

        print('to fill desc')
        # page.locator("div").filter(has_text=re.compile(r"^请填写视频简介0/400$")).get_by_role("combobox").locator("div").nth(2).click()
        await page.locator("div").filter(has_text=re.compile(r"^请填写视频简介0/400$")).get_by_role("combobox").fill(v_desc)

        print('to process 贴纸')
        await page.get_by_text("添加贴纸").click()
        time.sleep(1)
        await page.locator("div:nth-child(2) > .community-sticker-btn > .community-sticker-btn-icon-ctn > .community-sticker-btn-icon").click()
        time.sleep(1)
        await page.get_by_role("spinbutton").nth(1).click()
        time.sleep(1)
        await page.get_by_role("spinbutton").nth(1).fill("5")
        time.sleep(1)
        await page.get_by_role("button", name="确定").click()

        print('to publish')
        await page.locator("label").filter(has_text="定时发布").locator("div").click()
        await page.get_by_placeholder("请选择时间").first.click()
        await page.get_by_text("30", exact=True).nth(1).click()
        # await page.get_by_role("button", name="发布").click()

        print('Send is OK')

        await page.wait_for_timeout(1000)
        await context.storage_state(path=self._cookiePath)
        await context.close()
        await browser.close()

    async def main(self,filePath):
        async with async_playwright() as playwright:
            await self.upload(playwright,filePath)
