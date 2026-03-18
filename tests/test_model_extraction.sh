#!/bin/bash

# Target file
AGENT_DIR="agents/nnw_writer_template"
AGENTS_MD="$AGENT_DIR/AGENTS.md"

echo "Testing model extraction logic from manage_writer/SKILL.md..."
echo "Target file: $AGENTS_MD"
echo "---------------------------------------------------"

# Coordinator Extraction
COORD_MODEL=$(awk -F'|' '/`coordinator`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENTS_MD")
echo "Coordinator Expected: qwen35-35b-a3b_no_thinking"
echo "Coordinator Actual:   $COORD_MODEL"
if [ "$COORD_MODEL" == "qwen35-35b-a3b_no_thinking" ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi
echo "---------------------------------------------------"

# Planner Extraction
PLANNER_MODEL=$(awk -F'|' '/`planner`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENTS_MD")
echo "Planner Expected: qwen35-27b-m"
echo "Planner Actual:   $PLANNER_MODEL"
if [ "$PLANNER_MODEL" == "qwen35-27b-m" ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi
echo "---------------------------------------------------"

# Writer Extraction
WRITER_MODEL=$(awk -F'|' '/`writer`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENTS_MD")
echo "Writer Expected: lms/qwen3-14b"
echo "Writer Actual:   $WRITER_MODEL"
if [ "$WRITER_MODEL" == "lms/qwen3-14b" ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi
echo "---------------------------------------------------"

# Proofreader Extraction
PROOF_MODEL=$(awk -F'|' '/`proofreader`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENTS_MD")
echo "Proofreader Expected: lms/phi4-reasoning-plus"
echo "Proofreader Actual:   $PROOF_MODEL"
if [ "$PROOF_MODEL" == "lms/phi4-reasoning-plus" ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi
echo "---------------------------------------------------"

if [ "$COORD_MODEL" == "qwen35-35b-a3b_no_thinking" ] && \
   [ "$PLANNER_MODEL" == "qwen35-27b-m" ] && \
   [ "$WRITER_MODEL" == "lms/qwen3-14b" ] && \
   [ "$PROOF_MODEL" == "lms/phi4-reasoning-plus" ]; then
    echo "Summary: ✅ ALL TEST CASES PASSED."
else
    echo "Summary: ❌ SOME TESTS FAILED."
fi
