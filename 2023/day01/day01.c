#include <stdio.h>
#include <string.h>

char *words[] = {"one", "two",   "three", "four", "five",
                 "six", "seven", "eight", "nine"};

// attempts to parse a digit from the given position of a string
int parse_digit_at(char *s, int part2) {
    if (*s > '0' && *s <= '9')
        return *s - '0';

    if (part2) {
        for (int i = 0; i < sizeof(words) / sizeof(words[0]); i++)
            if (!strncmp(s, words[i], strlen(words[i])))
                return i + 1;
    }
    return -1;
}

// attempts to parse the two-digit calibration number starting from the
// beginning of the string
int parse_number(char *s, int part2) {
    int a = 0, b = 0;
    for (; *s; s++) {
        int digit = parse_digit_at(s, part2);
        if (digit >= 0) {
            if (a == 0)
                a = digit;
            b = digit;
        }
    }
    return 10 * a + b;
}

int main() {
    FILE *fd = fopen("day01.in", "r");
    char line[256];
    int ans1 = 0;
    int ans2 = 0;

    while (fgets(line, sizeof(line), fd)) {
        ans1 += parse_number(line, 0);
        ans2 += parse_number(line, 1);
    }

    printf("part1: %d\n", ans1);
    printf("part2: %d\n", ans2);
    return 0;
}
