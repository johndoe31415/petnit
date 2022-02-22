#	petnit - Penetration testing network interception tool
#	Copyright (C) 2022-2022 Johannes Bauer
#
#	This file is part of petnit.
#
#	petnit is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	petnit is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with petnit; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import re
import subprocess
import ipaddress

class IPTools():
	_ADDR_RE = re.compile(r"^\s+inet6? (?P<net>(?P<ip>[^/]+)/\d+).*\sscope global", flags = re.MULTILINE)

	@classmethod
	def get_interface(cls, ifname):
		cmd = subprocess.check_output([ "ip", "a", "show", "dev", ifname ]).decode()
		info = {
			"name": ifname,
			"addresses": [ ],
		}
		for match in cls._ADDR_RE.finditer(cmd):
			match = match.groupdict()
			addrinfo = {
				"net": ipaddress.ip_network(match["net"], strict = False),
				"addr": ipaddress.ip_address(match["ip"]),
			}
			info["addresses"].append(addrinfo)
		return info
