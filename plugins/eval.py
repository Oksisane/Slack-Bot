def on_message(msg):
    if "!eval" in msg:
        args = msg.split("!eval")[1]
        return "Eval Result:" + str(eval(args))
