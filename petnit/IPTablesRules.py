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

import uuid
import subprocess
import re

class IPTablesRules():
	def __init__(self):
		self._rid = str(uuid.uuid4())
		self._remove_regex = re.compile(r"^(?P<rulenum>\d+)\s+.*/\* petnit-%s \*/$" % (self._rid), flags = re.MULTILINE)
		self._modified = set()

	def add(self, table, chain, cmd):
		self._modified.add((table, chain))
		cmd = [ "iptables", "-t", table, "-A", chain, "-m", "comment", "--comment", "petnit-%s" % (self._rid) ] + cmd
		subprocess.check_call(cmd)

	def _remove_all_from(self, table, chain):
		output = subprocess.check_output([ "iptables", "-t", table, "-L", chain, "--line-numbers" ]).decode()
		rules = [ ]
		for match in self._remove_regex.finditer(output):
			match = match.groupdict()
			rulenum = int(match["rulenum"])
			rules.append(rulenum)

		for rulenum in reversed(rules):
			subprocess.check_call([ "iptables", "-t", table, "-D", chain, str(rulenum) ])

	def remove_all(self):
		for (table, chain) in self._modified:
			self._remove_all_from(table, chain)
		self._modified = set()

if __name__ == "__main__":
	iptr = IPTablesRules()
	iptr.add("nat", "INPUT", [ "-d", "1.2.3.4", "-j", "ACCEPT" ])
	iptr.remove_all()
