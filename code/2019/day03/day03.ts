import { readFileSync } from 'fs';

function get_offsets(direction: string) {
  switch (direction) {
    case 'R': return [1, 0];
    case 'L': return [-1, 0];
    case 'U': return [0, -1];
    case 'D': return [0, 1];
  }
}

// Returns a list of points traced by a line segment, not including the starting point
function iter_coords(cur_x: number, cur_y: number, direction: string, amount: number) {
  let coords: number[][] = [];
  let [xoff, yoff] = get_offsets(direction);
  for (let i = 0; i < amount; i++) {
    cur_x += xoff;
    cur_y += yoff;
    coords.push([cur_x, cur_y]);
  }
  return coords;
}

// Traces every point in a wire, returning a dict mapping each 'x,y' coordinate to its associated step count
function trace_wire(commands: string[]) {
  let positions: { [key: string]: number } = {};
  let steps = 1, cur_x = 0, cur_y = 0;
  for (let entry of commands) {
    const line_points = iter_coords(cur_x, cur_y, entry[0], parseInt(entry.substring(1)));
    for ([cur_x, cur_y] of line_points) {
      const key = cur_x + ',' + cur_y;
      if (positions[key] == null)
        positions[key] = steps;
      steps++;
    }
  }
  return positions;
}

let input = readFileSync('input', 'utf-8');
let commands = input.trim().split('\n').map(line => line.split(','));
let wire_steps = commands.map(v => trace_wire(v));
let intersections: string[] = [];

for (let pos of Object.keys(wire_steps[0]))
  if (wire_steps[1][pos] != null)
    intersections.push(pos);

let ans1 = Number.MAX_VALUE;
let ans2 = Number.MAX_VALUE;

for (let pos of intersections) {
  let [x, y] = pos.split(',').map(v => parseInt(v));
  const dist = Math.abs(x) + Math.abs(y);
  if (dist < ans1)
    ans1 = dist;

  const steps = wire_steps[0][pos] + wire_steps[1][pos];
  if (steps < ans2)
    ans2 = steps;
}

console.log(`part1: ${ans1}`);
console.log(`part2: ${ans2}`);
