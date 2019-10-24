SimpleDataServer
=====
A single websocket server targeting for small applications.

## Concepts
The idea of the app comes from Robot Operating System(ROS), where nodes are allowed to communicate via topics. Topics are named bus over which nodes are sending/receiving messages.

## Mode
We can create nodes in different communication types.

1. publish - Nodes are allowed to send both text and binary messages. Each message will then be broadcast to subscribed nodes that registers the route.
2. subscribe - Nodes are listening for target route.
3. session - Bidirectional communication.
4. chat - Bidirectional communication without protocal

## Roadmap
1. Finish publish/subscribe/chat mode - Done
2. High level API for node without touching websocket. - WIP
3. Finish session - WIP
4. Route aliasing
5. Refine load balance (10~30 connections)


## Usage
First 
```bash
    pip install websocket-client
```
Connect /robot/lidar1 in subscribe mode.

```python
    import websocket
    ws = websocket.WebSocket('ws://localhost:9002/robot/lidar1/subscribe')
   
    while True:
        data = ws.recv()
```
