const { input, flatten, rebuild, add, magnitude } = require('./day18')

const num = input().map(flatten).reduce(add)

console.log(magnitude(rebuild(num)[0]))
