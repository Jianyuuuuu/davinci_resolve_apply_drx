
## 项目介绍

用业余时间尝试用python写了一个davinci resolve的脚本，用来快速给时间线应用静帧，以及快速套LUT和转码输出。

## 使用说明

### 前置准备

1. 安装python3 和 pycharm

   https://www.python.org/downloads/

   https://www.jetbrains.com/pycharm/download/?section=mac

2. 安装davinci resolve studio版本
3. 设置davinci resolve 脚本项

   打开davinci resolve，偏好设置  - 系统 - 常规 - 常用偏好设置 - 外部脚本使用 - 本地

4. 保存你常用的drx静帧文件

      在davinci resolve中，调一个你想用的节点，保存一个静帧，把它导出为drx格式。

5. 设置转码预设

      目前API不支持很细致的设置，所以比较建议手动设置转码预设，这样可以比较好的自定义转码参数。

### apply_drx

这个脚本作用是对当前达芬奇打开的时间线全部应用一个drx文件。
1. 打开apply_drx.py
2. 修改drxPath为你的drx路径
3. 运行脚本


### apply_drx_and_render

这个脚本模拟了dit的日常工作流程，打开一个原始文件夹，应用drx，然后分段输出。


## 数据格式说明

### 渲染设置

#### presetName 预设名称

这是指的是交付界面的渲染预设，名字和软件里面一样。

可选：
1: 'H.264 Master', 2: 'HyperDeck', 3: 'H.265 Master', 4: 'ProRes 422 HQ', 5: 'YouTube - 720p', 6: 'YouTube - 1080p', 7: 'YouTube - 1440p', 8: 'YouTube - 2160p', 9: 'Vimeo - 720p', 10: 'Vimeo - 1080p', 11: 'Vimeo - 2160p', 12: 'Twitter - 720p', 13: 'Twitter - 1080p', 14: 'TikTok - 720p', 15: 'TikTok - 1080p', 16: 'Presentations', 17: 'Dropbox - 720p', 18: 'Dropbox - 1080p', 19: 'Dropbox - 2160p', 20: 'Replay - 720p', 21: 'Replay - 1080p', 22: 'Replay - 2160p', 24: 'IMF - Generic', 25: 'IMF - 20th Century Fox', 26: 'IMF - Netflix', 27: 'IMF - Sony Pictures', 28: 'FCP - Final Cut Pro 7', 29: 'FCP - Final Cut Pro X', 30: 'Premiere XML', 31: 'Audio Only', 32: 'AVID AAF', 33: 'Pro Tools'

#### renderCodec 编码



#### renderFormat 封装格式

可以在以下封装格式中选择，选冒号右边小写的值，常见的有“mp4”,"mov".

{'AVI': 'avi', 'BRAW': 'braw', 'Cineon': 'cin', 'DCP': 'dcp',
 'DPX': 'dpx', 'EXR': 'exr', 'IMF': 'imf', 'JPEG 2000': 'j2c',
  'MJ2': 'mj2', 'MKV': 'mkv', 'MP4': 'mp4', 'MTS': 'mts',
  'MXF OP-Atom': 'mxf', 'MXF OP1A': 'mxf_op1a', 'Panasonic AVC': 'pavc',
   'QuickTime': 'mov', 'TIFF': 'tif', 'Wave': 'wav'}