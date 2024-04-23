import json
from src.model.modelLlama3 import ModelLlama3


class Hanabi:
    def __init__(self, model, systemPromptLocation: str, chatHistoryLocation=None):
        self.model = model
        self.systemPromptLocation = systemPromptLocation
        self.chatHistoryLocation = chatHistoryLocation
        self.chatMemoryLimit = 10
        self.chatHistory = []
        self.customSystemPrompt = None
        self.customUserPrompt = None

        self.loadModel()
        self.loadJsonFile()

    def loadModel(self):
        self.chatbot = ModelLlama3(self.model)

    def loadChatHistory(self):
        history = self.chatHistory

        if self.chatHistoryLocation is not None:
            for line in self.localChatHistory:
                history.append(line)

        if len(history) > self.chatMemoryLimit:
            history = history[-self.chatMemoryLimit :]
        return history

    def saveChatHistory(self, role: str, response: str):
        chat = {"role": role, "content": response}

        self.chatHistory.append(chat)

    def loadJsonFile(self):
        if self.systemPromptLocation is None:
            raise Exception("System prompt location not found")
        with open(self.systemPromptLocation, "r") as file:
            bruteText = file.read()
            self.systemPrompt = {"role": "system", "content": bruteText}

        if self.chatHistoryLocation is not None:
            with open(self.chatHistoryLocation, "r") as file:
                bruteText = file.read()
                self.localChatHistory = json.loads(bruteText)

    def useChatHistoryCustom(self, history):
        customHistory = []

        roleUser = []
        roleAssistant = []

        for line in history:
            roleUser.append({"role": "user", "content": line[0]})
            roleAssistant.append({"role": "assistant", "content": line[1]})

        if len(history) > 10:
            roleUser = roleUser[-8:]
            roleAssistant = roleAssistant[-2:]

        for i, chatUser in enumerate(roleUser):

            customHistory.append(chatUser)

            differecence = len(roleUser) - len(roleAssistant)

            if i >= differecence:
                customHistory.append(roleAssistant[i - differecence])

        return customHistory

    def mountPrompt(self, question: str, historyCustom=None) -> str:
        history = self.loadChatHistory()

        if historyCustom is not None:
            history = self.useChatHistoryCustom(historyCustom)

        prompt = []

        if self.customSystemPrompt is not None:
            prompt.append({"role": "system", "content": self.customSystemPrompt})
        else:
            prompt.append(self.systemPrompt)

        if self.customUserPrompt is not None:
            prompt.append({"role": "user", "content": self.customUserPrompt})

        for chat in history:
            prompt.append(chat)

        questionPrompt = {"role": "user", "content": question}

        prompt.append(questionPrompt)

        return prompt

    def getNewResponse(self, question: str, history=None) -> str:
        prompt = self.mountPrompt(question, history)

        self.saveChatHistory("user", question)

        response = self.chatbot.getResponse(prompt)

        self.saveChatHistory("assistant", response)

        return response
