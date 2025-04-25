import runpod
import time  

def handler(event):
    print(f"Worker Start")
    input = event['input']
    
    prompt = input.get('prompt')  
    seconds = input.get('seconds', 0)  

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    
    while True:
        time.sleep(seconds)
        print("Loop iteration completed, continuing...")
    
    # Note: This return statement will never be reached due to the endless loop
    return prompt 

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })