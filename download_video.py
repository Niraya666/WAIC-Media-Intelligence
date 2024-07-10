from config import video_headers, page_headers
from utils import fetch_forum_info, extract_useful_info, save_forum_info_to_file
import subprocess
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

import argparse


def download_video(forum_id, video_headers, page_headers):
    headers = video_headers
    forum_info = fetch_forum_info(forum_id, page_headers)
    if not forum_info:
        return
    save_forum_info_to_file(forum_info, forum_id)
    video_url = forum_info.get('chinaVideoUrl480pCh') or forum_info.get('chinaVideoUrl720pCh')
    if not video_url:
        print("No video URL found.")
        return

    # 设置要保存的目录
    save_dir = os.path.join('forum_info', forum_id)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    checkpoint_file = os.path.join(save_dir, 'checkpoint.txt')

    # 读取已下载的文件列表
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            completed_files = set(f.read().splitlines())
    else:
        completed_files = set()



    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(video_url, headers=headers, verify=False)
    response.raise_for_status()
    m3u8_content = response.text

    ts_urls = []
    base_url = os.path.dirname(video_url)
    for line in m3u8_content.split('\n'):
        if line and not line.startswith('#'):
            ts_urls.append(f"{base_url}/{line.strip()}")

    def download_ts(ts_url, i):
        ts_file = os.path.join(save_dir, f'{i}.ts')
        if os.path.basename(ts_file) in completed_files:
            # print(f'Skipped: {ts_file}')
            return ts_file

        try:
            ts_response = session.get(ts_url, headers=headers, verify=False, timeout=10)
            ts_response.raise_for_status()
            with open(ts_file, 'wb') as f:
                f.write(ts_response.content)
            # print(f'Downloaded: {ts_file}')

            with open(checkpoint_file, 'a') as f:
                f.write(f'{os.path.basename(ts_file)}\n')

            return ts_file
        except requests.exceptions.RequestException as e:
            # print(f"Error downloading {ts_url}: {e}")
            return None

    ts_files = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ts = {executor.submit(download_ts, ts_url, i): ts_url for i, ts_url in enumerate(ts_urls)}
        for future in as_completed(future_to_ts):
            ts_file = future.result()
            if ts_file:
                ts_files.append(ts_file)

    output_file = os.path.join(save_dir, f'{forum_id}.mp4')
    with open(output_file, 'wb') as f:
        for i, ts_url in enumerate(ts_urls):
            ts_file = os.path.join(save_dir, f'{i}.ts')
            if os.path.exists(ts_file):
                with open(ts_file, 'rb') as ts_f:
                    f.write(ts_f.read())
                os.remove(ts_file)

    print(f'Video merged and saved as: {output_file}')

    convert_mp4_to_wav(output_file)

def convert_mp4_to_wav(mp4_path):
    if not os.path.exists(mp4_path):
        print(f"File not found: {mp4_path}")
        return

    # 获取文件目录和文件名（不带扩展名）
    dir_name = os.path.dirname(mp4_path)
    base_name = os.path.splitext(os.path.basename(mp4_path))[0]

    # 设置wav文件的路径
    wav_path = os.path.join(dir_name, f"{base_name}.wav")

    # 构建ffmpeg命令
    command = ["ffmpeg", "-i", mp4_path, "-ac", "2", "-ar", "16000", wav_path]

    # 执行命令
    try:
        subprocess.run(command, check=True)
        print(f"Converted {mp4_path} to {wav_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {mp4_path} to WAV: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download video from forum.')
    parser.add_argument('--forum_id', type=str, required=True, help='The forum ID to download the video from.')

    args = parser.parse_args()

    forum_id = args.forum_id
    # forum_id = "ad3060f7f1ac495c833494547a7541e9"

    download_video(forum_id,video_headers, page_headers)

