import gradio as gr

from src.Hanabi import Hanabi

class Interface:
    def __init__(self, systemPromptLocation: str):
        self._interface = None
        self.model = Hanabi("meta-llama/Meta-Llama-3-8B-Instruct", systemPromptLocation)
        # self.model = Hanabi("meta-llama/Meta-Llama-3-70B-Instruct", systemPromptLocation)

    def textProcessing(self, text, history, systemPrompt, userPrompt):
        self.model.customSystemPrompt = None
        self.model.customUserPrompt = None
        
        if systemPrompt != "":
            self.model.customSystemPrompt = systemPrompt
        
        if userPrompt != "":
            self.model.customUserPrompt = userPrompt       
        response = self.model.getNewResponse(text, history)
        return response

    def run(self):
        additional_inputs = [
            gr.Textbox("", label="System Prompt"),
            gr.Textbox("", label="User Prompt"),
        ]
        gr.ChatInterface(self.textProcessing, additional_inputs=additional_inputs).launch(server_name="0.0.0.0")
