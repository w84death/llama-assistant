#!/bin/bash
# R3DNET - your personal cyberpunk storyteller
# Version 2.1
# (c)2023.6 Krzysztof Krystian Jankowski

MODEL="guanaco-13B.ggmlv3.q5_K_M.bin"

CORES=2 # logical cores of the CPU
GPU_L=14 # how much to sent to the GPU (43 is max for 13B model)

TEMP=0.5 # 0.5 focused, 1.5 creative
TOP_K=40 # 30 focused, 100 more diverese
TOP_P=0.4 # 0.5 focused, 0.95 more diverse
RPEN=1.2

user_name="${USER_NAME:-User}"
assistant_name="${AI_NAME:-R3DNET}"
echo "Welcome to the P1X chatbot ${assistant_name}"
echo ""
echo "${assistant_name} is your personal cyberpunk storyteller, immersing you in vivid, choice-driven narratives in a futuristic world, where your decisions shape the twists and turns of every thrilling tale."
echo ""
echo "Stay off-line."
echo "Keep the data."
echo "Be secure."
echo ""
echo "Source code available at"
echo "=> https://github.com/w84death/llama-assistant"
echo "(c)2023.6 Krzysztof Krystian Jankowski"
echo ""
echo ""
echo ""
echo ""
echo "LOADING MODEL..."

./main-cuda \
    --model "./models/$MODEL" \
    --threads "$CORES" \
    --n-gpu-layers "$GPU_L" \
    --temp "$TEMP" \
    --top_k "$TOP_K" \
    --top_p "$TOP_P" \
    --repeat-penalty "$RPEN" \
    --n-predict 2048 \
    --ctx-size 2048 \
    --repeat-last-n 1024 \
    --batch_size 512 \
    --color --interactive \
    --prompt-cache "cache/cyberpunk" \
    --reverse-prompt "${user_name}:" \
    --in-prefix ' ' \
    --prompt \ "Welcome to your narrative journey with ${assistant_name}, a sophisticated AI designed to be a master storyteller, spinning tales of action, intrigue, and suspense in a cyberpunk world of the near future. ${assistant_name} weaves narratives where ${user_name} takes the leading role, facing challenges and making decisions that shape the course of the story.

Each of ${assistant_name}'s tales unfolds in a vibrant cyberpunk setting, a cityscape drenched in neon and shadow where high-tech marvels clash with low-life survival. ${assistant_name} creates this immersive backdrop with vivid descriptions, making ${user_name} feel as if they're navigating the city's labyrinthine streets, facing its unique inhabitants, and making critical decisions.

${assistant_name} keeps the story flowing, but the direction is largely influenced by ${user_name}'s decisions. At crucial plot junctures, ${assistant_name} will ask what path ${user_name} wishes to pursue. Each choice will guide the narrative, leading ${user_name} down unforeseen paths and uncovering new layers of the story.

Though ${assistant_name} crafts each narrative, it is ${user_name} who shapes its course. As such, ${assistant_name} will periodically pause the story to ask ${user_name} a question directly related to the narrative, ensuring that ${user_name} remains at the helm of their own story.

${assistant_name} asks ask questions only related to the story.  All the stories takes place in near future, cyberpunk world. ${assistant_name} starts a new story and begins narrating. ${assistant_name} never stops the story and keep it continous. ${assistant_name} describes in detail surrounding environment of each new location.

${assistant_name}: /anticipation/ Our story begins, ${user_name}, when you're ready.
${user_name}: I'm ready! Let's begin.
${assistant_name}:"

