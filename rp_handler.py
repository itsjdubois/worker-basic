import runpod
import time
import multiprocessing
import os
import signal
import sys
from datetime import datetime

def endless_loop(seconds, test_type="basic"):
    """
    Different types of endless loops to test various timeout scenarios
    """
    print(f"[{datetime.now()}] Starting {test_type} endless loop with {seconds} second interval")
    iteration = 0
    
    try:
        while True:
            iteration += 1
            
            if test_type == "basic":
                time.sleep(seconds)
                print(f"[{datetime.now()}] Basic loop iteration {iteration} completed")
                
            elif test_type == "cpu_intensive":
                # CPU intensive loop
                start_time = time.time()
                while time.time() - start_time < seconds:
                    _ = sum(range(10000))  # Burn CPU cycles
                print(f"[{datetime.now()}] CPU intensive iteration {iteration} completed")
                
            elif test_type == "memory_intensive":
                # Memory intensive loop
                data = [i for i in range(100000)]  # Create some data
                time.sleep(seconds)
                print(f"[{datetime.now()}] Memory intensive iteration {iteration} completed (data size: {len(data)})")
                del data
                
            elif test_type == "io_intensive":
                # I/O intensive loop
                with open(f"/tmp/test_file_{iteration}.txt", "w") as f:
                    f.write("x" * 10000)
                time.sleep(seconds)
                print(f"[{datetime.now()}] I/O intensive iteration {iteration} completed")
                try:
                    os.remove(f"/tmp/test_file_{iteration}.txt")
                except:
                    pass
                    
    except KeyboardInterrupt:
        print(f"[{datetime.now()}] Loop interrupted by signal")
    except Exception as e:
        print(f"[{datetime.now()}] Loop error: {e}")

def signal_handler(signum, frame):
    """Handle termination signals"""
    print(f"[{datetime.now()}] Received signal {signum}, attempting graceful shutdown...")
    sys.exit(0)

def handler(event):
    print(f"[{datetime.now()}] Worker Start - PID: {os.getpid()}")
    
    # Register signal handlers to detect when RunPod tries to kill the function
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    input_data = event['input']
    
    prompt = input_data.get('prompt', 'No prompt provided')
    seconds = input_data.get('seconds', 1)
    test_type = input_data.get('test_type', 'basic')  # basic, cpu_intensive, memory_intensive, io_intensive
    return_delay = input_data.get('return_delay', 0)  # Delay before returning (to test if subprocess continues)
    
    print(f"[{datetime.now()}] Configuration:")
    print(f"  - Prompt: {prompt}")
    print(f"  - Loop interval: {seconds} seconds")
    print(f"  - Test type: {test_type}")
    print(f"  - Return delay: {return_delay} seconds")
    
    # Create and start the subprocess
    print(f"[{datetime.now()}] Starting subprocess...")
    process = multiprocessing.Process(target=endless_loop, args=(seconds, test_type))
    process.start()
    
    print(f"[{datetime.now()}] Subprocess PID: {process.pid}")
    print(f"[{datetime.now()}] Main process continuing...")
    
    # Optional delay before returning (to test different scenarios)
    if return_delay > 0:
        print(f"[{datetime.now()}] Waiting {return_delay} seconds before returning...")
        time.sleep(return_delay)
    
    response = {
        "status": "started",
        "prompt": prompt,
        "main_pid": os.getpid(),
        "subprocess_pid": process.pid,
        "test_type": test_type,
        "interval_seconds": seconds,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[{datetime.now()}] Returning response: {response}")
    return response

if __name__ == '__main__':
    print(f"[{datetime.now()}] Starting RunPod serverless handler...")
    runpod.serverless.start({'handler': handler})