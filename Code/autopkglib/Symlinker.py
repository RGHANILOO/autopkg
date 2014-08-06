#!/usr/bin/python
#
# Copyright 2013 Greg Neagle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from autopkglib import Processor, ProcessorError


__all__ = ["Symlinker"]


class Symlinker(Processor):
    description = "Copies source_path to destination_path."
    input_variables = {
        "source_path": {
            "required": True,
            "description": "Path to a file or directory to symlink.",
        },
        "destination_path": {
            "required": True,
            "description": "Path to destination.",
        },
        "overwrite": {
            "required": False,
            "description":
                "Whether the destination will be overwritten if necessary.",
        },
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        source_path = self.env['source_path']
        destination_path  = self.env['destination_path']

        # Remove destination if needed.
        if os.path.exists(destination_path):
            if "overwrite" in self.env and self.env['overwrite']:
                try:
                    os.unlink(destination_path)
                except OSError as e:
                    raise ProcessorError(
                        "Can't remove %s: %s" % (destination_path, e.strerror))

        # Make symlink.
        try:
            os.symlink(source_path, destination_path)
            self.output("Symlinked %s to %s"
                        % (source_path, destination_path))
        except BaseException as e:
            raise ProcessorError("Can't symlink %s to %s: %s"
                                 % (source_path, destination_path, e))


if __name__ == '__main__':
    processor = Symlinker()
    processor.execute_shell()

