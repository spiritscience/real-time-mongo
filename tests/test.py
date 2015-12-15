import sys
import os
sys.path.insert (0,'/home/taiiwo/wwwphantas.ml/real-time-mongo')
os.chdir("/home/taiiwo/wwwphantas.ml/real-time-mongo")
from RTM import RTM
rtm = RTM()
rtm.send("One giant leap for bob-kind", ["test", "supersecretkey"], "bob", "messages")
