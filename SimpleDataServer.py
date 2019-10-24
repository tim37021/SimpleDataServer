import asyncio
import websockets
import re

import Service

routes_service = {'/': None}

class SimpleDataServer(object):
    def __init__(self, port):
        self._port = port

    def _start_server(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        task = websockets.serve(serve, "0.0.0.0", self._port, ping_timeout=None)
        
        self._loop.run_until_complete(task)
        try:
            self._loop.run_forever()
        except:
            pass

    def run(self):
        from threading import Thread
        
        self._thread = Thread(target = self._start_server)
        self._thread.start()
        
        while self._thread.isAlive():
            try:
                self._thread.join(1)
            except KeyboardInterrupt:
                self._loop.call_soon_threadsafe(self._loop.stop())
        


async def serve(ws, path):
    """ serve incoming client """

    m = re.match('^(.*)\/([^\/]+)$', path)
    if m != None:
        route, service_type = m.groups()

        # check if the route has created
        try:
            ctx = routes_service[route]
        except:
            # create a new route
            ctx = routes_service[route] = Service.init_service(service_type, ws)
            print('route %s created in %s mode'%(route, service_type))

        if ctx != None:
            await eval('Service.serve_'+service_type)(ctx, ws)
            print('id'+str(id(ws))+' '+path+' closed')
        else:
            print('reject bad connection')
        
    await ws.close()


if __name__ == '__main__':
    server = SimpleDataServer(9002)
    server.run()