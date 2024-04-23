from accelerate import Accelerator
import transformers
import torch
from typing import List

class ModelLlama3:
    def __init__(self, model: str):
        self.modelName = model.split("/")[-1]

        self.verifyModel()
        self.loadModel()
        self.createTerminators()

    def verifyModel(self):
        if self.modelName == "Meta-Llama-3-8B-Instruct":
            self.model = "meta-llama/Meta-Llama-3-8B-Instruct"
            return True
        
        if self.modelName == "Meta-Llama-3-70B-Instruct":
            self.model = "meta-llama/Meta-Llama-3-70B-Instruct"
            return True

        raise Exception("Model not found")
        
    def loadModel(self):
        accelerator = Accelerator()
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=accelerator.device,
        )
        self.pipeline.model = accelerator.prepare(self.pipeline.model)

    def createTerminators(self):
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

    def getResponse(self, prompt: List[{str}]):
        accelerator = Accelerator()
        prompt = self.pipeline.tokenizer.apply_chat_template(
            prompt, tokenize=False, add_generation_prompt=True
        )

        with accelerator.autocast():
            outputs = self.pipeline(
                prompt,
                max_new_tokens=2048,
                eos_token_id=self.terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
        
        text = outputs[0]["generated_text"][len(prompt) :]
        
        return text
