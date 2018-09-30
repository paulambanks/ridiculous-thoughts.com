# Wait for the database connection.
import socket
import time
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('database', 5432))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)