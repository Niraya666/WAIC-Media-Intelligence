# WAIC 视频下载+AI总结
（2024年版）
本项目旨在帮助您下载WAIC（世界人工智能大会）的论坛视频，获取基本信息，并进行视频音频转换。
即使您未注册大会，之后也会陆续提供了相关文字稿。

## 视频下载，基本信息获取， 视频音频转换

如果想要下载视频，需要注册大会，并从网页中获得对应的Cokies 和token；
如果没有注册也没有关系， 因为我已经将这些视频整理成文字稿，存放在了[文稿](/data/STT_manuscripts/)


如果您已注册会议，想要下载视频：

已将所有支持回看的论坛，爬取并保存成一个json文件,于->[all_data](/data/basic/all_data.json)

### 环境配置

1. 安装Python及所需依赖：
    ```sh
    pip install -r requirements.txt
    ```

2. 安装`ffmpeg`：
    ```sh
    # 例如在macOS上使用Homebrew安装：
    brew install ffmpeg
    ```

### 获取headers

下载视频需要两个headers，一个用于视频下载（video_headers），一个用于网页信息获取（page_headers）。

#### 获取video_headers

1. 打开一个论坛视频，按`F12`打开开发者工具。
2. 点击`Network`，找到`mudu.js`。
3. 点击`Headers`，复制`Request Headers`中的`Cookie`。

修改`config.py`中的`video_headers`，替换对应的`Cookie`：

```python
# 设置请求头
video_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '[replace_by_your_Cookie]',
    'Host': 'pull0109ise.mudu.tv',
    'Referer': 'https://online2024.worldaic.com.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}
```

#### 获取page_headers

1. 找到`queryOnLineForum`，查看其`Request Headers`。
2. 复制`token`并替换`config.py`中的`token`。

```python
page_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "api2024.worldaic.com.cn",
    "Origin": "https://online2024.worldaic.com.cn",
    "Pragma": "no-cache",
    "Referer": "https://online2024.worldaic.com.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "token": "[replace_by_your_token]"
}
```


### 下载视频

执行以下命令下载视频，并保存基本信息（json）、视频（mp4）和音频文件（wav）：

```sh
python download_video.py
```

### 结果示例

下载后的视频及相关文件将按如下格式存放：

```
uuid/
    uuid.json
    uuid.mp4
    uuid.wav
```