from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline
import yaml
import torch

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

def load_llm():
    model_name = config["model"]["name"]
    
    print(f"Loading model: {model_name}...")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float32
    )
    
    # Create pipeline with optimized settings
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=config["model"]["max_tokens"],
        temperature=config["model"]["temperature"],
        do_sample=True,  # Enable sampling for better responses
        top_p=0.9,
        repetition_penalty=1.2
    )
    
    print("✅ Model loaded successfully")
    return HuggingFacePipeline(pipeline=pipe)
