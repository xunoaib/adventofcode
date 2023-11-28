#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int compare(const void * a, const void * b) {
    return *(int*)a - *(int*)b;
}

void part1() {
    char line[64];
    int sides[3];
    int num_valid = 0;
    while (fgets(line, sizeof(line), stdin) > 0) {
        for (int i = 0; i < 3; i++)
            sides[i] = strtol(line + i * 5, NULL, 10);
        qsort(sides, 3, sizeof(int), compare);
        if (sides[0] + sides[1] > sides[2])
            num_valid++;
    }
    printf("part1: %d\n", num_valid);
}

int readgroup() {
    int values[3][3]; // [col][row]
    char line[64];

    // read 3 lines at a time
    for (int row = 0; row < 3; row++) {
        if (fgets(line, 64, stdin) == NULL)
            return -1; // EOF

        // split line into 3 ints
        for (int col = 0; col < 3; col++)
            values[col][row] = strtol(line + col * 5, NULL, 10);
    }

    // sort columns, then count the number of valid triangles
    int valid = 0;
    for (int col = 0; col < 3; col++) {
        qsort(values[col], 3, sizeof(int), compare);
        if (values[col][0] + values[col][1] > values[col][2])
            valid++;
    }
    return valid;
}

void part2() {
    int total = 0;
    int num_valid;

    while ((num_valid = readgroup()) != -1)
        total += num_valid;
    printf("part2: %d\n", total);
}

int main() {
    /* part1(); */
    part2();
}
