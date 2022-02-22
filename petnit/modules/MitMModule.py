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
from petnit.IPTablesRules import IPTablesRules

_log = logging.getLogger(__spec__.name)

@BaseModule.register("mitm")
class MitMModule(BaseModule):
	def _set_local_net_forward(value):
		with open("/proc/sys/net/ipv4/conf/all/route_localnet", "w") as f:
			print(str(value), file = f)

	def start(self):
		mitm_hosts = [ ]
		target_ports = [ 443 ]
		interface = self._ctrlr.config["interfaces"]["dut"]
		_log.info("Starting MitM on %s for hosts %s and target ports %s", interface, mitm_hosts, target_ports)

		cmd = [ "ratched" ]
		if len(mitm_hosts) > 0:
			# intercept selectively
			cmd += [ "--defaults", "intercept=forward" ]
			for hostname in mitm_hosts:
				cmd += [ "--intercept", hostname ]
		cmd += [ "-o", self._ctrlr.session.persistent_file("mitm.pcapng") ]

		procout = None if _log.isEnabledFor(logging.DEBUG) else subprocess.DEVNULL
		self._proc = subprocess.Popen(cmd, stdout = procout, stderr = procout)

		self._set_local_net_forward("1")
		self._ipt = IPTablesRules()
		for target_port in target_ports:
			self._ipt.add("nat", "PREROUTING", [ "-i", interface, "-p", "tcp", "--dport", str(target_port), "-j", "DNAT", "--to", "127.0.0.1:9999" ])

	def stop(self):
		self._ipt.remove_all()
		self._proc.kill()
		self._set_local_net_forward("0")
