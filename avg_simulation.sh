#!/bin/bash

sum_float1=0
sum_float2=0
file_count=0

for file in /home/bruno.schaffer/CatchTheLionRemade/Resources/Alpha_Beta_TT-vs-Alpha_Beta_Fix/5-9-Alpha_Beta_TT-0-0-vs-Alpha_Beta_Fix-7-0/*.txt; do
    if [[ -f "$file" && -r "$file" ]]; then
        float_line=$(sed -n '3p' "$file")
        if [[ ! -z "$float_line" ]]; then
            float1=$(echo "$float_line" | cut -d':' -f1)
            float2=$(echo "$float_line" | cut -d':' -f2)
            sum_float1=$(echo "$sum_float1 + $float1" | bc)
            sum_float2=$(echo "$sum_float2 + $float2" | bc)
            ((file_count++))
        fi
    fi
done

if [[ $file_count -gt 0 ]]; then
    average_float1=$(echo "scale=2; $sum_float1 / $file_count" | bc)
    average_float2=$(echo "scale=2; $sum_float2 / $file_count" | bc)
    echo "Average of White: $average_float1"
    echo "Average of Black: $average_float2"
else
    echo "No valid files found."
fi