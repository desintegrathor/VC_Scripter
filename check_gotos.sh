#!/bin/bash
for file in test1_validation.c test2_validation.c test3_validation.c; do
  echo "=== Checking $file ==="
  undefined=0
  while IFS= read -r line; do
    # Extract block number from goto statement
    block=$(echo "$line" | grep -o 'goto block_[0-9]\+' | grep -o '[0-9]\+')
    if [ -n "$block" ]; then
      # Check if label exists
      if ! grep -q "^[[:space:]]*block_${block}:" "$file"; then
        echo "UNDEFINED: $line"
        undefined=$((undefined + 1))
      fi
    fi
  done < <(grep 'goto block_' "$file")
  if [ $undefined -eq 0 ]; then
    echo "✓ No undefined gotos"
  else
    echo "✗ Found $undefined undefined gotos"
  fi
  echo ""
done
