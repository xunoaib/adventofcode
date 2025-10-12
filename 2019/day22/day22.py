import sys

lines = sys.stdin.read().strip().splitlines()
cards: list[int] = list(range(10007))

for line in lines:

    if line == 'deal into new stack':
        cards = cards[::-1]
    elif line.startswith('cut'):
        n = int(line.split()[-1])
        cards = cards[:n] + cards[n:]
    elif line.startswith('deal with increment'):
        n = int(line.split()[-1])
        new_cards: list[int | None] = [None] * len(cards)
        pos = 0
        while cards:
            new_cards[pos] = cards.pop(0)
            pos = (pos + 1) % len(new_cards)

        cards = new_cards

print(cards)
