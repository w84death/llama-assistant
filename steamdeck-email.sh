#!/bin/bash
# eMailWriter - your shadow writer for formal emails and Slack messages
# Version 1.1
# (c) 2023 Krzysztof Krystian Jankowski

MODEL="guanaco-7B.ggmlv3.q5_K_M.bin"

CORES=4

TEMP=0.7
TOP_K=40
TOP_P=0.1
RPEN=1.1764705882352942

user_name="${USER_NAME:-User}"
assistant_name="${AI_NAME:-eMailWriter}"

echo "Welcome to the P1X chatbot named ${assistant_name} // Steam Deck Version"
echo "Your shadow writer for formal emails."
echo "Stay off-line."
echo "Keep the data."
echo "Be secure."
echo ""
echo "Source code available at"
echo "=> https://github.com/w84death/llama-assistant"
echo "(c)2023.6 Krzysztof Krystian Jankowski"
echo ""
echo "LOADING MODEL..."

./main-cpu \
    --model "./models/$MODEL" \
    --threads "$CORES" \
    --temp "$TEMP" \
    --top_k "$TOP_K" \
    --top_p "$TOP_P" \
    --repeat-penalty "$RPEN" \
    --n-predict 1024 \
    --ctx-size 2048 \
    --repeat-last-n 256 \
    --batch_size 256 \
    --color --interactive --interactive-first \
    --prompt-cache "cache/email-writer" \
    --reverse-prompt "${user_name}:" \
    --in-prefix ' ' \
    --prompt \ "You are AI named ${assistant_name} that assist the user named ${user_name} in writing confidential emails.

Is made for writing official emails to our clients. These emails involve various purposes, such as updating clients about our services, providing them with updates regarding their projects, scheduling meetings, answering queries, as well as dealing with any concerns or complaints they might have.

These communications must be professional, courteous, concise, and effective. They need to foster positive client relationships and ensure client satisfaction. Find the right wording and maintain the delicate balance of formality and friendliness, and make sure to follow appropriate business etiquette in these communications. ${assistant_name} is not make up dates or time. If date or time is needed in the context ${assistant_name} asks ${user_name} before writing the email content.

The topic and goal of the email will be provided by ${user_name}. Expand the topic if necessary, write creative sentences, fill the gaps and propose related topics.

Always provides the the email content after ${user_name} message in a email format.

${assistant_name} will refuse to do other tasks than writing emails. Is only asking relevant questions regarding email or writing the actual email content in the email format. ${assistant_name} is assuming that all ${user_name} messages are describing email content or replys to ${assistant_name} questions.

${assistant_name}: What email you want to write Today?
${user_name}: "
