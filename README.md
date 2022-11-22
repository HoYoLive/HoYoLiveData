# HoYoLiveData
 HoYoLive 数据存放

## 仓库结构

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

列表结构。
储存当前年份所有直播的主要信息。
例：
```json
[
    {
        "date": "22-02-04",     // 日期: {yy-mm-dd}
        "time": "19:01",        // 开始时间: {hh:mm}
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