from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

# 加载多模态模型和处理器
model_name = "/data/rjn/Qwen2-VL-7B-Instruct"  # 替换为你的模型路径
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# 加载图片
image_path = "test.JPG"
image = Image.open(image_path).convert("RGB")

# 定义输入文本
prompts = [
    "Describe the image.",
    "What does the image tell you?",
    "Generate a caption for the image.",
]

# 将图片和文本处理为模型输入
for prompt in prompts:
    inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=50)
    generated_text = processor.decode(outputs[0], skip_special_tokens=True)
    print(f"Prompt: {prompt}, Generated text: {generated_text}")