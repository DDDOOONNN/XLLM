from chat_handler import initialize_chat, send_message_with_retry, delete_last_message
import os
from prompt_discussion import (
    prompt_Judge,
    prompt_Participant1,
    prompt_Participant2,
    prompt_Participant3,
    prompt_Participant4
)


# Path to the image
image_path = "/home/xxxy/hh/RJN/xllm/Qwen/test.JPG"

# Initialize chat sessions for judge and participants
chat_judge = initialize_chat(prompt_Judge)
chat_p1 = initialize_chat(prompt_Participant1)
chat_p2 = initialize_chat(prompt_Participant2)
chat_p3 = initialize_chat(prompt_Participant3)
chat_p4 = initialize_chat(prompt_Participant4)

# Path to the image directory
image_folder = "/data/IQA-Dataset/BID/ImageDatabase"

image_files = sorted(
    [os.path.join(image_folder, file)
     for file in os.listdir(image_folder)
     if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
)

# ====================================================
# Round 1
# ====================================================

prompt_p1 = "This is round 1. Please share your opinion about the overall quality of the image. "
response_p1 = send_message_with_retry(chat_p1, prompt_p1, inline_image=image_path)
print("\nP1:\n\n" + response_p1)

prompt_p2 = "This is round 1. Please share your opinion about the overall quality of the image. "
response_p2 = send_message_with_retry(chat_p2, prompt_p2, inline_image=image_path)
print("\nP2:\n\n" + response_p2)

prompt_p3 = "This is round 1. Please share your opinion about the overall quality of the image."
response_p3 = send_message_with_retry(chat_p3, prompt_p3, inline_image=image_path)
print("\nP3:\n\n" + response_p3)

prompt_p4 = "This is round 1. Please share your opinion about the overall quality of the image."
response_p4 = send_message_with_retry(chat_p4, prompt_p4, inline_image=image_path)
print("\nP4:\n\n" + response_p4)



# Judge summarizes Round 1
prompt_judge = (
    "In the first round, your role is to:\n\n"
    "1. **Evaluate each participant's response** by highlighting the relevance and quality of their points. Create a separate summary for each participant's analysis, focusing on the key observations and insights they provided about the image's quality. Ignore any scores or numerical values mentioned in the participants' responses.\n"
    "2. **Provide a general summary** that synthesizes the collective insights from all participants into a cohesive overview. This summary should focus on the overall analysis of the image's quality based on the participants' comments. Avoid attributing specific points to individual participants in this section and keep the summary open-ended. Do not include any suggestions for improvement.\n\n"
    "**Output Format:**\n\n"
    "- **Participant Summaries:**\n"
    "  - **Participant 1:**\n"
    "    [Write a concise summary of participant 1's response here.]\n"
    "  - **Participant 2:**\n"
    "    [Write a concise summary of participant 2's response here.]\n"
    "  - **Participant 3:**\n"
    "    [Write a concise summary of participant 3's response here.]\n"
    "- **Participant 4:**\n"
    "    [Write a concise summary of participant 4's response here.]\n\n"
    "- **General Summary:**\n"
    "  [Write the general summary here, focusing on collective insights from all participants.]\n\n"
    "**Input:**\n"
    f"- This is the result from participant 1: `{response_p1}`\n"
    f"- This is the result from participant 2: `{response_p2}`\n"
    f"- This is the result from participant 3: `{response_p3}`\n"
    f"- This is the result from participant 4: `{response_p4}`\n\n"
)
response_judge = send_message_with_retry(chat_judge, prompt_judge)
print("\nJudge:\n\n" + response_judge)


# ====================================================
# Round 2
# ====================================================


# Prepare system messages with judge's summary from Round 1

prompt_p1_system = f"This is the summary of round 1 from the judge of the discussion: {response_judge}."
prompt_p2_system = f"This is the summary of round 1 from the judge of the discussion: {response_judge}."
prompt_p3_system = f"This is the summary of round 1 from the judge of the discussion: {response_judge}."
prompt_p4_system = f"This is the summary of round 1 from the judge of the discussion: {response_judge}."

send_message_with_retry(chat_p1, prompt_p1_system, role="system")
send_message_with_retry(chat_p2, prompt_p2_system, role="system")
send_message_with_retry(chat_p3, prompt_p3_system, role="system")
send_message_with_retry(chat_p4, prompt_p4_system, role="system")



prompt_p1 = "This is round 2. Please share your opinion about the local quality of the image."
response_p1 = send_message_with_retry(chat_p1, prompt_p1)
print("\nP1:\n\n" + response_p1)

prompt_p2 = "This is round 2. Please share your opinion about the local quality of the image."
response_p2 = send_message_with_retry(chat_p2, prompt_p2)
print("\nP2:\n\n" + response_p2)

prompt_p3 = "This is round 2. Please share your opinion about the local quality of the image."
response_p3 = send_message_with_retry(chat_p3, prompt_p3)
print("\nP3:\n\n" + response_p3)

prompt_p4 = "This is round 2. Please share your opinion about the local quality of the image."
response_p4 = send_message_with_retry(chat_p4, prompt_p4)
print("\nP4:\n\n" + response_p4)


# Judge summarizes Round 2

prompt_judge = (
    "In the second round, your role is to:\n\n"
    "1. **Evaluate each participant's response** by highlighting the relevance and quality of their points regarding the image's local quality. Create a separate summary for each participant's analysis, focusing on the key observations and insights they provided. Ignore any scores or numerical values mentioned in the participants' responses.\n"
    "2. **Provide a general summary** that synthesizes the collective insights from all participants into a cohesive overview. This summary should focus on the overall analysis of the image's local quality based on the participants' comments. Avoid attributing specific points to individual participants in this section and keep the summary open-ended. Do not include any suggestions for improvement.\n\n"
    "**Output Format:**\n\n"
    "- **Participant Summaries:**\n"
    "  - **Participant 1:**\n"
    "    [Write a concise summary of participant 1's response here.]\n"
    "  - **Participant 2:**\n"
    "    [Write a concise summary of participant 2's response here.]\n"
    "  - **Participant 3:**\n"
    "    [Write a concise summary of participant 3's response here.]\n"
    "- **Participant 4:**\n"
    "    [Write a concise summary of participant 4's response here.]\n\n"
    "- **General Summary:**\n"
    "  [Write the general summary here, focusing on collective insights from all participants.]\n\n"
    "**Input:**\n"
    f"- This is the result from participant 1: `{response_p1}`\n"
    f"- This is the result from participant 2: `{response_p2}`\n"
    f"- This is the result from participant 3: `{response_p3}`\n"
    f"- This is the result from participant 4: `{response_p4}`\n\n"
)
response_judge = send_message_with_retry(chat_judge, prompt_judge)
print("\nJudge:\n\n" + response_judge)



# ====================================================
# Round 3
# ====================================================


# Prepare system messages with judge's summary from Round 2

prompt_p1_system_r2 = f"This is the summary of round 2 from the judge of the discussion: {response_judge}."
prompt_p2_system_r2 = f"This is the summary of round 2 from the judge of the discussion: {response_judge}."
prompt_p3_system_r2 = f"This is the summary of round 2 from the judge of the discussion: {response_judge}."
prompt_p4_system_r2 = f"This is the summary of round 2 from the judge of the discussion: {response_judge}."

send_message_with_retry(chat_p1, prompt_p1_system_r2, role="system")
send_message_with_retry(chat_p2, prompt_p2_system_r2, role="system")
send_message_with_retry(chat_p3, prompt_p3_system_r2, role="system")
send_message_with_retry(chat_p4, prompt_p4_system_r2, role="system")



prompt_p1 = (
    "This is round 3. Please provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
)
response_p1 = send_message_with_retry(chat_p1, prompt_p1)
print("\nP1:\n\n" + response_p1)

prompt_p2 = (
    "This is round 3. Please provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
)
response_p2 = send_message_with_retry(chat_p2, prompt_p2)
print("\nP2:\n\n" + response_p2)

prompt_p3 = (
    "This is round 3. Please provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
)
response_p3 = send_message_with_retry(chat_p3, prompt_p3)
print("\nP3:\n\n" + response_p3)

prompt_p4 = (
    "This is round 3. Please provide your final assessment of the image's quality along with the discussion process and provide a final score out of 100."
)
response_p4 = send_message_with_retry(chat_p4, prompt_p4)
print("\nP4:\n\n" + response_p4)


# Judge summarizes Round 3
prompt_judge = (
    "In the final round, your role is to:\n\n"
    "1. **Summarize the collective insights** about the image's quality based on the final analyses provided by the participants. Your summary should be detailed and comprehensive, combining the key points from all responses into a cohesive overview that reflects shared observations and general trends. Focus only on the content provided in the final round and ignore any incomplete or unclear responses. Do not attribute specific points to individual participants or create separate summaries for each response.\n"
    "2. **Extract and calculate the average score** provided by the participants in the final round (out of 100). Identify the numerical scores explicitly mentioned in the participants' responses. If a participant does not provide a numerical score, exclude their input from the calculation. Include the formula used for the calculation in your response.\n\n"
    "**Output Format:**\n\n"
    "- **Final Summary:**\n"
    "  [Write the detailed and comprehensive summary here based on the collective insights.]\n\n"
    "- **Average Score:**\n"
    "  1. Extracted Scores:\n"
    "     - Participant 1: [Extracted score or \"No score provided\"]\n"
    "     - Participant 2: [Extracted score or \"No score provided\"]\n"
    "     - Participant 3: [Extracted score or \"No score provided\"]\n"
    "     - Participant 4: [Extracted score or \"No score provided\"]\n"
    "  2. Formula: `(score1 + score2 + score3 + score4) / number of participants who provided scores = average score`\n"
    "  3. Average Score: [Calculate the average score here.]\n\n"
    "**Input:**\n"
    f"- This is the result from participant 1: `{response_p1}`\n"
    f"- This is the result from participant 2: `{response_p2}`\n"
    f"- This is the result from participant 3: `{response_p3}`\n"
    f"- This is the result from participant 4: `{response_p4}`\n\n"
)
response_judge = send_message_with_retry(chat_judge, prompt_judge)
print("\nJudge:\n\n" + response_judge)


# ====================================================
# End of Discussion
# ====================================================
