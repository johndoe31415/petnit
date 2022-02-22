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

import logging
import subprocess
from petnit.BaseModule import BaseModule
from petnit.Tools import IPTools

_log = logging.getLogger(__spec__.name)

@BaseModule.register("dnsmasq")
class DNSMasqModule(BaseModule):
	def start(self):
		interface = self._ctrlr.config["interfaces"]["dut"]
		ifinfo = IPTools.get_interface(interface)

		netrange = ifinfo["addresses"][0]
		dhcp_begin = netrange["net"][100]
		dhcp_end = netrange["net"][150]
		_log.info("Starting dnsmasq on %s with DHCP range from %s to %s", interface, dhcp_begin, dhcp_end)

		config_filename = self._ctrlr.session.tempdir("dnsmasq") + "/dnsmasq.conf"
		self._leasefile = self._ctrlr.session.tempdir("dnsmasq") + "/leases.txt"

		with open(config_filename, "w") as f:
			print("interface=%s" % (interface), file = f)
			print("bind-interfaces", file = f)
			print("dhcp-range=%s,%s,12h" % (dhcp_begin, dhcp_end), file = f)
			print("dhcp-leasefile=%s" % (self._leasefile), file = f)

		self._proc = subprocess.Popen([ "dnsmasq", "-C", config_filename, "-k" ], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

	def stop(self):
		self._proc.kill()
