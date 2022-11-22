# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 00:29:42 2022

@author: Terry
"""
import os
import json
import srt

def getMainJson(path : str = "."):
    with open(os.path.join(path,"main.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        return j

def fileCharacter(rootPath: str, character: str):
    path = os.path.join(rootPath, character)
    with open(os.path.join(path, "main.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        for y in j["years"]:
            fileByYear(path, y)
            
# 归档某一年的数据
def fileByYear(rootPath: str, year: int):
    path = os.path.join(rootPath, str(year))
    main = []
    for mr in range(1,12):
        m = str(mr).zfill(2)
        m_path = os.path.join(path, m)
        main_path = os.path.join(m_path, "main.json")
        if not os.path.exists(main_path) :continue
        with open(main_path, "r", encoding="utf-8") as mf:
            try:
                mj = json.load(mf)
                main.extend(mj)
            except:
                print("错误: 载入{}失败。".format(main_path))
        createSearchJson(m_path) # 创建每个月的search.json
    with open(os.path.join(path, "main.json"), "w", encoding="utf-8") as yf:
        json.dump(main, yf)
    createSearchJson(path, False) # 创建该年的search.json
    return

def createSearchJson(path:str, warn:bool = True):
    main_path = os.path.join(path, "main.json")
    search_path = os.path.join(path, "search.json")
    search = {}
    with open(main_path, "r", encoding="utf-8") as f:
        try:
            j = json.load(f)
            for x in j:
                if x["srt"] == "": 
                    if warn: 
                        print("【警告】无字幕文件：" 
                              + x["title"] + "：" + x["video"])
                    continue
                srt_path = getFilePath(path, x["srt"] + '.srt')
                if srt_path == "": 
                    print("【错误】未找到字幕文件：" 
                          + x["title"] + "：" + x["video"])
                    continue
                srt_raw = ""
                with open(srt_path, "r", encoding="utf-8") as f:
                    srt_raw = f.read()
                srt_list = list(srt.parse(srt_raw))
                srt_text = " ".join([s.content for s in srt_list])
                search[x["srt"]] = srt_text
                if x["video"] == "" and warn:
                    print("【警告】未上传"+ path + x["title"])
        except:
            print("错误: 通过{}创建字幕失败。".format(main_path))
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search, f)
            
def getFilePath(path:str, srtName:str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == srtName:
                return os.path.join(root, file)
    return ""

if __name__ == "__main__":
    path = "."
    main = getMainJson()
    for c in main["character"]:
        fileCharacter(path, c)
    