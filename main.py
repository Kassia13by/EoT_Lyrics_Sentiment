"""
主程式：處理 .csv 檔案輸入、.json 輸出及呼叫函數。
"""
import csv
import json
from functions import eot_processes
from config import roles

def main():
    """
    主要功能：從 CSV 檔案讀取歌詞，進行情感分析，並將結果寫入新的 CSV 檔案。
    """

    # CSV 檔案路徑設定（請依據實際情況調整檔案路徑）
    input_csv = "./lyrics.csv"  
    output_json = "./lyrics_with_eot.json"

    results = []  # 用來存放所有輸出的 JSON 物件

    with open(input_csv, "r", encoding="utf-8") as csvfile_in:
        reader = csv.reader(csvfile_in)
        # 假設 CSV 第一行為 header，如果有 header，可以視情況跳過
        header = next(reader)
        
        for row in reader:
            lyric = row[0]  # 根據實際 CSV 格式調整索引
            print(f"Processing lyric (first 30 chars): {lyric[:30]}...")
            final_numeric, role_results, discussion_log = eot_processes(lyric, max_iterations=3)
            
            output_dict = {
                "lyric": lyric,
                "roles": role_results,
                "final_decision": final_numeric,
                "discussion_log": discussion_log
            }
            results.append(output_dict)
            print(f"Final label: {final_numeric}\n")

    with open(output_json, "w", encoding="utf-8") as json_out:
        json.dump(results, json_out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()