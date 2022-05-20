#-------------------------------------------------------------------------
# This is a fork of the transport.py which was originally written by Barry Pederson and
# maintained by the Celery project: https://github.com/celery/py-amqp.
#
# Copyright (C) 2009 Barry Pederson <bp@barryp.org>
#
# The license text can also be found here:
# http://www.opensource.org/licenses/BSD-3-Clause
#
# License
# =======
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------
import asyncio
import logging
from io import BytesIO
from ._transport_async import AsyncTransportMixin
from ..constants import WEBSOCKET_PORT, AMQP_WS_SUBPROTOCOL
from .._websocket_transport import WebSocketTransport

_LOGGER = logging.getLogger(__name__)

def get_running_loop():
    try:
        import asyncio  # pylint: disable=import-error
        return asyncio.get_running_loop()
    except AttributeError:  # 3.6
        loop = None
        try:
            loop = asyncio._get_running_loop()  # pylint: disable=protected-access
        except AttributeError:
            _LOGGER.warning('This version of Python is deprecated, please upgrade to >= v3.6')
        if loop is None:
            _LOGGER.warning('No running event loop')
            loop = asyncio.get_event_loop()
        return loop


class WebSocketTransportAsync(AsyncTransportMixin):
    def __init__(self, host, port=WEBSOCKET_PORT, connect_timeout=None, ssl=None, **kwargs
        ):
        self._read_buffer = BytesIO()
        self.loop = get_running_loop()
        self.socket_lock = asyncio.Lock()
        self.sslopts = ssl if isinstance(ssl, dict) else {}
        self._connect_timeout = connect_timeout or 1
        self.host = host
        self.ws = None
        self._http_proxy = kwargs.get('http_proxy', None)

    async def connect(self):
        http_proxy_host, http_proxy_port, http_proxy_auth = None, None, None
        if self._http_proxy:
            http_proxy_host = self._http_proxy['proxy_hostname']
            http_proxy_port = self._http_proxy['proxy_port']
            username = self._http_proxy.get('username', None)
            password = self._http_proxy.get('password', None)
            if username or password:
                http_proxy_auth = (username, password)
        try:
            from websocket import create_connection
            self.ws = create_connection(
                url="wss://{}".format(self.host),
                subprotocols=[AMQP_WS_SUBPROTOCOL],
                timeout=self._connect_timeout,
                skip_utf8_validation=True,
                sslopt=self.sslopts,
                http_proxy_host=http_proxy_host,
                http_proxy_port=http_proxy_port,
                http_proxy_auth=http_proxy_auth
            )
        except ImportError:
            raise ValueError("Please install websocket-client library to use websocket transport.")

    async def _read(self, n, buffer=None, **kwargs): # pylint: disable=unused-arguments
        """Read exactly n bytes from the peer."""
        from websocket import WebSocketTimeoutException

        length = 0
        view = buffer or memoryview(bytearray(n))
        nbytes = self._read_buffer.readinto(view)
        length += nbytes
        n -= nbytes
        try:
            while n:
                data = await self.loop.run_in_executor(
                    None, self.ws.recv
                )

                if len(data) <= n:
                    view[length: length + len(data)] = data
                    n -= len(data)
                else:
                    view[length: length + n] = data[0:n]
                    self._read_buffer = BytesIO(data[n:])
                    n = 0

            return view 
        except WebSocketTimeoutException as wex:
            raise TimeoutError()

    def close(self):
        """Do any preliminary work in shutting down the connection."""
        # TODO: async close doesn't:
        # 1) shutdown socket and close. --> self.sock.shutdown(socket.SHUT_RDWR) and self.sock.close()
        # 2) set self.connected = False
        # I think we need to do this, like in sync
        self.ws.close()

    async def write(self, s):
        """Completely write a string to the peer.
        ABNF, OPCODE_BINARY = 0x2
        See http://tools.ietf.org/html/rfc5234
        http://tools.ietf.org/html/rfc6455#section-5.2
        """
        await self.loop.run_in_executor(
                None, self.ws.send_binary, s
                )
