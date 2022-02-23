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

import sys
import logging
import json
from .FriendlyArgumentParser import FriendlyArgumentParser
from .PetnitController import PetnitController

def _modname_params(text):
	if ":" not in text:
		return (text, None)
	else:
		(module_name, module_args_json)  = text.split(":", maxsplit = 1)
		module_args = json.loads(module_args_json)
		return (module_name, module_args)

def main():
	parser = FriendlyArgumentParser(description = "petnit: pentesting network interception tool.")
	parser.add_argument("-m", "--module", type = _modname_params, metavar = "modname[:jsonparams]", action = "append", default = [ ], help = "Module to start. Can also contain a colon that separates its arguments (JSON encoded). This can be given multiple times. If omitted, the default modules from the configuration file are used.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	parser.add_argument("config_file", nargs = "?", default = "petnit.json", help = "JSON petnit configuration file. Defaults to %(default)s.")
	args = parser.parse_args(sys.argv[1:])

	if args.verbose == 0:
		loglevel = logging.WARN
	elif args.verbose == 1:
		loglevel = logging.INFO
	else:
		loglevel = logging.DEBUG
	logging.basicConfig(format = "{name:>40s} [{levelname:.1s}]: {message}", style = "{", level = loglevel)

	pnc = PetnitController(args)
	pnc.run()

if __name__ == "__main__":
	main()
