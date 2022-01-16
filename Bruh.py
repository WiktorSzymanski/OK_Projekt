from timeit import default_timer as timer

def main():
  start_time = timer()
  while(timer() - start_time < 10):
    print(timer() - start_time)
  
  

main()