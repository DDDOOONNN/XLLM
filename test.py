from vllm import LLM, SamplingParams
import os


os.environ['NCCL_IGNORE_DISABLED_P2P'] = '1'

prompts = [
    "Your name is Davy.",
    "Who are you?",
    "What is your name?",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.5, top_p=0.95, max_tokens=512)
llm = LLM(model="/data/rjn/Qwen2-VL-7B-Instruct", tensor_parallel_size=2)  # you can add tensor_parallel_size=2 to make
# /data/rjn/Qwen2-VL-2B-Instruct
#/data/rjn/llava/llava-1.5-7b-hf


outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

