# LLaMA Assistant
Set of scripts for llama.cpp that provide different usefulf assistants scenarios/templates.

## Assistants
- chatbot.sh - Generic chat
- prompt-engineer - Creating prompts for Stable Diffusion
- email.sh - Helping writing formal emails

## Prepare
Download model and put it in the /models/ folder. Recommendeed models from [WizardVinunaLM](https://github.com/melodysdreamj/WizardVicunaLM):
- [Wizard-Vicuna-13B-Uncensored.ggmlv3.q5_K_M.bin](https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GGML/resolve/main/Wizard-Vicuna-13B-Uncensored.ggmlv3.q5_K_M.bin) 9.21GB

## Usage
```
./chatbot.sh
```

First run will take a while as it needs to create cache file. Be patient.
