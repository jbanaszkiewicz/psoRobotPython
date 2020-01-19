import subprocess
from time import time
import os, sys
import json
from main import main
from tqdm import tqdm

graph_paths = [
  "graph1000"
]
nrs_of_iterations = [
  10000
]

threads_per_block = [ 32
  # 128, 128, 128, 128, 128,
  # 32, 32, 32, 32, 32
  # 64, 64, 64, 64, 64, 
  # 256, 256, 256, 256, 256
]

blocks_per_grid = [ 128
  # 16, 16, 16, 16, 16
  # 32, 32, 32, 32, 32,
  # 64, 64, 64, 64, 64,
  # 128, 128, 128, 128, 128
]
particles_in = [
  200, 200, 200, 200, 200,
  960, 960, 960, 960, 960,
  1920, 1920, 1920, 1920, 1920 
]

date_start = int(time()) 
data = []
for graph_path in  graph_paths: 
  for nr_of_iteration in nrs_of_iterations:
    for nr_of_threads in threads_per_block:
      for blocks in blocks_per_grid:
        for particles in tqdm(particles_in, desc='graphs_progress'):  
          duration, cost_best_path = main('./graphs'+graph_path, nr_of_iteration, nr_of_threads, blocks, particles)
          single_data = {"name":            str(graph_path)+'_iters'+str(nr_of_iteration)+'_threads'+str(nr_of_threads)+'_blocks'+str(blocks)+'_particles'+str(particles),
                        "graph":            graph_path,
                        "nr_of_iteration":  nr_of_iteration,
                        "nr_of_threads":    nr_of_threads,
                        "nr_of_blocks":     blocks,
                        "duration":         duration,
                        "cost_best_path":   cost_best_path,
                        "particles":   particles
                        }
          data.append(single_data)
with open(f"./results/{date_start}.json", "w") as json_file:
  json.dump(data, json_file, indent=4)
  json_file.write("\n")