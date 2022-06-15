from dyn_topic_fetcher import BasicScript, robot_state

buttons = []
#Example :
forward = robot_state.Speed()
forward.vx = 1.0
buttons.append(BasicScript("forward 1.0", "cmd_vel", forward))

if __name__ == "__main__": #debug console interface
    for i, x in enumerate(buttons):
        print(f"input {i} to use button {x.script_name}")
    while True:
        user = input("\n")
        if user.isdigit():
            buttons[int(user)].execute()
