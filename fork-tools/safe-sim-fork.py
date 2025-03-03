import threading
import time

def simulated_fork_bomb(depth=0, max_depth=3):
    if depth >= max_depth:
        print(f"🔚 Process at depth {depth} stopping.")
        return  # Stop recursion at max_depth to prevent system overload
    
    print(f"🚀 Process {depth} spawned. (Thread ID: {threading.get_ident()})")
    time.sleep(0.5)  # Simulate delay
    
    # Create two new threads instead of real processes
    t1 = threading.Thread(target=simulated_fork_bomb, args=(depth + 1, max_depth))
    t2 = threading.Thread(target=simulated_fork_bomb, args=(depth + 1, max_depth))
    
    print(f"🔁 Spawning children at depth {depth + 1}...")
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"✅ Process at depth {depth} completed.")

# Run the simulation
simulated_fork_bomb()


#Threads hav used isntaed of processes to avoid damage 