#!/bin/bash
# eMailWriter - chat bot shadow writing formal emails for the user
# Version 1.0
# (c) 2023 Krzysztof Krystian Jankowski

MODEL="Wizard-Vicuna-13B-Uncensored.ggmlv3.q5_K_M.bin"

CORES=2
GPU_L=14

TEMP=0.7
TOP_K=40
TOP_P=0.1
RPEN=1.1764705882352942

user_name="${USER_NAME:-User}"
assistant_name="${AI_NAME:-eMailWriter}"
echo "Welcome to the Prompt Creator!"
echo "---------------------------"
echo user_name: $user_name
echo assistant_name: $assistant_name
echo "---------------------------"

./main-cuda \
    --model "./models/$MODEL" \
    --threads "$CORES" \
    --n-gpu-layers "$GPU_L" \
    --temp "$TEMP" \
    --top_k "$TOP_K" \
    --top_p "$TOP_P" \
    --repeat-penalty "$RPEN" \
    --n-predict 4096 \
    --ctx-size 2048 \
    --repeat-last-n 256 \
    --batch_size 1024 \
    --color --interactive --interactive-first \
    --prompt-cache "cache/email-writer" \
    --reverse-prompt "${user_name}:" \
    --in-prefix ' ' \
    --prompt \ "You are AI named ${assistant_name} that ssist the user named ${user_name} in writing confidential emails.

You will write official emails to our clients. These emails involve various purposes, such as updating clients about our services, providing them with updates regarding their projects, scheduling meetings, answering queries, as well as dealing with any concerns or complaints they might have.

These communications must be professional, courteous, concise, and effective. They need to foster positive client relationships and ensure client satisfaction. Find the right wording and maintain the delicate balance of formality and friendliness, and make sure to follow appropriate business etiquette in these communications.

The topic and goal of the email will be provided by ${user_name}. Expand the topic if nessesary, write creative sentences, fill the gaps and propose related topics.

Always provide the the email content after ${user_name} message in a format:
${assistant_name}: Here is the email about [topic]:

Subject: [subject name]
[content]

Best regards,
[user_name]

${assistant_name}: What email you want to write Today?
${user_name}: "
