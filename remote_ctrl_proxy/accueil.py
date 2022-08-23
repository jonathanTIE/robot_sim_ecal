
"""
This file manage the input of many users, and periodically take the majority cmd to send it
"""
import websockets

import asyncio

DEBUG = False

ROBOT_URL = "ws://192.168.42.226/ws"
PROXY_URL = "192.168.42.124" 
PROXY_PORT = 5000

users_cmds = {} #remote address : last cmd received  #remote address = (IP of user, port)
cur_ws = [] #list of all websockets of connected users
active_users = 0 #count sent regularly
majority_cmd = "s"
majority_cmd_users = 0

#https://websockets.readthedocs.io/en/stable/
async def on_ws(data): 
    while True:
    #receive msg and send the user count
        if data not in cur_ws: 
            cur_ws.append(data)
        msg = None
        try:
            msg = await data.recv()
        except websockets.ConnectionClosedOK:
            print("closed")
            break

        #check if msg is valid or not and add it to the list of all last cmds
        if msg != None and (msg == "f" or msg == "b" or msg == "l" or msg == "r" or msg == "s"):
            users_cmds[data.remote_address] = msg
            print(msg)
        else: 
            print(f"error ! invalid msg received from user {data.remote_address}")

def fusion_cmd(list_of_cmds: list()):
    #return (majority command, number of ppl who chose it)
    cmd_count = {"f": 0, "b": 0, "l": 0, "r":0, "s":0}
    for cmd in list_of_cmds:
        cmd_count[cmd] += 1

    max_val = 0
    cmd_to_send = None
    for key, value in cmd_count.items():
        if value > max_val:
            max_val = value
            cmd_to_send = key
    return (cmd_to_send, max_val)

async def periodic_robot_cmd():
    global majority_cmd_users, majority_cmd, DEBUG
    async with websockets.connect(ROBOT_URL) as websocket:
        while True:
            cmd, majority_cmd_users = fusion_cmd(users_cmds.values())
            majority_cmd = cmd
            if cmd == None:
                cmd = "s"
            if not DEBUG:
                await websocket.send(cmd)
            print(f"sent to robot {cmd}")
            await asyncio.sleep(0.100) #send at ~10 hz the commands

async def count_check_connected_users():
    #remove the inactive users commands and count the active users
    global active_users, majority_cmd
    ws_str_to_user = {"f": "AVANCER", "b": "RECULER", "l": "GAUCHE", "r":"DROITE", "s":"STOP", None:"STOP"}
    while True:
        count = 0
        for ws in cur_ws:
            if ws.closed: 
                cur_ws.remove(ws)
            else: 
                count += 1
        for ws in cur_ws:
            await ws.send(f"Choix {ws_str_to_user[majority_cmd]} de {majority_cmd_users}/{active_users}")
        active_users = count
        await asyncio.sleep(0.25)

async def main():
    if DEBUG:
        asyncio.create_task(periodic_robot_cmd())
    else:
        asyncio.create_task(periodic_robot_cmd())
    asyncio.create_task(count_check_connected_users())
    async with websockets.serve(on_ws, PROXY_URL, PROXY_PORT) as server:
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    #launch server
    asyncio.run(main())