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

from io import BytesIO
from ._transport import _AbstractTransport
from .constants import WEBSOCKET_PORT, AMQP_WS_SUBPROTOCOL
from websocket import create_connection

class WebSocketTransport(_AbstractTransport):
    def __init__(self, host, port=WEBSOCKET_PORT, connect_timeout=None, ssl=None, **kwargs):
        self.sslopts = ssl if isinstance(ssl, dict) else {}
        self._connect_timeout = connect_timeout or 1
        self._host = host
        super().__init__(
            host, port, connect_timeout, **kwargs
            )
        self.ws = None
        self._http_proxy = kwargs.get('http_proxy', None)

    def connect(self):
        http_proxy_host, http_proxy_port, http_proxy_auth = None, None, None
        if self._http_proxy:
            http_proxy_host = self._http_proxy['proxy_hostname']
            http_proxy_port = self._http_proxy['proxy_port']
            username = self._http_proxy.get('username', None)
            password = self._http_proxy.get('password', None)
            if username or password:
                http_proxy_auth = (username, password)
        try:
            self.ws = create_connection(
                url="wss://{}".format(self._host),
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

    def _read(self, n, initial=False, buffer=None, **kwargs):  # pylint: disable=unused-arguments
        """Read exactly n bytes from the peer."""
        from websocket import WebSocketTimeoutException

        length = 0
        view = buffer or memoryview(bytearray(n))
        nbytes = self._read_buffer.readinto(view)
        length += nbytes
        n -= nbytes
        try:
            while n:
                data = self.ws.recv()

                if len(data) <= n:
                    view[length: length + len(data)] = data
                    n -= len(data)
                else:
                    view[length: length + n] = data[0:n]
                    self._read_buffer = BytesIO(data[n:])
                    n = 0
            return view
        except WebSocketTimeoutException:
            raise TimeoutError()

    def _shutdown_transport(self):
        """Do any preliminary work in shutting down the connection."""
        self.ws.close()

    def _write(self, s):
        """Completely write a string to the peer.
        ABNF, OPCODE_BINARY = 0x2
        See http://tools.ietf.org/html/rfc5234
        http://tools.ietf.org/html/rfc6455#section-5.2
        """
        self.ws.send_binary(s)
