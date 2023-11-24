import asyncio
from playwright.async_api import Playwright, async_playwright
import time
from ConstText import *
from ConstURLs import *
from Utils import *
from datetime import datetime
from XG_Uploader import *
from DY_Uploader import *
import os

c_DataPath = r'd:\\Dailys'
g_ForceDate = None
g_ForceDate = datetime(2023,11,23)

def main():    
    today = None
    if g_ForceDate is None:
        today = datetime.today()
    else:
        today = g_ForceDate
    theDatePath = os.path.join(c_DataPath,f'{str(today.date())}_Output')
    portrait_paths = []
    landscape_paths = []
    for foldername, subfolders, filenames in os.walk(theDatePath):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            if "竖" in filename:
                portrait_paths.append(file_path)
            else:
                landscape_paths.append(file_path)
    
    p_cnt = len(portrait_paths)
    l_cnt = len(landscape_paths)

    if p_cnt==l_cnt:
        for i in range(0,p_cnt):
            # p_path = portrait_paths[i]
            # print(f'to upload {p_path}')
            # dy_app = DY_Uploader(c_DataPath)
            # asyncio.run(dy_app.main(p_path))

            # time.sleep(20)

            l_path = landscape_paths[i]
            print(f'to upload {l_path}')
            xg_app = XG_Uploader(c_DataPath)
            asyncio.run(xg_app.main(l_path))

            time.sleep(20)

if __name__ == '__main__':
    main()