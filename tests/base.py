# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import glob
import re

import docutils.core
import testtools


class BaseDocTest(testtools.TestCase):

    def build_structure(self, spec):
        section = {}
        name = ''

        for node in spec:
            if node.tagname == 'title':
                name = node.rawsource
            elif node.tagname == 'section':
                subsection, subsection_name = self.build_structure(node)
                section[subsection_name] = subsection

        return section, name

    def verify_structure(self, fname, struct,
                         expected_struct, supersection=None):
        expected_titles = expected_struct.keys()
        real_titles = struct.keys()

        for t in expected_titles:
            self.assertIn(t, real_titles)

            substruct = expected_struct[t]

            if substruct is not None:
                self.verify_structure(fname, struct[t], substruct, t)

    def check_lines_wrapping(self, tpl, raw):
        for i, line in enumerate(raw.split('\n')):
            if 'http://' in line or 'https://' in line:
                continue
            self.assertTrue(
                len(line.decode("utf-8")) < 80,
                msg="%s:%d: Line limited to a maximum of 79 characters." %
                (tpl, i+1))

    def check_no_cr(self, tpl, raw):
        matches = re.findall('\r', raw)
        self.assertEqual(
            len(matches), 0,
            'Found %s literal carriage returns in file %s' %
            (len(matches), tpl))

    def test_template(self):
        files = self.files
        versions = self.versions

        for v in versions:
            files.extend(glob.glob('specs/%s/*' % v))

        # filtering images subdirectory
        files = filter(lambda x: 'images' not in x, files)
        for filename in files:
            self.assertTrue(filename.endswith('.rst'),
                            'Specification files must use .rst extensions.')
            with open(filename) as f:
                data = f.read()

            spec = docutils.core.publish_doctree(data)
            document, name = self.build_structure(spec)
            self.verify_structure(filename, document, self.expected_structure)
            self.check_lines_wrapping(filename, data)
            self.check_no_cr(filename, data)
