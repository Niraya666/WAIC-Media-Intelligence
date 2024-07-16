import re
import json

def read_txt_to_str(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def segment_text_by_reports(text, threshold=300):
    # 定义报告开始和结束的关键词
    start_keywords = ["有请", "接下来有请"]
    end_keywords = ["谢谢", "以上是我的报告", "谢谢大家"]

    # 生成正则表达式
    start_pattern = re.compile("|".join(start_keywords))
    end_pattern = re.compile("|".join(end_keywords))
    
    # 用于存储每个报告的分段文本
    segments = []
    
    # 追踪当前位置和当前报告的文本内容
    current_position = 0
    current_report = []
    
    # 分割文本为句子，并移除空行
    sentences = [s.strip() for s in re.split(r'(?<=[。！？\n])', text) if s.strip()]
    
    for sentence in sentences:
        if start_pattern.search(sentence):
            if current_report:
                segments.append("".join(current_report))
                current_report = []
            current_report.append(sentence)
        elif end_pattern.search(sentence):
            current_report.append(sentence)
            segments.append("".join(current_report))
            current_report = []
        else:
            current_report.append(sentence)
    
    # 处理可能遗留的最后一段
    if current_report:
        segments.append("".join(current_report))

    # 合并长度小于阈值的段落
    merged_segments = []
    skip_next = False
    for i, segment in enumerate(segments):
        if skip_next:
            skip_next = False
            continue
        if len(segment) < threshold and i + 1 < len(segments):
            merged_segments.append(segment + segments[i + 1])
            skip_next = True
        else:
            merged_segments.append(segment)
    
    return merged_segments

if __name__ == '__main__':
    stt_result_path = "../data/STT_manuscripts/4f67d56860d84bac9b9d2eb3c3bd89d9/STT_results.txt"

    text= read_txt_to_str(stt_result_path)

    print(len(text))

    segments = segment_text_by_reports(text)

    # 打印分割结果
    for i, segment in enumerate(segments):
        print(f"报告 {i+1}:\n{segment}\n")
        print(len(segment))
        

    with open('../data/STT_manuscripts/4f67d56860d84bac9b9d2eb3c3bd89d9/segments.json', 'w', encoding='utf-8') as file:
        json.dump(segments, file, ensure_ascii=False, indent=4)