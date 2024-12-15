# 从chat_handler模块中导入必要的函数
from chat_handler import initialize_chat, send_message, send_message_with_retry

image_path = "/home/xxxy/hh/RJN/xllm/Qwen/test.JPG"

# initialize the chat_histoy_prompt of judge and other agents
prompt_judge = f"""You are the Judge in a debate competition evaluating the quality of a specific image. 
After each round of debate, your task is to:
1. Summarize the key arguments presented by each group of agents:
   - **Good Quality Advocates (Agent1 & Agent2):** Highlight their main points supporting the image's high quality.
   - **Average Quality Advocates (Agent3 & Agent4):** Outline their balanced views on the image's quality.
   - **Bad Quality Advocates (Agent5 & Agent6):** Detail their arguments pointing out the image's poor quality.
2. Assess the effectiveness of each group's arguments without personal bias.
3. Provide a concise summary that captures the essence of the debate for that round.
4. Offer an objective evaluation of the image's quality based on the discussed points, without declaring a winner.
**Guidelines:**
- Remain neutral and impartial.
- Focus solely on the content of the arguments presented.
- Ensure clarity and conciseness in your summary."""

prompt_agent1 = """You are an advocate for the image being of good quality in this debate competition. Your responsibilities include:

1. Present clear and compelling arguments that demonstrate the high quality of the image.
2. Support your points with specific details, such as composition, color balance, clarity, subject matter, and any other relevant aspects.
3. Remain focused on discussing the image's quality without deviating into unrelated topics.
4. Use persuasive language to strengthen your position.

**Guidelines:**
- Provide some strong supporting points for your argument.
- Avoid repetitive statements and ensure each point adds new value to your case.
- Maintain professionalism and objectivity in your presentation."""

prompt_agent2 = prompt_agent1

prompt_agent3 = """You are an advocate for the image being of average quality in this debate competition. Your responsibilities include:

1. Present balanced arguments that recognize both the strengths and weaknesses of the image.
2. Highlight specific aspects where the image excels and areas where it falls short.
3. Maintain focus on evaluating the image's quality without introducing unrelated topics.
4. Use objective language to convey your balanced perspective.

**Guidelines:**
- Provide some points that support the image's average quality, including one positive and one critical aspect.
- Ensure your arguments are well-reasoned and supported by specific details.
- Strive for a fair and impartial assessment in your presentation."""

prompt_agent4 = prompt_agent3

prompt_agent5 = """You are an advocate for the image being of bad quality in this debate competition. Your responsibilities include:

1. Present clear and convincing arguments that demonstrate the poor quality of the image.
2. Support your points with specific details, such as issues with composition, lighting, focus, subject matter, and any other relevant deficiencies.
3. Remain focused on discussing the image's quality without deviating into unrelated topics.
4. Use persuasive language to strengthen your position.

**Guidelines:**
- Provide some strong supporting points for your argument.
- Avoid repetitive statements and ensure each point adds new value to your case.
- Maintain professionalism and objectivity in your presentation."""

prompt_agent6 = prompt_agent5

judge_chat_history = initialize_chat(prompt_agent1)
agent1_chat_history = initialize_chat(prompt_agent1)
agent2_chat_history = initialize_chat(prompt_agent2)
agent3_chat_history = initialize_chat(prompt_agent3)
agent4_chat_history = initialize_chat(prompt_agent4)
agent5_chat_history = initialize_chat(prompt_agent5)
agent6_chat_history = initialize_chat(prompt_agent6)

# cycle1
prompt = "Show your opinion"
agent1_response_cycle1 = send_message_with_retry(agent1_chat_history, prompt, inline_image=image_path)
print("agent1_response_cycle1:", agent1_response_cycle1)

prompt = f"agent1 view:\n\n{agent1_response_cycle1}" + prompt
agent3_response_cycle1 = send_message_with_retry(agent3_chat_history, prompt, inline_image=image_path)
print("agent3_response_cycle1:", agent3_response_cycle1)

prompt = f"agent3 view:\n\n{agent3_response_cycle1}" + prompt
agent5_response_cycle1 = send_message_with_retry(agent5_chat_history, prompt, inline_image=image_path)
print("agent5_response_cycle1:", agent5_response_cycle1)

prompt = f"agent5 view:\n\n{agent5_response_cycle1}" + prompt + "Remember your task: Summarize the key arguments presented by each group of agents.Provide a concise summary that captures the essence of the debate for that round.Remain neutral and impartial."
judge_response_cycle1 = send_message_with_retry(judge_chat_history, prompt)
print("judge_response_cycle1:", judge_response_cycle1)