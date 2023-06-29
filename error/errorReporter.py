import traceback

def error_console_report (e):
  print(f"An error of type {type(e)} occurred: {e}")
  print("Traceback (most recent call last):")
  traceback.print_exc()
