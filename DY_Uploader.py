import os
from playwright.async_api import Playwright, async_playwright
import time
from ConstText import *
from ConstURLs import *
from Utils import *

class DY_Uploader():
    def __init__(self,basePath):
        super(DY_Uploader, self).__init__()
        self._basePath = basePath
        self._cookiePath = os.path.join(basePath,'dyCookie.json')

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
        await page.goto(c_UploadURL)

        if no_cookie:
            time.sleep(20)
            await context.storage_state(path=self._cookiePath)

        print("Step GoTo")

        time.sleep(2)

        upload_btn = page.locator(f"span:has-text({c_UploadBtnText})")
        await upload_btn.set_input_files(filePath)
        
        print("Step set file")

        # await page.wait_for_url(c_PublishURL)
        time.sleep(10)

        print("Step to fill title")

        v_title,v_screenMode,v_desc = filePath_Infos(filePath)

        title_input = page.locator(".zone-container")
        await title_input.click()
        await title_input.type(v_title)

        for tag in c_DY_Tags:
            await title_input.type(f" {tag}")
            await title_input.press('Enter')
            time.sleep(1)

        print("Step title filled")

        time.sleep(5)

        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[5]/div/div[2]/div[1]/div/div[1]/div').click()
        print("Cover is ok")

        # await page.get_by_text("请选择合集").click()
        # await page.get_by_text("主力资金归一化 概念榜").click()

        time.sleep(5)

        # await page.locator(
        #     'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        
        print('Send is OK')

        await page.wait_for_timeout(10)

        await context.storage_state(path=self._cookiePath)
        await context.close()
        await browser.close()

    async def main(self,filePath):
        async with async_playwright() as playwright:
            await self.upload(playwright,filePath)
