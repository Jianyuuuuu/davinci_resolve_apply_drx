#!/usr/bin/env python

"""

这是一个简单的脚本，用来快速应用一个drx给当前时间线的所有片段。

"""

from python_get_resolve import GetResolve # 只导入GetResolve函数，如此调用不需要加前缀
import sys
import time


# 输入参数区域

drxPath = "/Volumes/极浪B1_2T/20240522Python渲染测试/03静帧/极浪-无调色.drx"  # 在这里输入drx文件的路径
gradeMode = 0 # 可选 0 / 1 / 2 ，默认为0


# ——————————————————————分割线——————————————————————


def ApplyDRXToAllTimelineClips(timeline, path, gradeMode=0):
    # 定义一个函数，用来将drx文件中的静帧应用到时间线的所有片段。
    trackCount = timeline.GetTrackCount("video")  # 获取视频轨道数量

    for index in range(1, int(trackCount) + 1):  # 遍历视频轨道数量
        clips = timeline.GetItemListInTrack("video", index)  # 获取视频轨道中的所有片段
        if not timeline.ApplyGradeFromDRX(path, int(gradeMode), clips):  # 如果没有将静帧应用到所有片段 返回False
            return False

    return True


# 主程序


# 获取现在打开的项目，获取当前时间线
resolve = GetResolve()
timeline = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline()

ApplyDRXToAllTimelineClips(timeline, drxPath, gradeMode)  # 将drx静帧应用到所有时间线

print("已经把drx静帧应用到当前时间线的所有片段")
