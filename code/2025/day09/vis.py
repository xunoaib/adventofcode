import sys
from itertools import pairwise

from PIL import Image, ImageDraw

lines = sys.stdin.read().strip().split('\n')
corners = [tuple(map(int, line.split(','))) for line in lines]

xmin = min(x for x, y in corners)
xmax = max(x for x, y in corners)
ymin = min(y for x, y in corners)
ymax = max(y for x, y in corners)

downscale = 100

im = Image.new(
    'RGB', (
        (xmax - xmin + downscale) // downscale + 1,
        (ymax - ymin + downscale) // downscale + 1,
    )
)
draw = ImageDraw.Draw(im)

for p, q in pairwise(corners + corners[:1]):
    pp = ((p[0] - xmin) // downscale, (p[1] - ymin) // downscale)
    qq = ((q[0] - xmin) // downscale, (q[1] - ymin) // downscale)
    draw.line((*pp, *qq), fill=(127, ) * 3)
    draw.line((*pp, *pp), fill=(0, 255, 0))

im.save('plot.png')
