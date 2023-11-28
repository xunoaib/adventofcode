import { readFileSync } from 'fs';

const regex = new RegExp('(\\d)\\1+');

function isValid1(s: string) {
  for (let i = 0; i < s.length - 1; i++)
    if (s[i] > s[i + 1])
      return false;
  return regex.test(s);
}

function isValid2(s: string) {
  if (!isValid1(s))
    return false;

  s = 'x' + s + 'x';
  for (let i = 0; i < s.length - 3; i++)
    if (s[i + 1] == s[i + 2] && s[i] != s[i + 1] && s[i + 2] != s[i + 3])
      return true;
  return false;
}

function main() {
  let [start, end] = readFileSync('input', 'utf-8').split('-').map(v => parseInt(v));
  let ans1 = 0, ans2 = 0;
  for (let n = start; n <= end; n++) {
    if (isValid1(String(n)))
      ans1++;
    if (isValid2(String(n)))
      ans2++;
  }

  console.log(`part1: ${ans1}`);
  console.log(`part2: ${ans2}`);
}

main();
