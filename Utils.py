import os

c_TestPath = 'D:\\Dailys\\2023-11-21_Output\\2020-11-21 归一化主力资金概念榜 (除以总流通市值)_竖版_主力资金概念榜 资金量除以流通市值来归一化.mp4'

def filePath_Infos(filePath):
    file_name = os.path.basename(filePath)
    results = file_name.split('_')
    title = results[0]
    screen_mode = results[2]
    desc_info = results[1]
    return title,screen_mode,desc_info

def testMain():
    t,s,d = filePath_Infos(c_TestPath)
    print(t)
    print(s)
    print(d)

if __name__ == '__main__':
    testMain()