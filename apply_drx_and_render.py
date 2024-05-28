"""

这个脚本会把你给定的文件夹的所有视频导入一条时间线，并且应用一个LUT，然后分段渲染到指定的文件夹 。

1. 安装python3 和 pycharm
2. 安装davinci resolve studio版本
3. 设置davinci resolve 脚本项
4. 保存你常用的drx静帧文件
5. 设置转码预设

"""

from python_get_resolve import GetResolve
import os
import sys
import time

# —————————— 在此区域设置你的参数 ——————————

projectName = "20240527PythonTest"  # 请替换为你的项目名称
framerate = "25"  # 帧率
width = "1920"  # 宽度
height = "1080"  # 高度
gradeMode = 0  # 调色模式 gradeMode : 0 - “No keyframes”, 1 - “Source Timecode aligned”, 2 - “Start Frames aligned”.
renderPresetName = "proxy_1080p"  # 渲染预设名称（注意，默认的转码预设不支持文件名为“源名称”，可以在davinci中修改预设，然后在这里输入你的预设名称）
mediaPath = "/Volumes/极浪B1_2T/20240522Python渲染测试/01原始素材/A001"  # 媒体文件夹路径
outputPath = "/Volumes/极浪B1_2T/20240522Python渲染测试/02代理素材"  # 输出文件夹路径
drxPath = "/Volumes/极浪B1_2T/20240522Python渲染测试/03静帧/极浪-Slog3cineTo709.drx"  # 静帧路径



# —————————— 这里是筛选的文件拓展名列表 如果没有可以增加自己的 ——————————

# 支持的媒体文件扩展名列表
supported_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.mxf']
timelineName = os.path.basename(mediaPath)  # 获取mediaPath的文件夹名称作为时间线名称
outputPath = os.path.join(outputPath, timelineName)  # 输出文件夹后面添加时间线名称（卷名）

# —————————— 程序区域  ——————————

# 检查媒体路径是否存在

def fetchMediaFiles(path, supported_extensions):
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"路径 {path} 不存在。")
        return False

    mediaFiles = []

    # 遍历路径下所有文件和文件夹
    for root, dirs, files in os.walk(path):
        # 筛选出媒体文件
        mediaFiles.extend(
            [os.path.join(root, file) for file in files if os.path.splitext(file)[1].lower() in supported_extensions])

    # 如果存在媒体文件，打印文件数目并返回文件列表
    if mediaFiles:
        print(f"找到{len(mediaFiles)}个媒体文件，开始启动达芬奇。")
        return mediaFiles

    else:
        print(f"在路径 {path} 下没有找到媒体文件。")
        return False


def AddTimelineToRender(project, timeline, presetName, targetDirectory):
    # 定义一个函数，将时间线添加到渲染
    project.SetCurrentTimeline(timeline)  # 设置当前时间线
    project.LoadRenderPreset(presetName)  # 加载渲染预设（预设名称）
    # project.SetCurrentRenderMode(0)  # 设置渲染模式，0 - Individual clips 多个单独片段, 1 - Single clip 单个片段
    project.SetRenderSettings({"SelectAllFrames": 1, "TargetDir": targetDirectory})  # 把渲染设置为所有帧，目标目录为targetDirectory
    return project.AddRenderJob()  # 返回添加渲染作业（的对象）


def RenderAllTimelines(resolve, presetName, targetDirectory):
    # 定义一个函数 渲染所有时间线
    projectManager = resolve.GetProjectManager()  # 获取项目管理器
    project = projectManager.GetCurrentProject()  # 获取当前项目
    if not project:  # 如果没有获取当前项目 返回False
        return False

    resolve.OpenPage("Deliver")  # 打开交付页面
    timelineCount = project.GetTimelineCount()  # 获取时间线数量

    for index in range(0, int(timelineCount)):  # 遍历时间线数量，从0到时间线数量
        if not AddTimelineToRender(project, project.GetTimelineByIndex(index + 1), presetName,
                                   targetDirectory, ):  # 调用addTimelineToRender函数，如果没有添加时间线到渲染 返回False
            return False
    return project.StartRendering()  # 返回开始渲染


def IsRenderingInProgress(resolve):
    # 定义一个函数，查看渲染是否在进行中
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    return project.IsRenderingInProgress()  # 返回项目正在渲染中


def WaitForRenderingCompletion(resolve):
    # 定义一个函数，等待渲染完成，当渲染正在进行时，等待1秒。
    while IsRenderingInProgress(resolve):
        time.sleep(1)
    return


def ApplyDRXToAllTimelineClips(timeline, path, gradeMode=0):
    # 定义一个函数，用来将drx文件中的静帧应用到时间线的所有片段。
    trackCount = timeline.GetTrackCount("video")  # 获取视频轨道数量

    for index in range(1, int(trackCount) + 1):  # 遍历视频轨道数量
        clips = timeline.GetItemListInTrack("video", index)  # 获取视频轨道中的所有片段
        if not timeline.ApplyGradeFromDRX(path, int(gradeMode), clips):  # 如果没有将静帧应用到所有片段 返回False
            return False

    return True


def ApplyDRXToAllTimelines(resolve, path, gradeMode=0):
    # 定义一个函数，将drx文件中的静帧应用到所有时间线中。
    projectManager = resolve.GetProjectManager()  # 获取项目管理器
    project = projectManager.GetCurrentProject()  # 获取当前项目
    if not project:  # 如果没有获取当前项目 返回False
        print('没有获取当前项目')
        return False
    timelineCount = project.GetTimelineCount()  # 获取时间线数量

    for index in range(0, int(timelineCount)):  # 遍历时间线数量，对每一条时间线都调用ApplyDRXToAllTimelineClips函数
        timeline = project.GetTimelineByIndex(index + 1)  # 因为时间线的index是从1开始的，所以这里+1
        project.SetCurrentTimeline(timeline)  # 设置当前时间线
        if not ApplyDRXToAllTimelineClips(timeline, path, gradeMode):  # 如果没有将静帧应用到所有片段 返回False
            print('没有将静帧应用到所有片段')
            return False
    return True


# 主程序

# 步骤1:调用函数检查媒体文件
mediaFiles = fetchMediaFiles(mediaPath, supported_extensions)


# 步骤2:创建项目并设置参数
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.LoadProject(projectName)
if not project:
    project = projectManager.CreateProject(projectName)
    print(f'未能找到名为"{projectName}"的项目，已创建新项目')

# 设定项目帧率、 分辨率
project.SetSetting("timelineFrameRate", str(framerate))
project.SetSetting("timelineResolutionWidth", str(width))
project.SetSetting("timelineResolutionHeight", str(height))

# 步骤3:将文件夹内容添加到媒体池
mediapool = project.GetMediaPool()
rootFolder = mediapool.GetRootFolder()
mediapool.AddSubFolder(rootFolder, timelineName)
clips = mediapool.ImportMedia(mediaFiles)

# 步骤4:创建时间线

timeline = mediapool.CreateEmptyTimeline(timelineName)
if not timeline:
    mediapool.CreateTimeline(f"{timelineName}1")
    print("无法创建时间线 '" + timelineName + "'")
    sys.exit()

# 按名称排序
clips = sorted(clips, key=lambda clip: clip.GetClipProperty("File Name"))

# 定义需要排除的文件扩展名列表
for clip in clips:
    mediapool.AppendToTimeline(clip)

# 把drx文件应用到所有时间线

if not ApplyDRXToAllTimelines(resolve, drxPath, gradeMode):
    print("不能把drx静帧应用到所有时间线")
    sys.exit()

if not RenderAllTimelines(resolve, renderPresetName, outputPath):
    print("渲染所有时间线时出错")
    sys.exit()

WaitForRenderingCompletion(resolve)

print("渲染完成")
