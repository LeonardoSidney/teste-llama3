from src.Hanabi import Hanabi
from src.tools.Interface import Interface

def main():
    systemPromptLocation = "/src/prompts/systemPrompt.txt"

    interface = Interface(systemPromptLocation)
    interface.run()


if __name__ == "__main__":
    main()