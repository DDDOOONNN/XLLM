import os
import pandas as pd
from tqdm import tqdm  # 用于显示进度条
from chat_handler import (
    initialize_chat,
    send_message,
    send_message_with_retry,
    delete_last_message
)
from prompt_discussion import (
    prompt_Judge,
    prompt_Participant1,
    prompt_Participant2,
    prompt_Participant3,
    prompt_Participant4
)

# 函数：记录每张图片的分析结果为字典
def record_image_analysis(image_name, responses):
    data = {'Image': image_name}
    for idx, response in enumerate(responses, start=1):
        data[f'Response_{idx}'] = response
    return data

# 设置图片文件夹路径
image_folder = "/data/IQA-Dataset/BID/ImageDatabase"

# 获取所有图片文件的路径，并按文件名排序
image_files = sorted(
    [os.path.join(image_folder, file)
     for file in os.listdir(image_folder)
     if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
)

# 将图片分组，每组最多 50 张
batch_size = 50
image_batches = [image_files[i:i + batch_size] for i in range(0, len(image_files), batch_size)]

# 遍历每组图片
for batch_index, image_batch in enumerate(image_batches, start=1):
    # Excel 文件名
    output_excel_path = f'dialogue_results_part{batch_index}.xlsx'
    
    # 初始化一个列表，用于存储当前批次所有图片的分析结果
    final_data = []
    
    # 遍历当前批次的图片
    for image_path in tqdm(image_batch, desc=f"Processing Batch {batch_index}"):
        image_name_with_ext = os.path.basename(image_path)
        image_name, _ = os.path.splitext(image_name_with_ext)  # 去掉扩展名
        
        # 初始化聊天会话
        chat_judge = initialize_chat(prompt_Judge)
        chat_p1 = initialize_chat(prompt_Participant1)
        chat_p2 = initialize_chat(prompt_Participant2)
        chat_p3 = initialize_chat(prompt_Participant3)
        chat_p4 = initialize_chat(prompt_Participant4)
        
        # 用于存储当前图片的所有响应
        image_responses = []
        
        try:
            # ====================================================
            # Round 1
            # ====================================================
            round_num = 1
            
            # Step 1 in Round 1: Think by themselves
            step = 1
            
            # Participant 1
            prompt_p1 = "This is round 1, please show your opinion about the overall quality of the image."
            try:
                response_p1 = send_message_with_retry(chat_p1, prompt_p1, inline_image=image_path)
            except Exception as e:
                response_p1 = f"Error: {e}"
            print(f"P1:\n\n{response_p1}")
            image_responses.append(response_p1)
            
            # Participant 2
            prompt_p2 = "This is round 1, Please show your opinion about the overall quality of the image."
            try:
                response_p2 = send_message_with_retry(chat_p2, prompt_p2, inline_image=image_path)
            except Exception as e:
                response_p2 = f"Error: {e}"
            print(f"P2:\n\n{response_p2}")
            image_responses.append(response_p2)
            
            # Participant 3
            prompt_p3 = ("This is round 1, Please show your opinion about the overall quality of the image. "
                         "Assess the image's overall quality with a tendency to highlight positive aspects.")
            try:
                response_p3 = send_message_with_retry(chat_p3, prompt_p3, inline_image=image_path)
            except Exception as e:
                response_p3 = f"Error: {e}"
            print(f"P3:\n\n{response_p3}")
            image_responses.append(response_p3)
            
            # Participant 4
            prompt_p4 = ("This is round 1, Please show your opinion about the overall quality of the image. "
                         "Assess the image's overall quality with a tendency to highlight negative aspects.")
            try:
                response_p4 = send_message_with_retry(chat_p4, prompt_p4, inline_image=image_path)
            except Exception as e:
                response_p4 = f"Error: {e}"
            print(f"P4:\n\n{response_p4}")
            image_responses.append(response_p4)
            
            # Judge Summary Step 1
            prompt_judge = (
                f"This is step {step} in round {round_num}, they have not discussed with others. "
                f"Now complete your task in round {round_num}. If they offer scores, do not pay attention to that. "
                f"Give a brief summary of each one's ideas and then give an overall summary.\n\n"
                f"This is the result from participant 1: {response_p1}\n\n\n"
                f"This is the result from participant 2: {response_p2}\n\n\n"
                f"This is the result from participant 3: {response_p3}\n\n\n"
                f"This is the result from participant 4: {response_p4}\n\n\n."
            )
            try:
                response_judge = send_message_with_retry(chat_judge, prompt_judge)
            except Exception as e:
                response_judge = f"Error: {e}"
            print(f"Judge:\n\n{response_judge}")
            image_responses.append(response_judge)
            
            # Step 2 in Round 1: Discussion with each other
            step = 2
            
            # Participant 1 Discussion
            prompt_p1_discuss = f"""
            This is a summary of the thoughts of the other participants in the first round and the judge {round_num} : \n
            {response_judge}
            \n\n\n\
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the overall quality of the image.
            """
            try:
                response_p1_discuss = send_message_with_retry(chat_p1, prompt_p1_discuss)
            except Exception as e:
                response_p1_discuss = f"Error: {e}"
            print(f"P1:\n\n{response_p1_discuss}")
            image_responses.append(response_p1_discuss)
            
            # Participant 2 Discussion
            prompt_p2_discuss = f"""
            This is a summary of the thoughts of the other participants in the first round and the judge {round_num} : \n
            {response_judge}
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the overall quality of the image.
            """
            try:
                response_p2_discuss = send_message_with_retry(chat_p2, prompt_p2_discuss)
            except Exception as e:
                response_p2_discuss = f"Error: {e}"
            print(f"P2:\n\n{response_p2_discuss}")
            image_responses.append(response_p2_discuss)
            
            # Participant 3 Discussion
            prompt_p3_discuss = f"""
            This is a summary of the thoughts of the other participants in the first round and the judge {round_num} : \n
            {response_judge}
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the overall quality of the image.Remember that You have a slight bias towards rating the image as higher quality.
            """
            try:
                response_p3_discuss = send_message_with_retry(chat_p3, prompt_p3_discuss)
            except Exception as e:
                response_p3_discuss = f"Error: {e}"
            print(f"P3:\n\n{response_p3_discuss}")
            image_responses.append(response_p3_discuss)
            
            # Participant 4 Discussion
            prompt_p4_discuss = f"""
            This is a summary of the thoughts of the other participants in the first round and the judge {round_num} : \n
            {response_judge}
            You can express your opinion, you can agree with them, or you can stand by your opinion. In short, express your thoughts about the overall quality of the image. Remember that you have a slight bias towards rating the image as lower quality.
            """
            try:
                response_p4_discuss = send_message_with_retry(chat_p4, prompt_p4_discuss)
            except Exception as e:
                response_p4_discuss = f"Error: {e}"
            print(f"P4:\n\n{response_p4_discuss}")
            image_responses.append(response_p4_discuss)
            
            # Judge Summary Step 2
            prompt_judge_step2 = f"""
            This is step {step} in round {round_num}, they have discussed with each other. 
            Now complete your task in the round {round_num}. 
            If they offer scores, do not pay attention to that. 
            Give a brief summary of each one's ideas and then give an overall summary.\n\n
            This is the result from participant 1: {response_p1_discuss}\n\n\n\
            this is the result from participant 2: {response_p2_discuss}\n\n\n\
            this is the result from participant 3: {response_p3_discuss}\n\n\n\
            this is the result from participant 4: {response_p4_discuss}\n\n\n.
            """
            try:
                response_judge_step2 = send_message_with_retry(chat_judge, prompt_judge_step2)
            except Exception as e:
                response_judge_step2 = f"Error: {e}"
            print(f"Judge:\n\n{response_judge_step2}")
            image_responses.append(response_judge_step2)
            
            # 清理会话
            delete_last_message(chat_p1)
            delete_last_message(chat_p2)
            delete_last_message(chat_p3)
            delete_last_message(chat_p4)
            
            # ====================================================
            # Round 2
            # ====================================================
            round_num += 1
            step = 1
            
            # 设置参与者系统信息（Judge的总结）
            system_message = f"This is the summary of round {round_num -1} from the judge of the discussion: {response_judge_step2}."
            try:
                send_message_with_retry(chat_p1, system_message, role="system")
                send_message_with_retry(chat_p2, system_message, role="system")
                send_message_with_retry(chat_p3, system_message, role="system")
                send_message_with_retry(chat_p4, system_message, role="system")
            except Exception as e:
                print(f"Error setting system message for Round {round_num}: {e}")
            
            # Step 1 in Round 2: Think by themselves
            
            # Participant 1 Round 2
            prompt_p1_round2 = "This is round 2, please show your opinion about the local quality of the image."
            try:
                response_p1_round2 = send_message_with_retry(chat_p1, prompt_p1_round2)
            except Exception as e:
                response_p1_round2 = f"Error: {e}"
            print(f"P1 Round 2:\n\n{response_p1_round2}")
            image_responses.append(response_p1_round2)
            
            # Participant 2 Round 2
            prompt_p2_round2 = "This is round 2, Please show your opinion about the local quality of the image."
            try:
                response_p2_round2 = send_message_with_retry(chat_p2, prompt_p2_round2)
            except Exception as e:
                response_p2_round2 = f"Error: {e}"
            print(f"P2 Round 2:\n\n{response_p2_round2}")
            image_responses.append(response_p2_round2)
            
            # Participant 3 Round 2
            prompt_p3_round2 = ("This is round 2, Please show your opinion about the local quality of the image. "
                                "Evaluate specific aspects of the image's quality in detail, emphasizing its strengths.")
            try:
                response_p3_round2 = send_message_with_retry(chat_p3, prompt_p3_round2)
            except Exception as e:
                response_p3_round2 = f"Error: {e}"
            print(f"P3 Round 2:\n\n{response_p3_round2}")
            image_responses.append(response_p3_round2)
            
            # Participant 4 Round 2
            prompt_p4_round2 = ("This is round 2, Please show your opinion about the local quality of the image. "
                                "Evaluate specific aspects of the image's quality in detail, emphasizing its shortcomings.")
            try:
                response_p4_round2 = send_message_with_retry(chat_p4, prompt_p4_round2)
            except Exception as e:
                response_p4_round2 = f"Error: {e}"
            print(f"P4 Round 2:\n\n{response_p4_round2}")
            image_responses.append(response_p4_round2)
            
            # Judge Summary Round 2 Step 1
            prompt_judge_round2_step1 = f"""
            This is step {step} in round {round_num}, they have not discussed with others. 
            Now complete your task in round {round_num}. 
            If they offer scores, do not pay attention to that. 
            Give a brief summary of each one's ideas and then give an overall summary.\n\n
            This is the result from participant 1: {response_p1_round2}\n\n\n\
            This is the result from participant 2: {response_p2_round2}\n\n\n\
            This is the result from participant 3: {response_p3_round2}\n\n\n\
            This is the result from participant 4: {response_p4_round2}\n\n\n.
            """
            try:
                response_judge_round2_step1 = send_message_with_retry(chat_judge, prompt_judge_round2_step1)
            except Exception as e:
                response_judge_round2_step1 = f"Error: {e}"
            print(f"Judge Round 2 Step 1:\n\n{response_judge_round2_step1}")
            image_responses.append(response_judge_round2_step1)
            
            
            
            # Step 2 in Round 2: Discussion with each other
            step = 2
            
            # Participant 1 Discussion Round 2
            prompt_p1_round2_discuss = f"""
            This is a summary of the thoughts of the other participants in the second round and the judge {round_num} : \n
            {response_judge_round2_step1}\n\n\n\
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the local quality of the image.
            """
            try:
                response_p1_round2_discuss = send_message_with_retry(chat_p1, prompt_p1_round2_discuss)
            except Exception as e:
                response_p1_round2_discuss = f"Error: {e}"
            print(f"P1:\n\n{response_p1_round2_discuss}")
            image_responses.append(response_p1_round2_discuss)
            
            # Participant 2 Discussion Round 2
            prompt_p2_round2_discuss = f"""
            This is a summary of the thoughts of the other participants in the second round and the judge {round_num} : \n
            {response_judge_round2_step1}\n\n\n\
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the local quality of the image.
            """
            try:
                response_p2_round2_discuss = send_message_with_retry(chat_p2, prompt_p2_round2_discuss)
            except Exception as e:
                response_p2_round2_discuss = f"Error: {e}"
            print(f"P2:\n\n{response_p2_round2_discuss}")
            image_responses.append(response_p2_round2_discuss)
            
            # Participant 3 Discussion Round 2
            prompt_p3_round2_discuss = f"""
            This is a summary of the thoughts of the other participants in the second round and the judge {round_num} : \n
            {response_judge_round2_step1}\n\n\n\
            You can express your opinion, you can agree with them or you can stand by your opinion, in short, express your thoughts about the local quality of the image.Remember that You have a slight bias towards rating the image as higher quality.
            """
            try:
                response_p3_round2_discuss = send_message_with_retry(chat_p3, prompt_p3_round2_discuss)
            except Exception as e:
                response_p3_round2_discuss = f"Error: {e}"
            print(f"P3:\n\n{response_p3_round2_discuss}")
            image_responses.append(response_p3_round2_discuss)
            
            # Participant 4 Discussion Round 2
            prompt_p4_round2_discuss = f"""
            This is a summary of the thoughts of the other participants in the second round and the judge {round_num} : \n
            {response_judge_round2_step1}\n\n\n\
            You can express your opinion, you can agree with them, or you can stand by your opinion. In short, express your thoughts about the local quality of the image. Remember that you have a slight bias towards rating the image as lower quality.
            """
            try:
                response_p4_round2_discuss = send_message_with_retry(chat_p4, prompt_p4_round2_discuss)
            except Exception as e:
                response_p4_round2_discuss = f"Error: {e}"
            print(f"P4:\n\n{response_p4_round2_discuss}")
            image_responses.append(response_p4_round2_discuss)
            
            # Judge Summary Round 2 Step 2
            prompt_judge_round2_step2 = f"""
            This is step {step} in round {round_num}, they have discussed with each other. 
            Now complete your task in the round {round_num}. 
            If they offer scores, do not pay attention to that. 
            Give a brief summary of each one's ideas and then give an overall summary.\n\n
            This is the result from participant 1: {response_p1_round2_discuss}\n\n\n\
            this is the result from participant 2: {response_p2_round2_discuss}\n\n\n\
            this is the result from participant 3: {response_p3_round2_discuss}\n\n\n\
            this is the result from participant 4: {response_p4_round2_discuss}\n\n\n.
            """
            try:
                response_judge_round2_step2 = send_message_with_retry(chat_judge, prompt_judge_round2_step2)
            except Exception as e:
                response_judge_round2_step2 = f"Error: {e}"
            print(f"Judge:\n\n{response_judge_round2_step2}")
            image_responses.append(response_judge_round2_step2)
            
            # 清理会话
            delete_last_message(chat_p1)
            delete_last_message(chat_p2)
            delete_last_message(chat_p3)
            delete_last_message(chat_p4)
            
            # ====================================================
            # Round 3
            # ====================================================
            round_num += 1
            step = 1
            
            # 设置参与者系统信息（Judge的总结）
            system_message_round3 = f"This is the summary of round {round_num -1} from the judge of the discussion: {response_judge_round2_step2}."
            try:
                send_message_with_retry(chat_p1, system_message_round3, role="system")
                send_message_with_retry(chat_p2, system_message_round3, role="system")
                send_message_with_retry(chat_p3, system_message_round3, role="system")
                send_message_with_retry(chat_p4, system_message_round3, role="system")
            except Exception as e:
                print(f"Error setting system message for Round {round_num}: {e}")
            
            # Step 1 in Round 3: Final Assessment
            # Participant 1 Round 3
            prompt_p1_round3 = "This is round 3, Provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
            try:
                response_p1_round3 = send_message_with_retry(chat_p1, prompt_p1_round3)
            except Exception as e:
                response_p1_round3 = f"Error: {e}"
            print(f"P1 Round 3:\n\n{response_p1_round3}")
            image_responses.append(response_p1_round3)
            
            # Participant 2 Round 3
            prompt_p2_round3 = "This is round 3, Please provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
            try:
                response_p2_round3 = send_message_with_retry(chat_p2, prompt_p2_round3)
            except Exception as e:
                response_p2_round3 = f"Error: {e}"
            print(f"P2 Round 3:\n\n{response_p2_round3}")
            image_responses.append(response_p2_round3)
            
            # Participant 3 Round 3
            prompt_p3_round3 = "This is round 3, Provide your final assessment of the image's quality and assign a score out of 100. You possibly tend to give a slightly higher score."
            try:
                response_p3_round3 = send_message_with_retry(chat_p3, prompt_p3_round3)
            except Exception as e:
                response_p3_round3 = f"Error: {e}"
            print(f"P3 Round 3:\n\n{response_p3_round3}")
            image_responses.append(response_p3_round3)
            
            # Participant 4 Round 3
            prompt_p4_round3 = "This is round 3, Provide your final assessment of the image's quality and assign a score out of 100, possibly favoring a lower score."
            try:
                response_p4_round3 = send_message_with_retry(chat_p4, prompt_p4_round3)
            except Exception as e:
                response_p4_round3 = f"Error: {e}"
            print(f"P4 Round 3:\n\n{response_p4_round3}")
            image_responses.append(response_p4_round3)
            
            # Judge Summary Round 3
            prompt_judge_round3 = f"""
            This is round {round_num}. Now complete your task in round {round_num}. 
            Give a brief overall summary and calculate the average score from all participants.\n\n
            This is the result from participant 1: {response_p1_round3}\n\n\n\
            This is the result from participant 2: {response_p2_round3}\n\n\n\
            This is the result from participant 3: {response_p3_round3}\n\n\n\
            This is the result from participant 4: {response_p4_round3}\n\n\n.
            """
            try:
                response_judge_round3 = send_message_with_retry(chat_judge, prompt_judge_round3)
            except Exception as e:
                response_judge_round3 = f"Error: {e}"
            print(f"Judge:\n\n{response_judge_round3}")
            image_responses.append(response_judge_round3)
            
            
            
            # 将当前图片的分析结果记录下来
            image_analysis = record_image_analysis(image_name, image_responses)
            final_data.append(image_analysis)
        
        except Exception as e:
            print(f"Unexpected error processing image {image_name}: {e}")
            # 记录错误信息
            image_analysis = record_image_analysis(image_name, [f"Unexpected error: {e}"])
            final_data.append(image_analysis)
        
    # 将当前批次的结果写入 Excel 文件
    df_batch = pd.DataFrame(final_data)
    try:
        # 使用 openpyxl 作为 Excel 引擎
        df_batch.to_excel(output_excel_path, index=False, engine='openpyxl')
        print(f"Batch {batch_index} saved to {output_excel_path}")
    except Exception as e:
        print(f"Error saving Batch {batch_index} to Excel: {e}")
    
    # 清空当前批次的数据
    final_data.clear()