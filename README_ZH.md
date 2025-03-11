# 歌詞情感分析專案

這個專案使用多個 AI 角色作為不同的專家（以 OpenAI GPT 模型為例），通過 Exchange of Thought, EOT 方法分析歌詞的情感。
其方法參考論文[Exchange-of-Thought: Enhancing Large Language Model Capabilities through Cross-Model Communication](https://aclanthology.org/2023.emnlp-main.936/)

## 專案結構

- `main.py`: 主程式，用於運行分析
- `functions.py`: 包含 API 呼叫、文字處理和 EOT 分析等主要函數
- `config.py`: 包含 API 金鑰、角色描述等配置設定
- `requirements.txt`: 專案套件版本需求
- `README.md`: 專案說明文件

## 設定

1. 安裝: 安裝所需套件版本

   ```
   pip install -r requirements.txt
   ```

2. 設定 API 金鑰:
   - 方法一：在 `config.py` 中直接更新 API 金鑰
   - 方法二 (建議)：設定環境變數 `OPENAI_API_KEY` （已於 `config.py` 中註解）
     ```
     # Linux/Mac
     export OPENAI_API_KEY="你的API金鑰"
     
     # Windows
     set OPENAI_API_KEY=你的API金鑰
     ```

3. 準備包含歌詞資料的輸入 CSV 檔案。（本專案例子之 `lyrics.csv` 檔案中包含一個 `lyrics` 欄，15 個歌詞段落列）

## 使用方法

執行主程式:

```
python main.py
```

程式將:
1. 從輸入的 CSV 檔案讀取歌詞
2. 通過 EOT 情感分析系統處理每一歌詞段落
3. 結果和討論記錄寫入新的 lyrics_with_eot.json 檔案

## 方法說明

EOT 過程的工作原理（僅使用 **Memory** 交流方式）:
1. 讓三個專家角色（Amy, Lily 和 John）獨立分析歌詞情感
2. 接著三者將分享他們的觀點並在多次迭代中取得分析結果
3. 本專案預設最多為 3 次迭代，若提前達成答案之一致性則提前終止迭代
4. 若 3 次後仍未達成一次則採多數決
5. 若無法多數決則預設採用 Amy 的答案
3. 最終情感標籤將達成一致（0 表示負面，1 表示正面情緒）

## 使用修改小提示

你可以修改:
- `config.py` 中的角色描述
- `config.py` 中的 API 參數
- `config.py` 中的 模型 參數
- `main.py` 中的輸入/輸出檔案路徑
- `main.py` 中 EOT 過程的迭代次數

