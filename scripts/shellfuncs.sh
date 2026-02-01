#!/bin/bash
# run "source shellfuncs.sh" to enable functions for the current shell
# "run" executes "python3 dayN.py < dayN.in" based on the current directory name (dayN)
# "submit" pipes previous output to aoc executable for submission


python="$HOME/.pyenv/versions/advent/bin/python3"

# Directory of this file (works when sourced)
SCRIPT_DIR=$(cd "$(dirname "$0")" 2>/dev/null && pwd)

# Define aoc if missing
if ! command -v aoc >/dev/null 2>&1; then
    aoc() {
        "$python" "$SCRIPT_DIR/aoc.py" "$@"
    }
fi

run() {
    name=$(basename "$PWD")

    case "$name" in
        day[1-9]*)
            ;;
        *)
            echo "cwd \"$name\" is not in the form: dayN"
            return 1
            ;;
    esac

    [ -f "$name.py" ] || { echo "missing $name.py"; return 1; }
    [ -f "$name.in" ] || { echo "missing $name.in"; return 1; }

    "$python" "$name.py" < "$name.in"
}

submit() {
    run | aoc submit
}
