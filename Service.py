import websockets
import struct
from Constants import *
available_services = ['publish', 'subscribe', 'session', 'chat']

class ClientPool(object):
    def __init__(self):
        self._clients = []

    def add_client(self, client):
        if not client in self._clients:
            self._clients.append(client)

    def remove_client(self, client):
        try:
            self._clients.remove(client)
        except:
            pass

    async def boardcast(self, src_client_ws, data, echo=False):
        for client in self._clients:
            if echo or src_client_ws != client:
                await client.send(data)

    async def sendto(self, dst_id, data):
        for client in self._clients:
            if dst_id == id(client):
                await client.send(data)
                return True
        return False

    @property
    def clients(self):
        return [id(x) for x in self._clients]

    @property
    def num_clients(self):
        return len(self._clients)


def init_service(service_type, ws):
    if service_type in available_services:
        print(service_type)
        return ClientPool()

def configure_service(service_instance, service_type, ws):
    pass


async def serve_publish(ctx, ws):
    while True:
        try:
            buf = await ws.recv()
            await ctx.boardcast(ctx, buf)
        except websockets.exceptions.ConnectionClosedOK:
            break
        except websockets.exceptions.ConnectionClosedError:
            break
    await ws.wait_closed()

async def serve_subscribe(ctx, ws):
    ctx.add_client(ws)
    await ws.wait_closed()
    ctx.remove_client(ws)

async def serve_session(ctx, ws):
    # greeting
    await ws.send(GREETING+struct.pack('<Q', id(ws)))
    ctx.add_client(ws)

    while True:
        try:
            buf = await ws.recv()
            if buf[0] == CMD_PARTICIPANT:
                clients_id = ctx.clients
                await ws.send(PARTICIPANT+struct.pack('<%dQ'%len(clients_id), *clients_id))
            if buf[0] == CMD_BOARDCAST:
                await ctx.boardcast(ws, BOARDCAST+buf[1:])
        except websockets.exceptions.ConnectionClosedOK:
            break
        except websockets.exceptions.ConnectionClosedError:
            break
    await ws.wait_closed()
    ctx.remove_client(ws)

async def serve_chat(ctx, ws):
    ctx.add_client(ws)

    while True:
        try:
            buf = await ws.recv()
            await ctx.boardcast(ws, buf)
        except websockets.exceptions.ConnectionClosedOK:
            break
        except websockets.exceptions.ConnectionClosedError:
            break
    await ws.wait_closed()
    ctx.remove_client(ws)
