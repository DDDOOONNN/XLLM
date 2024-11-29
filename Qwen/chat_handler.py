# chat_handler.py

import logging
import time
from openai import OpenAI  # 修改了导入方式
from image_encoder import encode_image  # 假设有一个图片编码模块

# 修改 OpenAI 的 API key 和 API base 以使用 vLLM 的 API 服务器。
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8900/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 指定模型路径
model_path = "/data/rjn/Qwen2-VL-7B-Instruct"

model = "/data/rjn/Qwen2-VL-7B-Instruct"  # 确保模型名称与服务端一致


def initialize_chat(system_message, role="system"):
    """
    初始化聊天会话。
    """
    try:
        history = [
            {
                "role": role,
                "content": system_message,
            }
        ]
        return history
    except Exception as e:
        logging.error(f"初始化聊天会话失败: {e}")
        raise e


def send_message(chat_session, message, role="user", inline_image=None):
    """
    发送消息到聊天会话并返回响应。
    """
    try:
        # 构建用户消息
        if inline_image:
            # 如果提供了图片，编码为 Base64 或直接使用路径
            image_data_uri = encode_image(inline_image)  # 确保返回的是正确的 data URI 或路径
            user_message = {
                "role": role,
                "content": [
                    {
                        "type": "text",
                        "text": message
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_uri
                        }
                    }
                ],
            }
        else:
            # 仅发送文本消息
            user_message = {
                "role": role,
                "content": message,
            }

        # 将用户消息添加到会话历史
        chat_session.append(user_message)

        # 调用 vLLM 的 chat completion 接口
        chat_completion = client.chat.completions.create(
            model=model,
            messages=chat_session,
            temperature=0.5,
            max_tokens=256,  # 限制返回的最大 Token 数量
        )

        # 从响应中提取助手的回复
        response = chat_completion.choices[0].message.content.strip()

        # 将助手的消息添加到会话历史
        chat_session.append({
            "role": "assistant",
            "content": response,
        })

        # 返回助手的响应文本
        return response

    except Exception as e:
        logging.error(f"发送消息时出错: {e}")
        return f"错误: {e}"


def send_message_with_retry(chat_session, message, role="user", inline_image=None, retries=3, delay=5):
    """
    发送消息并在失败时重试。
    """
    for attempt in range(1, retries + 1):
        response = send_message(chat_session, message, role, inline_image)
        if not response.startswith("错误:") and not response.startswith("Error:"):
            return response  # 成功返回结果
        else:
            logging.warning(f"尝试 {attempt} 失败，错误: {response}")
            if attempt < retries:
                logging.info(f"{delay} 秒后重试...")
                time.sleep(delay)
            else:
                logging.error("所有重试尝试均失败。")
                return response

    time.sleep(2)


if __name__ == "__main__":
    # 初始化聊天会话
    chat_history = initialize_chat("You are a helpful assistant.")

    # 发送文本消息
    response = send_message(chat_history, "Hello, how are you?")
    print("Response:", response)

    # 发送包含图片的消息
    image_path = "/home/xxxy/hh/RJN/xllm/Qwen/test.JPG"
    response_with_image = send_message(chat_history, "What is in this image?", inline_image=image_path)
    print("Response with image:", response_with_image)