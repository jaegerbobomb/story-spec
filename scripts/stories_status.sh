#!/usr/bin/env bash
# StorySpec - stories_status.sh
# Prints a colour-coded status table of all story files.
#
# Usage: ./stories_status.sh [stories-dir]
#   stories-dir defaults to ./stories

set -euo pipefail

STORIES_DIR="${1:-stories}"

if [[ ! -d "$STORIES_DIR" ]]; then
    echo "Directory not found: $STORIES_DIR" >&2
    exit 1
fi

GREEN='\033[32m'
YELLOW='\033[33m'
WHITE='\033[37m'
RED='\033[31m'
CYAN='\033[36m'
RESET='\033[0m'

printf "${CYAN}%-8s %-12s %-6s %-10s %s${RESET}\n" "ID" "STATUS" "BDD" "ESTIMATE" "TITLE"
printf "%-8s %-12s %-6s %-10s %s\n" "--------" "------------" "------" "----------" "-----"

shopt -s nullglob
files=("$STORIES_DIR"/S*.md)

if [[ ${#files[@]} -eq 0 ]]; then
    echo "No story files found in $STORIES_DIR"
    exit 0
fi

for f in "${files[@]}"; do
    id=$(grep -m1 '^id:'       "$f" | sed 's/id: *//')
    status=$(grep -m1 '^status:'  "$f" | sed 's/status: *//')
    bdd=$(grep -m1 '^bdd:'     "$f" | sed 's/bdd: *//')
    estimate=$(grep -m1 '^estimate:' "$f" | sed 's/estimate: *//')
    title=$(grep -m1 '^title:'   "$f" | sed 's/title: *//;s/"//g')

    case "$status" in
        done)        color="$GREEN"  ;;
        in_progress) color="$YELLOW" ;;
        todo)        color="$WHITE"  ;;
        *)           color="$RED"    ;;
    esac

    printf "${color}%-8s %-12s %-6s %-10s %s${RESET}\n" \
        "$id" "$status" "$bdd" "$estimate" "$title"
done
