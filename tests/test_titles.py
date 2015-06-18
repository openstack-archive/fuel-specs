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


class TestTitles(testtools.TestCase):

    def _build_structure(self, spec):
        section = {}
        name = ''

        for node in spec:
            if node.tagname == 'title':
                name = node.rawsource
            elif node.tagname == 'section':
                subsection, subsection_name = self._build_structure(node)
                section[subsection_name] = subsection

        return section, name

    def _check_titles(self, fname, titles):
        expected_titles = ('Problem description', 'Proposed changes',
                           'Alternatives', 'Upgrade impact', 'Security impact',
                           'End user impact', 'Performance impact',
                           'Deployment impact', 'Developer impact',
                           'Infrastructure/operations impact',
                           'Notifications impact',
                           'Documentation impact', 'Expected OSCI impact',
                           'Implementation', 'Testing, QA', 'References')

        self.assertEqual(sorted(expected_titles),
                         sorted(titles.keys()),
                         'Expected titles not found in document %s' % fname)

        proposed = titles['Proposed changes'].keys()

        self.assertIn('Web UI', proposed)
        self.assertIn('Nailgun', proposed)
        self.assertIn('Orchestration', proposed)
        self.assertIn('Fuel Client', proposed)
        self.assertIn('Plugins', proposed)
        self.assertIn('Fuel Library', proposed)

        impl = titles['Implementation'].keys()

        self.assertIn('Assignee(s)', impl)
        self.assertIn('Dependencies', impl)
        self.assertIn('Work Items', impl)

        test = titles['Testing, QA'].keys()
        self.assertIn('Acceptance criteria', test)

        # Check required subtopics for Nailgun, Orchestration
        nailgun = titles['Proposed changes']['Nailgun'].keys()
        self.assertIn('Data model', nailgun)
        self.assertIn('REST API', nailgun)

        orc = titles['Proposed changes']['Orchestration'].keys()
        self.assertIn('RPC Protocol', orc)

    def _check_lines_wrapping(self, tpl, raw):
        for i, line in enumerate(raw.split('\n')):
            if 'http://' in line or 'https://' in line:
                continue
            self.assertTrue(
                len(line.decode("utf-8")) < 80,
                msg="%s:%d: Line limited to a maximum of 79 characters." %
                (tpl, i+1))

    def _check_no_cr(self, tpl, raw):
        matches = re.findall('\r', raw)
        self.assertEqual(
            len(matches), 0,
            'Found %s literal carriage returns in file %s' %
            (len(matches), tpl))

    def test_template(self):
        files = ['specs/template.rst']
        versions = ('8.0',)

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
            document, name = self._build_structure(spec)
            self._check_titles(filename, document)
            self._check_lines_wrapping(filename, data)
            self._check_no_cr(filename, data)
