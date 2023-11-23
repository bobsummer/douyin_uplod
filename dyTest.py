import asyncio
from playwright.async_api import Playwright, async_playwright
import time
from ConstText import *
from ConstURLs import *
from Utils import *
from datetime import datetime

c_DataPath = r'd:\\Dailys'
c_CookiePath = c_DataPath+'\\cookie.json'

class Uploader():
    # def __init__(self):
    #     super(Uploader, self).__init__()

    async def upload(self, playwright: Playwright, filePath:str) -> None:
        browser = await playwright.chromium.launch(
            executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=False)
        context = None

        no_cookie = False

        if os.path.exists(c_CookiePath):
            context = await browser.new_context(
                storage_state=c_CookiePath,
                geolocation={'latitude':31,'longitude':121}
                )
        else:
            context = await browser.new_context()
            no_cookie = True
        page = await context.new_page()
        await page.goto(c_UploadURL)

        if no_cookie:
            time.sleep(20)
            await context.storage_state(path=c_CookiePath)

        print("Step GoTo")

        time.sleep(2)

        upload_btn = page.locator(f"span:has-text({c_UploadBtnText})")
        await upload_btn.set_input_files(filePath)
        
        print("Step set file")

        # await page.wait_for_url(c_PublishURL)
        time.sleep(10)

        print("Step to fill title")

        v_title,v_screenMode,v_desc = filePath_Infos(filePath)

        # await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(v_title)
        # await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(v_title)
        title_input = page.locator(".zone-container")
        await title_input.click()
        await title_input.fill(v_title)
        await title_input.fill(f"{v_title} #原创")
        await page.keyboard.press('Enter')
        # await title_input.fill(f"{v_title} ​ #原创 #股票")
        # await page.keyboard.press('Enter')
        # await page.get_by_text("#  原创", exact=True).click()
        # await title_input.fill(f"{v_title} ​ #原创 #股票")
        # await page.get_by_text("#  股票", exact=True).click()
        # await title_input.fill(f"{v_title} ​ #原创  #股票")

        print("Step title filled")

        time.sleep(20)

        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[5]/div/div[2]/div[1]/div/div[1]/div').click()
        print("Cover is ok")

        # await page.get_by_text("请选择合集").click()
        # await page.get_by_text("主力资金归一化 概念榜").click()

        time.sleep(30)

        await page.locator(
            'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        
        print('Send is OK')

        await page.wait_for_timeout(10)

        await context.storage_state(path=c_CookiePath)
        await context.close()
        await browser.close()

    async def main(self,filePath):
        async with async_playwright() as playwright:
            await self.upload(playwright,filePath)

g_ForceDate = None
g_basePath = 'D:\\Dailys\\'

def main():    
    today = None
    if g_ForceDate is None:
        today = datetime.today()
    else:
        today = g_ForceDate
    theDatePath = f'{g_basePath}{str(today.date())}_Output'

    for foldername, subfolders, filenames in os.walk(theDatePath):
        for filename in filenames:
            if "竖版" not in filename:
                continue
            if "主力资金概念榜" in filename and "归一化" not in filename:
                continue
            file_path = os.path.join(foldername, filename)
            print(f'to upload {file_path}')
            app = Uploader()
            asyncio.run(app.main(file_path))
            time.sleep(600)
    
    # file_path = theDatePath + '2023-11-23 主力资金概念榜 如有其他指标需求请留言_主力资金流入流出榜 以概念板块为单位_竖版.mp4'


if __name__ == '__main__':
    main()