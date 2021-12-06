#!/bin/bash
# run "source shellfuncs.sh" to enable functions for the current shell
# "run" executes "python3 dayN.py < dayN.in" based on the current directory name (dayN)
# "submit" pipes previous output to aoc executable for submission

# aliases aoc to ./scripts/aoc.py in this github repo
if ! command -v aocs &> /dev/null; then
    alias aoc="`dirname "$0"`/aoc.py"
fi

function run {
    name=${PWD##*/}
    if ! [[ $name =~ ^day[0-9]+$ ]]; then
        echo "cwd \"$name\" is not in the form: day[0-9]+"
        return 1
    fi
    python3 $name.py < $name.in
}

function submit {
    run | aoc submit
}
