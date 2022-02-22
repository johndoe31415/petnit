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

_log = logging.getLogger(__spec__.name)

@BaseModule.register("tcpdump")
class TCPDumpModule(BaseModule):
	def start(self):
		interface = self._ctrlr.config["interfaces"]["dut"]
		filesize_mb = 10
		_log.info("Starting tcpdump on %s, maximum PCAP filesize %d MB", interface, filesize_mb)

		procout = None if _log.isEnabledFor(logging.DEBUG) else subprocess.DEVNULL
		self._proc = subprocess.Popen([ "tcpdump", "-n", "-s", "0", "--packet-buffered", "-C", str(filesize_mb), "-w", self._ctrlr.session.persistent_file("packet_dump.pcap") ], stdout = procout, stderr = procout)

	def stop(self):
		self._proc.kill()
