import time

def sleep_for_retry (retry_interval):
  print(f"--- Start time out retry interval {retry_interval} seconds ---")
  time.sleep(retry_interval)
  print(f"--- End time out retry interval ---")
