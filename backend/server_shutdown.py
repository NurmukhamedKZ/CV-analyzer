import os
import signal

# Get the PID of the running Uvicorn process (replace with actual PID if known)
# For example, if you know the PID, you can use: pid = 12345
# Otherwise, you might need to find it using tools like 'ps' or 'tasklist'
pid = 8000 # This gets the current process's PID, not necessarily the Uvicorn server's if run as a subprocess

# Send the SIGINT signal to the process
os.kill(pid, signal.SIGINT)