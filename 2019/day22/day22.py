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
        spots: list[int | None] = [None] * len(cards)
        pos = 0

        print('Dealing with increment:', n)
        print('Looping')

        while cards:
            moves_left = n
            while moves_left and None in spots:
                pos = (pos + 1) % len(cards)
                if spots[pos] is None:
                    moves_left -= 1
            spots[pos] = cards.pop(0)
            print(
                'writing spot', pos, 'cards left:', len(cards),
                sum(s == None for s in spots)
            )
            # print(n, len(cards))

        cards = spots
        print('Done')
        # print(spots)
        exit()
