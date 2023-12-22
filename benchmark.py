import time

stats = {}

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        if func.__name__ in stats:
            stats[func.__name__]["total_time"] += elapsed_time
            stats[func.__name__]["call_count"] += 1
        else:
            stats[func.__name__] = {"total_time": elapsed_time, "call_count": 1}
        
        return result
    
    return wrapper

def show_stats():
    for func_name, func_stats in stats.items():
        avg_time = func_stats["total_time"] / func_stats["call_count"]
        print(f"{func_name}: {1000 * avg_time:.6f}ms avg")
