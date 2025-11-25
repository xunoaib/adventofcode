GSN = int(input())


def power_level(x, y, gsn=GSN):
    rack_id = x + 10
    p = rack_id * y
    p += gsn
    p *= rack_id
    p = ((p % 1000) - (p % 100)) // 100
    p -= 5
    return p


print(power_level(3, 5, 8))
print(power_level(122, 79, 57))
print(power_level(217, 196, 39))
print(power_level(101, 153, 71))
