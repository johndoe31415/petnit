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
from petnit.IPTablesRules import IPTablesRules
from petnit.BaseModule import BaseModule

_log = logging.getLogger(__spec__.name)

@BaseModule.register("masquerade")
class MasqueradeModule(BaseModule):
	@staticmethod
	def _set_ipv4_forward(value):
		with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
			print(str(value), file = f)

	def start(self):
		output_interface = self._args.get("output_interface", self._ctrlr.config["interfaces"]["egress"])
		_log.info("Enabling IP masquerading with egress interface %s", output_interface)
		self._set_ipv4_forward("1")
		self._rules = IPTablesRules()
		self._rules.add("nat", "POSTROUTING", [ "-o", output_interface, "-j", "MASQUERADE" ])

	def stop(self):
		self._set_ipv4_forward("0")
		self._rules.remove_all()
