# LLaMA Assistant
Set of scripts for llama.cpp that provide different usefulf assistants scenarios/templates.

## Assistants
- email.sh - eMailWriter - chat bot shadow writing formal emails for the user
- prompt-engineer.sh - PromptEngineer - chat bot for creating prompts for Stable Diffusion
- chatbot.sh - P1XBOT - a generic chat bot with frendly vibe

## Prepare
Download model and put it in the /models/ folder. Recommendeed models from [WizardVinunaLM](https://github.com/melodysdreamj/WizardVicunaLM):
- [Wizard-Vicuna-13B-Uncensored.ggmlv3.q5_K_M.bin](https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GGML/resolve/main/Wizard-Vicuna-13B-Uncensored.ggmlv3.q5_K_M.bin) 9.21GB

## Usage
```
./chatbot.sh
```

First run will take a while as it needs to create cache file. Be patient.
