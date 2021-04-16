#!/usr/bin/python
#
# Copyright 2016 James Reynolds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for VariableFromPath class"""

import os.path
import re

from autopkglib import Processor, ProcessorError
from glob import glob

__all__ = ["VariableFromPath"]


class VariableFromPath(Processor):
	"""Returns version information from a path"""
	description = __doc__

	input_variables = {
		"re_pattern": {
			"required": True,
			"description":
				("Regular expression (Python) to match against the found path."),
		},
		"input_path": {
			"required": True,
			"description":
				("File path to a file or directory (can be a glob)."),
		},
		'result_output_var_name': {
			'description': ('The name of the output variable that is returned '
							'by the match. If not specified then a default of '
							'"match" will be used.'),
			'required': False,
			'default': 'match',
		},
		're_flags': {
			'description': ('Optional array of strings of Python regular '
							'expression flags. E.g. IGNORECASE.'),
			'required': False,
		},
	}
	output_variables = {
		'result_output_var_name': {
			'description': (
				'First matched sub-pattern from input found on the fetched '
				'URL. Note the actual name of variable depends on the input '
				'variable "result_output_var_name" or is assigned a default of '
				'"match."')
		}
	}

	def search_path(self, path, re_pattern, flags=None):
		'''Search path for re_pattern'''
		flag_accumulator = 0
		if flags:
			for flag in flags:
				if flag in re.__dict__:
					flag_accumulator += re.__dict__[flag]

		re_compiled = re.compile(re_pattern, flags=flag_accumulator)

		match = re_compiled.search(path)

		if not match:
			raise ProcessorError('No match found on path: %s' % path)

# 		print('VariableFromPath match: %s' % (match.group(match.lastindex or 0)))

		# return the last matched group with the dict of named groups
		return (match.group(match.lastindex or 0), match.groupdict() )

	def main(self):
		"""Return a version for file at input_plist_path"""
		matches = glob(self.env['input_path'])
		if len(matches) == 0:
			raise ProcessorError(
				"Error processing path '%s' with glob. " % self.env['input_path'])
		matched_source_path = matches[0]

		self.output('Found path %s' % matched_source_path)

		if not os.path.exists(matched_source_path):
			raise ProcessorError(
				"Path '%s' does not exist or could not be read." %
				matched_source_path)

		flags = self.env.get('re_flags', {})
		groupmatch, groupdict = self.search_path(matched_source_path, self.env['re_pattern'],
			flags)

		# favor a named group over a normal group match
		output_var_name = self.env['result_output_var_name']
		self.output('output_var_name %s' % output_var_name)

		if output_var_name not in groupdict.keys():
			groupdict[output_var_name] = groupmatch

		self.output_variables = {}
		for key in groupdict.keys():
			self.env[key] = groupdict[key]
			self.output('Found matching text (%s): %s' % (key, self.env[key], ))
			self.output_variables[key] = {
				'description': 'Matched regular expression group'}

if __name__ == '__main__':
	processor = VariableFromPath()
	processor.execute_shell()

