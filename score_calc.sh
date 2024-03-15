#!/bin/bash

total_score_x=0
total_score_y=0

for file in /home/bruno.schaffer/CatchTheLionRemade/Resources/MCTS_MR-vs-Alpha_Beta_Fix/4-50-MCTS_MR-4-0-vs-Alpha_Beta_Fix-5-0/*.txt; do
    scores=$(head -n 1 "$file" | grep -oE '[0-9]+(\.[0-9]+)?,[0-9]+(\.[0-9]+)?|[0-9]+(\.[0-9]+)?:[0-9]+(\.[0-9]+)?' | tr '\n' ' ')
    score_x=$(echo "$scores" | awk -F: '{print $1}' | awk -F',' '{print $1}')
    score_y=$(echo "$scores" | awk -F: '{print $2}' | awk -F',' '{print $1}')
    
    total_score_x=$(echo "$total_score_x + $score_x" | bc)
    total_score_y=$(echo "$total_score_y + $score_y" | bc)
done

echo "Total score: $total_score_x:$total_score_y"