import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

pipeline_kwargs={
    "temperature": 0.5,
    "max_new_tokens": 8192,
    "top_k": 0.99,
    "top_p": 3

}
  
if __name__ == "__main__":
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        "ura-hcmut/MixSUra-SFT-AWQ",
        device_map="auto"
    )
    model.eval()

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "ura-hcmut/MixSUra-SFT-AWQ",
        trust_remote_code=True
    )
  
    pipeline = transformers.pipeline(
        model=model, 
        tokenizer=tokenizer,
        return_full_text=False,
        task='text-generation',
        **pipeline_kwargs
    )
  
    query_template = "<s> [INST] Bạn là một trợ lý thông minh. Hãy thực hiện các yêu cầu hoặc trả lời câu hỏi từ người dùng bằng tiếng Việt.\n {query}[/INST] "
  
    while True:
        query = input("Query: ")
        if query == "exit":
            break
      
        query = query_template.format(query=query)
        answer = pipeline(query)[0]["generated_text"]
        print(answer)
