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

class BaseModule():
	_CLASSES = { }

	def __init__(self, ctrlr, args):
		self._ctrlr = ctrlr
		self._args = args

	def start(self):
		pass

	def stop(self):
		pass

	@classmethod
	def instanciate(cls, name, ctrlr, args = None):
		return cls._CLASSES[name](ctrlr, args)

	@classmethod
	def register(cls, module_name):
		def decorator(decoree_class):
			cls._CLASSES[module_name] = decoree_class
			return decoree_class
		return decorator
