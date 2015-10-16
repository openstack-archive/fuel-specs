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

from tests import base

class TestTitles(base.BaseDocTest):
    expected_structure = {
        'Problem description': None,
        'Proposed changes': {
            'Web UI': None,
            'Nailgun': {
                'Data model': None,
                'REST API': None
            },
            'Orchestration': {
                'RPC Protocol': None
            },
            'Fuel Client': None,
            'Fuel Library': None
        },
        'Alternatives': None,
        'Upgrade impact': None,
        'Security impact': None,
        'End user impact': None,
        'Performance impact': None,
        'Deployment impact': None,
        'Developer impact': None,
        'Infrastructure impact': None,
        'Notifications impact': None,
        'Documentation impact': None,
        'Implementation': {
            'Assignee(s)': None,
            'Dependencies': None,
            'Work Items': None
        },
        'Testing, QA': {
            'Acceptance criteria': None
        },
        'References': None
    }

    files = ['specs/template.rst']
    versions = ('8.0',)
