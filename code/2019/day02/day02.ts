import { readFileSync } from 'fs';

function exec_one(opcode: number, v1: number, v2: number) {
  return opcode == 1 ? v1 + v2 : v1 * v2;
}

function part1(arr: number[], v1: number = 12, v2: number = 2) {
  arr = arr.map(v => v);
  arr[1] = v1;
  arr[2] = v2;
  for (let i = 0; i < arr.length && arr[i] != 99; i += 4)
    arr[arr[i + 3]] = exec_one(arr[i], arr[arr[i + 1]], arr[arr[i + 2]]);
  return arr[0];
}

function part2(vals: number[]) {
  for (let v1 = 0; v1 < 100; v1++)
    for (let v2 = 0; v2 < 100; v2++)
      if (part1(vals, v1, v2) == 19690720)
        return v1 * 100 + v2;
}

let data = readFileSync('input', 'utf-8');
let vals = data.trim().split(',').map(v => parseInt(v));

const ans1 = part1(vals);
console.log(`part1: ${ans1}`);

const ans2 = part2(vals);
console.log(`part2: ${ans2}`);
