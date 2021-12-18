// It's too annoying to solve the puzzle today in Rust,
// so I use Javascript for this.

const fs = require('fs')

/** @type {() => any[]} */
const input = () => fs
  .readFileSync("input/day18.txt", { encoding: 'utf-8' })
  .split("\n").slice(0, -1).map(l => JSON.parse(l))

/** @type {(num: any) => [number, number][]} */
const flatten = num =>
  typeof num == 'number' ? [[num, 0]]
  : [...flatten(num[0]), ...flatten(num[1])]
    .map(([num, l]) => [num, l + 1])

/** @type {(num: [number, number][]) => [any, [number, number][]]} */
function rebuild(num) {
  const [[n, level], ...tail] = num
  if (level == 0) return [n, tail]
  else {
    const [left, rest1] = rebuild(num.map(([num, l]) => [num, l - 1]))
    const [right, rest2] = rebuild(rest1)
    return [[left, right], rest2.map(([num, l]) => [num, l + 1])]
  }
}

/** @type {(num: [number, number][]) => [number, number][]?} */
function explode(num) {
  const leftIdx = num.findIndex(([_, l]) => l > 4)
  if (leftIdx == -1) return null
  /** @type {[number, number][]} */
  let res = []
  if (leftIdx > 0) {
    res.push(...num.slice(0, leftIdx - 1))
    const [left, _] = num[leftIdx]
    const [leftN, leftNL] = num[leftIdx - 1]
    res.push([left + leftN, leftNL])
  }
  res.push([0, num[leftIdx][1] - 1])
  if (leftIdx + 1 < num.length - 1) {
    const [right, _] = num[leftIdx + 1]
    const [rightN, rightNL] = num[leftIdx + 2]
    res.push([right + rightN, rightNL])
    res.push(...num.slice(leftIdx + 3))
  }
  return res
}

/** @type {(num: [number, number][]) => [number, number][]?} */
function split(num) {
  const idx = num.findIndex(([num, _]) => num >= 10)
  if (idx == -1) return null
  const [n, l] = num[idx]
  return [
    ...num.slice(0, idx),
    [Math.floor(n / 2), l + 1],
    [Math.ceil(n / 2), l + 1],
    ...num.slice(idx + 1)
  ]
}

/** @type {(left: [number, number][], right: [number, number][])=> [number, number][]} */
function add(left, right) {
  /** @type {[number, number][]} */
  let sum = [...left, ...right].map(([num, l]) => [num, l + 1])
  while (true) {
    let step = explode(sum) ?? split(sum)
    if (step == null) break
    sum = step
  }
  return sum
}

const magnitudeHelper = num => typeof num == 'number' ? num : magnitude(num)
/** @type {(num: any) => number} */
const magnitude = ([left, right]) =>
  3 * magnitudeHelper(left) + 2 * magnitudeHelper(right)

module.exports = {
  input,
  flatten, rebuild,
  explode, split,
  add,
  magnitude
}
