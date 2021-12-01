#!/bin/bash
mod=${1/#src\//}
mod=${mod/%.rs/}
mod=${mod//\//::}
rm src/main.rs
cat > src/main.rs <<EOF
fn main() {
  advent_of_code::$mod::main();
}
EOF
