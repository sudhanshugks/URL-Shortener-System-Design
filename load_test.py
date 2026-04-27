import concurrent.futures
import requests
import time
import statistics

BASE_URL = "http://localhost:5000"
NUM_REQUESTS = 500
CONCURRENCY = 20

def shorten_and_resolve(i):
    long_url = f"https://example.com/page_{i}"
    
    # 1. Shorten
    start_time = time.time()
    try:
        res = requests.post(f"{BASE_URL}/shorten", json={"url": long_url}, timeout=2)
        res.raise_for_status()
        data = res.json()
        short_code = data['short_code']
        shorten_time = time.time() - start_time
        
        # 2. Resolve (allow redirects to be caught as 302, rather than followed)
        start_time_resolve = time.time()
        resolve_res = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False, timeout=2)
        resolve_time = time.time() - start_time_resolve
        
        if resolve_res.status_code == 302:
            return (True, shorten_time, resolve_time)
        else:
            return (False, shorten_time, resolve_time)
    except Exception as e:
        return (False, 0, 0)

def main():
    print(f"Starting Load Test...")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    
    start_time = time.time()
    
    success_count = 0
    failure_count = 0
    shorten_latencies = []
    resolve_latencies = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(shorten_and_resolve, i) for i in range(NUM_REQUESTS)]
        
        for future in concurrent.futures.as_completed(futures):
            success, s_time, r_time = future.result()
            if success:
                success_count += 1
                shorten_latencies.append(s_time)
                resolve_latencies.append(r_time)
            else:
                failure_count += 1

    total_time = time.time() - start_time
    
    print("\n--- Load Test Results ---")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {failure_count}")
    
    if success_count > 0:
        rps = success_count / total_time
        print(f"Requests Per Second (RPS): {rps:.2f}")
        
        avg_shorten = statistics.mean(shorten_latencies) * 1000
        avg_resolve = statistics.mean(resolve_latencies) * 1000
        print(f"Average Shorten Latency: {avg_shorten:.2f} ms")
        print(f"Average Resolve Latency: {avg_resolve:.2f} ms")

if __name__ == "__main__":
    main()
