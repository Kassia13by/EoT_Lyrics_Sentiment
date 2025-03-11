"""
主要函數：包含 API 呼叫、文字處理和 EOT 分析過程。
"""
import time
import re
import openai
from collections import Counter
from config import role_descriptions, roles, OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

# 設定 OpenAI API 金鑰
openai.api_key = OPENAI_API_KEY

def generate_response(prompt, system_prompt):
    """呼叫 OpenAI API 生成回答"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model= MODEL_NAME,  # 可根據需要替換成其他模型
            messages=messages,
            temperature= TEMPERATURE
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return ""

def extract_numeric(response_text):
    """
    利用正則表達式從回答文字中抽取獨立出現的 0 或 1。
    即使回答中包含詳細說明，也只取其中獨立出現的數字。
    若有多個數字，取最後一個作為該角色的最終判斷。
    """
    matches = re.findall(r'\b[01]\b', response_text)
    if matches:
        return matches[-1]  # 取最後一個數字
    else:
        return None


def eot_processes(lyric, max_iterations=3):
    """
    針對單一歌詞進行情緒分析，並記錄：
      - 每個角色的初始提示、回答與抽取的數字
      - 每一輪迭代時的提示、回答與抽取的數字
      - 每輪抽取數字情況、收斂檢查與最終決策過程（存放在 discussion_log 中）
    回傳：
      final_numeric: 最終決策的數字標籤（0 或 1）
      role_results: 各角色詳細紀錄的字典
      discussion_log: 整體討論過程的記錄（列表形式）
    """
    discussion_log = []  # 用來記錄全局討論日誌
    role_results = {}    # 記錄每個角色的詳細討論內容
    responses = {}       # 當前回覆存放

    # 初始提示與各角色的初始回答
    initial_prompt = (
        f"Please analyze the sentiment of the following lyrics, discussing your view in detail. "
        f"However, at the end of your answer, please provide an isolated number for lyrics sentiment: 0 for negative, 1 for positive.\n\n{lyric}"
    )
    discussion_log.append("【Initial Response】")
    for role in roles:
        initial_response = generate_response(initial_prompt, role_descriptions[role])
        extracted = extract_numeric(initial_response)
        role_results[role] = {
            "initial": {
                "prompt": initial_prompt,
                "response": initial_response,
                "extracted_number": extracted
            },
            "iterations": []  # 後續記錄每輪的更新回答
        }
        responses[role] = initial_response
        discussion_log.append(f"{role}'s initial answer extracted number: {extracted}")
        time.sleep(1)

    # 多輪記憶討論，最多 max_iterations 輪
    iteration = 0
    converged = False
    while iteration < max_iterations and not converged:
        discussion_log.append(f"【Memory Round {iteration+1}】")
        new_responses = {}
        # 每個角色依據上一輪所有角色的回答（初始或上一次迭代）來生成新的回答
        for role in roles:
            # 組合所有角色的上一輪回答
            all_responses = []
            for r in roles:
                all_responses.append(f"{r}'s answer:\n{responses[r]}")
            responses_text = "\n\n".join(all_responses)
            
            # 調試輸出：印出目前組合好的所有角色回答
            print(f"\nIteration {iteration+1} - {role}'s turn. Combined responses from all roles:\n{responses_text}\n")
            
            iter_prompt = (
                f"Please refer to the clearly marked answers of all experts below (including your own previous answer) and update your own sentiment analysis accordingly.\n\n"
                f"{responses_text}\n\n"
                f"Please analyze the sentiment of the following lyrics again, discussing your view in detail, but at the end provide an isolated number for lyrics sentiment: 0 for negative, 1 for positive.\n\n{lyric}"
            )
            iter_response = generate_response(iter_prompt, role_descriptions[role])
            iter_extracted = extract_numeric(iter_response)
            # 將本輪資訊記錄到該角色的迭代列表中
            role_results[role]["iterations"].append({
                "round": iteration + 1,
                "prompt": iter_prompt,
                "response": iter_response,
                "extracted_number": iter_extracted
            })
            new_responses[role] = iter_response

        # 印出這一輪各角色抽取到的數字
        extracted_numbers = {role: extract_numeric(new_responses[role]) for role in roles}
        discussion_log.append(f"Iteration {iteration+1} extracted numbers: {extracted_numbers}")
        print(f"Iteration {iteration+1} extracted numbers: {extracted_numbers}")

        # 若所有角色抽取的數字一致則視為收斂
        if len(set(extracted_numbers.values())) == 1:
            converged = True
            final_numeric = list(set(extracted_numbers.values()))[0]
            discussion_log.append(f"Convergence achieved on iteration {iteration+1}: All extracted numbers converged to {final_numeric}.")
            print(f"Converged at iteration {iteration+1}: {final_numeric}")
        else:
            responses = new_responses  # 更新所有角色的回答，用於下一輪迭代
            iteration += 1
            time.sleep(1)

    # 若多輪後仍未收斂，以每個角色最新回答中的數字作為決策依據
    final_numeric_list = []
    for role in roles:
        if role_results[role]["iterations"]:
            num = role_results[role]["iterations"][-1]["extracted_number"]
        else:
            num = role_results[role]["initial"]["extracted_number"]
        if num is not None:
            final_numeric_list.append(num)
        else:
            discussion_log.append(f"{role}'s answer did not contain an extractable number. Response: {responses[role]}")

    discussion_log.append(f"Final extracted numbers before voting: {final_numeric_list}")
    print(f"Final extracted numbers before voting: {final_numeric_list}")

    # 多數決決策：若超過半數角色持相同數字則選此數字，否則預設 Amy 的回答
    counter = Counter(final_numeric_list)
    most_common = counter.most_common(1)
    if most_common and most_common[0][1] > 1:
        final_numeric = most_common[0][0]
        discussion_log.append(f"Majority vote selected final answer: {final_numeric}")
        print(f"Final decision by majority vote: {final_numeric}")
    else:
        final_numeric = extract_numeric(responses["Amy"]) or "Unable to determine"
        discussion_log.append(f"No majority vote, defaulting to Amy's answer: {final_numeric}")
        print(f"No majority vote, defaulting to Amy's answer: {final_numeric}")

    return final_numeric, role_results, discussion_log
