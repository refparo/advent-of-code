const { input, flatten, rebuild, add, magnitude } = require('./day18')

const nums = input().map(flatten)
const len = nums.length
let max = 0;
for (let i = 0; i < len; i++)
  for (let j = i + 1; j < len; j++)
    max = Math.max(max,
      magnitude(rebuild(add(nums[i], nums[j]))[0]),
      magnitude(rebuild(add(nums[j], nums[i]))[0]))

console.log(max)
