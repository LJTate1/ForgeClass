from tqdm import tqdm
import time

# Sample task with tqdm
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.1)  # Simulate some work
