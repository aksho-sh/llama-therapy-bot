from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_model():
    global model, tokenizer
    config = PeftConfig.from_pretrained("aksho-sh/Llama-3.1-8b-finetuned")
    base_model = AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        load_in_4bit=True,
        device_map="auto"
    )
    model = PeftModel.from_pretrained(base_model, "aksho-sh/Llama-3.1-8b-finetuned")
    tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

@app.get("/generate")
async def generate(input_text: str):
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Input:
    {}

    ### Response:
    {}"""


    inputs = tokenizer([alpaca_prompt.format(
        "Give mental therapy advise to the following input. Give the advise in a more conversational way as a human therapist would.",
        input_text, "")], return_tensors="pt").to("cuda")

    outputs = model.generate(**inputs, max_new_tokens=500, use_cache=True, eos_token_id=tokenizer.eos_token_id)
    raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    cleaned_response = clean_model_output(raw_response)

    return {"response": cleaned_response}

def clean_model_output(output_text):
    if "### Response:" in output_text:
        cleaned_text = output_text.split("### Response:")[-1].strip()
    else:
        cleaned_text = output_text.strip()

    return cleaned_text
