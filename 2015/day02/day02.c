#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int compare(const void* a, const void* b) {
    return *(int*)a - *(int*)b;
}

int main() {
    int total_area = 0;   // part1
    int total_ribbon = 0; // part2
    char line[32];

    while (fgets(line, sizeof(line), stdin) > 0) {
        // read values into array
        int dims[3], idx = 0;
        char *token = strtok(line, "x");
        while (token != NULL) {
            dims[idx++] = strtol(token, NULL, 0);
            token = strtok(NULL, "x");
        }

        qsort(dims, 3, sizeof(int), compare);
        int area = 3 * dims[0] * dims[1] + 2 * (dims[0] * dims[2] + dims[1] * dims[2]);
        total_area += area;

        total_ribbon += 2 * (dims[0] + dims[1]);     // ribbon wrap
        total_ribbon += dims[0] * dims[1] * dims[2]; // bow
    }
    printf("part1: %d\n", total_area);
    printf("part2: %d\n", total_ribbon);
    return 0;
}
