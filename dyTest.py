import asyncio
from playwright.async_api import Playwright, async_playwright
import time
from ConstText import *
from ConstURLs import *
from Utils import *
from datetime import datetime
from DY_Uploader import *
import os

c_DataPath = r'd:\\Dailys'
g_ForceDate = None

def main():    
    today = None
    if g_ForceDate is None:
        today = datetime.today()
    else:
        today = g_ForceDate
    theDatePath = os.path.join(c_DataPath,f'{str(today.date())}_Output')
    for foldername, subfolders, filenames in os.walk(theDatePath):
        for filename in filenames:
            if "竖版" not in filename:
                continue
            file_path = os.path.join(foldername, filename)
            print(f'to upload {file_path}')
            app = DY_Uploader(c_DataPath)
            asyncio.run(app.main(file_path))
            break
            time.sleep(600)
    
    # file_path = theDatePath + '2023-11-23 主力资金概念榜 如有其他指标需求请留言_主力资金流入流出榜 以概念板块为单位_竖版.mp4'


if __name__ == '__main__':
    main()