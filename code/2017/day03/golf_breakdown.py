# 🔥 110 byte golf (Part 1 Only)
# n=int(input());print((lambda b=int((n-1)**.5-1)//2*2+1:(b//2+abs(((n-b**2)-1)%(b+1)-b//2)+1))() if n>1 else 0)


# main function which is easier on the eyes
def solve_pt1(n):
    return (
        lambda b=int((n - 1)**.5 - 1) // 2 * 2 + 1:
        (b // 2 + abs(((n - b**2) - 1) % (b + 1) - b // 2) + 1)
    )() if n > 1 else 0


def main():
    print(solve_pt1(325489))

    for n in range(1, 50):
        print(n, solve_pt1(n))

    # # original version, broken down into parts
    # for n in range(2,75):
    #     base = int((n - 1)**.5 - 1) // 2 * 2 + 1
    #     raw_diff = (n - base**2)
    #     mod_diff = (raw_diff - 1) % (base + 1)   # mod base + 1 to remove rotational symmetry around outer edges
    #     dist = abs(mod_diff - base // 2)         # generate the 2 1 0 1 2 3 pattern
    #     total = base // 2 + dist + 1
    #     print(n, total, '.'*dist)

    # # with substitutions from above
    # for n in range(2,95):
    #     base = int((n-1)**.5 - 1) // 2 * 2 + 1
    #     total = base // 2 + abs(((n - base**2) - 1) % (base + 1) - base // 2) + 1
    #     print(n, total)


if __name__ == '__main__':
    main()
