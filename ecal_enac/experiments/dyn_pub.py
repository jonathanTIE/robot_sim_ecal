import ecal.core.core as ecal_core_deep
from dyn_topic_fetcher import BasicScript, robot_state

buttons = []
#Example :w
forward = robot_state.Speed()
forward.vx = 1.0
buttons.append(BasicScript("forward 1.0", "cmd_vel", forward))

if __name__ == "__main__": #debug console interface
    ecal_core_deep.set_process_state(1, 1, "interactive console debug interface waiting for input")
    for i, x in enumerate(buttons):
        print(f"input {i} to use button {x.script_name}")
    while True:
        user = input("\n")
        if user.isdigit():
            buttons[int(user)].execute()
