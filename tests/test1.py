from RTM import RTM
rtm = RTM()
a = rtm.receive_stream(["test", "supersecretkey"], [["test", "supersecretkey"],], "messages")

for i in a:
    print(i)
