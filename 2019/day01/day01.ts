import { readFileSync } from 'fs';

function calcpart2(mass: number) {
  let fuel = 0;
  while (true) {
    mass = Math.floor(mass / 3) - 2;
    if (mass <= 0)
      return fuel;
    fuel += mass; 
  }
}

let data = readFileSync('input', 'utf-8');
let vals = data.trim().split('\n').map(v => parseInt(v));

const part1 = vals.map(v => Math.floor(v / 3) - 2).reduce((a, b) => (a + b));
const part2 = vals.map(v => calcpart2(v)).reduce((a, b) => (a + b));

console.log("part1:", part1);
console.log("part2:", part2);
