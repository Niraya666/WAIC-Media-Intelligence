import requests
import os
import json
from config import page_headers
def fetch_forum_info(forum_id,page_headers):
    sub_page_info_url_base = "https://api2024.worldaic.com.cn/waic-portal/onLineForum/queryOnLineForum/"
    page_info_url = sub_page_info_url_base + forum_id


    response = requests.get(page_info_url, headers=page_headers)

    if response.status_code == 200:
        useful_info = extract_useful_info(response.text)
        return useful_info
    else:
        print(f"Failed to fetch forum info. Status code: {response.status_code}")
        return None

def extract_useful_info(response_text):
    data = json.loads(response_text).get('data', {})
    # print(data)
    result = {
        'name': data.get('name', ''),
        'addr': data.get('addr', ''),
        'coverImgUrl': data.get('coverImgUrl', ''),
        'desc': data.get('desc', ''),
        'chinaVideoUrl480pCh': data.get('chinaVideoUrl480pCh', ''),
        'chinaVideoUrl720pCh': data.get('chinaVideoUrl720pCh', ''),
        'scheduleInfoList': [],
        'guestVisitList': []
    }

    # 增加判断，如果scheduleInfoList不存在，则跳过循环
    if 'scheduleInfoList' in data and data['scheduleInfoList'] is not None:
        for schedule in data.get('scheduleInfoList', []):
            result['scheduleInfoList'].append({
                'startTime': schedule.get('startTime', ''),
                'endTime': schedule.get('endTime', ''),
                'speechGuest': schedule.get('speechGuest', ''),
                'speechTheme': schedule.get('speechTheme', '')
            })

    # 增加判断，如果guestVisitList不存在，则跳过循环
    if 'guestVisitList' in data and data['guestVisitList'] is not None:
        for guest in data.get('guestVisitList', []):
            result['guestVisitList'].append({
                'name': guest.get('name', ''),
                'company': guest.get('company', ''),
                'position': guest.get('position', '')
            })

    return result

def save_forum_info_to_file(forum_info, forum_id):
    # 构建文件夹路径
    folder_path = 'forum_info/' + forum_id + '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 构建文件路径
    file_path = os.path.join(folder_path, f'{forum_id}.json')

    # 将信息保存为json文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(forum_info, file, ensure_ascii=False, indent=4)
    print(f"Forum info saved to {file_path}")

if __name__ == '__main__':
    forum_id = "ad3060f7f1ac495c833494547a7541e9"
    forum_info = fetch_forum_info(forum_id,page_headers)
    if forum_info:
        save_forum_info_to_file(forum_info, forum_id)   