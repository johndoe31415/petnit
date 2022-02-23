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

import json
import time
from .BaseModule import BaseModule
from .PetnitSession import PetnitSession
import petnit.modules

class PetnitController():
	def __init__(self, args):
		self._args = args
		with open(self._args.config_file) as f:
			self._config = json.load(f)
		self._session = PetnitSession(self)
		self._running = { }

	@property
	def config(self):
		return self._config

	@property
	def session(self):
		return self._session

	def start_module(self, name, args = None):
		if self._running.get("name") is not None:
			raise Exception("Module %s is already running." % (name))

		if args is None:
			args = { }
		self._running[name] = BaseModule.instanciate(name, self, args)
		self._running[name].start()

	def stop_module(self, name):
		mod = self._running.get(name)
		if mod is not None:
			mod.stop()
			self._running[name] = None

	def stop_all_modules(self):
		for mod in self._running:
			self.stop_module(mod)

	def lookup_module(self, name, args = None):
		if args is None:
			args = { }
		if name not in self._config.get("module_aliases", { }):
			yield (name, args)
		else:
			for surrogate in self._config["module_aliases"][name]:
				yield from self.lookup_module(name = surrogate["name"], args = surrogate.get("args"))

	def run(self):
		try:
			if len(self._args.module) == 0:
				module_src = self.config["default_modules"]
			else:
				module_src = self._args.module
			for module_def in module_src:
				src_module_name = module_def["name"]
				src_module_args = module_def.get("args", { })
				for (module_name, module_args) in self.lookup_module(src_module_name, src_module_args):
					self.start_module(module_name, args = module_args)
			while True:
				time.sleep(1)
		finally:
			self.stop_all_modules()
			self._session.close()
