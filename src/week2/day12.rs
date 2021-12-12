use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Graph = HashMap<String, Vec<String>>;

pub fn input() -> Graph {
  let file = File::open("input/day12.txt").unwrap();
  let paths = BufReader::new(file).lines()
    .map(|l| {
      let s = l.unwrap();
      let (a, b) = s.split_once('-').unwrap();
      (String::from(a), String::from(b))
    })
    .collect::<Vec<_>>();
  let mut graph = HashMap::with_capacity(16);
  for (a, b) in paths.iter() {
    if !graph.contains_key(a) {
      graph.insert(String::from(a), Vec::with_capacity(8));
    }
    if !graph.contains_key(b) {
      graph.insert(String::from(b), Vec::with_capacity(8));
    }
  }
  for (a, b) in paths.iter() {
    graph.get_mut(a).unwrap().push(String::from(b));
    graph.get_mut(b).unwrap().push(String::from(a));
  }
  graph
}

pub fn search<'a, const hurry: bool>(graph: &'a Graph, path: &mut Vec<&'a str>)
  -> usize {
  let mut count = 0;
  let next_caves = graph[path[path.len() - 1]].iter()
    .filter(|c| c.chars().next().unwrap().is_uppercase() ||
      path.iter().all(|d| c != d))
    .collect::<Vec<_>>();
  for next in next_caves {
    if next == "end" {
      count += 1;
    } else {
      path.push(next);
      count += search::<hurry>(graph, path);
      path.pop();
    }
  }
  if !hurry {
    let next_caves = graph[path[path.len() - 1]].iter()
      .filter(|c| c != &"start" &&
        c.chars().next().unwrap().is_lowercase() &&
        path.iter().any(|d| c == d))
      .collect::<Vec<_>>();
    for next in next_caves {
      path.push(next);
      count += search::<true>(graph, path);
      path.pop();
    }
  }
  count
}
