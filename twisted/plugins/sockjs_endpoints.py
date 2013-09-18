# Copyright (c) 2012, Christopher Gamble
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Christopher Gamble nor the names of its 
#      contributors may be used to endorse or promote products derived 
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.internet.interfaces import IStreamServerEndpointStringParser, IStreamServerEndpoint
from twisted.internet.endpoints import serverFromString
from txsockjs.factory import SockJSFactory

def escape(s):
	return s.replace('\\', '\\\\').replace(':', '\\:').replace('=', '\\=')

class SockJSServerParser(object):
	implements(IPlugin, IStreamServerEndpointStringParser)

	prefix = "sockjs"

	def parseStreamServer(self, reactor, *args, **kwargs):
		args = [escape(x) for x in args]

		sockjs_kwargs = {}
		for k,v in kwargs.items():
			if k.startswith("sockjs_"):
				sockjs_kwargs[k[7:]] = v
			else:
				args.append(escape(k) + "=" + escape(v))

		description = ":".join(args)
		endpoint = serverFromString(reactor, description)

		return SockJSServerEndpoint(endpoint, sockjs_kwargs)

class SockJSServerEndpoint(object):
	implements(IPlugin, IStreamServerEndpoint)

	def __init__(self, endpoint, options):
		self._endpoint = endpoint
		self._options = options

	def listen(self, protocolFactory):
		return self._endpoint.listen(SockJSFactory(protocolFactory, self._options))

SockJSServerParserInstance = SockJSServerParser()
