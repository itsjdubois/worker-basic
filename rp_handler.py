import runpod
import time
import multiprocessing

def endless_loop(seconds):
    print(f"Starting endless loop with {seconds} second interval")
    while True:
        time.sleep(seconds)
        print("Loop iteration completed, continuing...")

def handler(event):
    print(f"Worker Start")
    input = event['input']
    
    prompt = input.get('prompt')  
    seconds = input.get('seconds', 0)  

    print(f"Received prompt: {prompt}")
    print(f"Starting subprocess with {seconds} second interval...")
    
    # Create and start the subprocess
    process = multiprocessing.Process(target=endless_loop, args=(seconds,))
    process.start()
    
    # Return immediately while the subprocess continues running
    return prompt 

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })