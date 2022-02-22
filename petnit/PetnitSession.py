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

import tempfile
import contextlib
import os
import datetime

class PetnitSession():
	def __init__(self, ctrlr):
		self._ctrlr = ctrlr
		self._tempdir = tempfile.TemporaryDirectory(prefix = "petnit_")
		self._start_ts = datetime.datetime.utcnow()

	def persistent_file(self, pathname):
		dirname = self._ctrlr.config["sessions"] + "/" + self._start_ts.strftime("%Y_%m_%d_%H_%M_%S") + "/"
		with contextlib.suppress(FileExistsError):
			os.makedirs(dirname)
		return dirname + pathname

	def tempdir(self, name):
		dirname = self._tempdir.name + "/" + name
		with contextlib.suppress(FileExistsError):
			os.makedirs(dirname)
		return dirname

	def close(self):
		self._tempdir.cleanup()
