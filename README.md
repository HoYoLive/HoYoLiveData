# HoYoLiveData
 HoYoLive 数据存放

## 仓库结构

```
[database]
├─ [yaoyao]
|   ├─ [2022]
|   |   ├─ [02]
|   |   |   ├─ subtitle1.srt
|   |   |   └─  ...
|   |   ├─ [03]
|   |   ├─ ...
|   |   ├─ main.json
|   |   └─ search.json
|   └─ main.json
├─ file.py
├─ main.json
└─ requirements.txt
```

### database 下的文件

#### `file.py`与`requirements.txt`
用于归档的 python 脚本及其依赖，push 前运行 `file.py`。
- 生成 *character* -> *year* 文件夹下的 `main.json` 与 `search.json`
- 若存在`.srt`字幕文件，但未填写对应录播的来源，则提示上传录播
- 若已填写录播的来源，但未存在对应`.srt`字幕文件，则提示无字幕文件

#### `main.json`

字典结构。
`character`键对应值为储存所有角色名(`string`)的数组，如`["yaoyao"]`。
例：
```json
{
    "character": ["yaoyao"]
}
```

### database -> *character* 下的文件

#### `main.json`

字典结构。
`years`键对应值为储存所有年份(`number`)的数组，如`[2022]`。
例：
```json
{
    "years": [2022]
}
```

### database -> *character* -> *year* 下的文件

#### `main.json` (由`file.py`生成)

列表结构。<a id="mainjson"></a>
储存当前年份所有直播的主要信息。
例：
```json
[
    {
        "date": "22-02-04",     // 日期: yy-mm-dd
        "time": "19:01",        // 开始时间: hh:mm
        "source": "acfun",      // 来源平台: acfun, bilibili
        "video": "ac33486236",  // 来源平台的视频地址标识
        "p": 1,                 // 位于该视频投稿的第几部分
        "type": ["chat"],       // 类型: chat, game, paint, song
        "title": "杳杳首播",     // 直播/录播标题
        "srt": "ac33486236"     // 不带文件拓展名的字幕文件名(.srt格式)
    },
    ...
]
```

#### `search.json` (由`file.py`生成)

字典结构。
储存当前年份所有直播的字幕文本，不带文件拓展名的字幕文件名(键)对应字幕文本内容(值)，句间存在空格。
例：
```json
{
    "2022-03-27 14-00-56_audio_index1": "啊欢迎大家下午好呀 因为因为...",
    ...
}

```

### database -> *character* -> *year* -> *month* 下的文件

#### `main.json` (人工标注)

储存当前月份所有直播的主要信息，其余同上`main.json`，但内容为人工标注。

#### `search.json` (由`file.py`生成)

储存当前月份所有直播的字幕文本，其余同上`search.json`。

## 如何添加新数据

### 下载录播文件

方法1：索取官方的obs录播文件，一般为MKV格式，包含多轨音频。

方法2：以 AcFun 平台为例，通过 [AcFun 助手](https://github.com/niuchaobo/acfun-helper) 等浏览器插件获取录播投稿的 `.m3u8` 地址。安装 [ffmpeg](https://ffmpeg.org/download.html) 后通过以下命令下载视频文件。

```
ffmpeg -i https://videoAddress.m3u8 -c copy -bsf:a aac_adtstoasc fileName.mp4
```

方法3：以 AcFun 平台为例，通过 [acfunlive](https://github.com/orzogc/acfunlive) 等开源项目下载直播视频。

### 生成字幕文件

下载 [剪映专业版](https://lv.ulikecam.com/) ，使用其内置的智能字幕完成 `.srt` 格式字幕文件的生成。

1. 启动剪映专业版。
2. 点击 开始创作。
3. 拖入录播文件至时间轴。若单个文件长度大于2小时，请在大约1小时位置分割(ctrl+B)文件，并确保分割的时间点没有被切断的人声。
4. 依次点击 文本 -> 智能字幕 -> 识别字幕(开始识别)。
5. 等待字幕识别完成。
6. 点击右上角的导出，更改“作品名称”与“保存至”，并勾选字幕导出。

**字幕文件名规则**

为确保字幕文件名不重复以避免不必要的错误发生，字幕文件的命名一般遵循以下规则：

- 若视频来源为obs录播文件或其提取音轨，则与媒体文件同名，如：
```
2022-04-05 19-01-19_audio_index1.srt
2022-04-16 14-02-21_audio_index1.srt
```

- 若视频来源为视频网站下载，则与网址中的唯一标识同名，如：
```
ac33707890.srt
ac33708835_1.srt
ac33708835_5.srt
```

### 归档

1. 将导出的字幕文件放到 database -> *character* -> *year* -> *month* -> srt 文件夹下。
2. 按照 [main.json的格式](#mainjson) 更新 database -> *character* -> *year* -> *month* -> main.json 文件。
3. 运行如下命令，完成最后的归档操作：

```
cd database
python file.py
```