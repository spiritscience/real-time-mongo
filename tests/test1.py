import sys
import os
sys.path.insert (0,'/home/taiiwo/wwwphantas.ml/real-time-mongo')
os.chdir("/home/taiiwo/wwwphantas.ml/real-time-mongo")
from RTM import RTM
rtm = RTM()
a = rtm.receive_stream(["test", "supersecretkey"], [["test", "supersecretkey"],], "messages")

while 1:
    for i in a:
        print(i)
