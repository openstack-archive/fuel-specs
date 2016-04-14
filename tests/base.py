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

from __future__ import print_function

import glob
import io
import os
import re
import sys

import docutils.parsers.rst
import docutils.nodes
import testtools


def _rst2ast(source, name):
    parser = docutils.parsers.rst.Parser()
    document = docutils.utils.new_document(name)

    # unfortunately, those settings are mandatory to pass though
    # we don't care about their values
    document.settings.tab_width = 4
    document.settings.pep_references = 1
    document.settings.rfc_references = 1
    document.settings.trim_footnote_reference_space = 0
    document.settings.syntax_highlight = 0

    try:
        parser.parse(source, document)
    except Exception as exc:
        # we're interested in printing filename of reStructuredText document
        # that's failed to be parsed
        print(name, exc, file=sys.stderr)
        raise
    return document


class _RstSectionWrapper(object):

    def __init__(self, node):
        self._node = node

    @property
    def title(self):
        # there could be only one title subnode
        titles = filter(lambda n: n.tagname == 'title', self._node.children)
        return titles[0].astext()

    @property
    def subsections(self):
        sections = filter(
            lambda n: n.tagname == 'section', self._node.children)

        # wrapping subsections into this class would simplify further
        # working flow
        return [self.__class__(node) for node in sections]

    def get_subsection(self, title):
        for section in self.subsections:
            if section.title == title:
                return section
        return None


class _CheckLinesWrapping(docutils.nodes.NodeVisitor):
    """docutils' NodeVisitor for checking lines wrapping.

    Check that lines are wrapped into 79 characters. Exceptions are:

        * references;
        * code blocks;
        * footnodes;

    Usage example:

        document.walk(_CheckLinesWrapping(document))

    """

    def visit_title(self, node):
        for line in node.rawsource.splitlines():
            if len(line) >= 80:
                self._fail(node)

    def visit_footnote(self, node):
        raise docutils.nodes.SkipChildren()

    def visit_paragraph(self, node):
        ok = True

        for line in node.rawsource.splitlines():
            if len(line) >= 80:
                ok = False

                # breaking style guide, let's check for exceptions
                for child in node.traverse(include_self=False):
                    # references and code blocks are ok to be >= 80
                    if child.tagname in ('reference', 'literal'):
                        if len(child.rawsource) >= 80:
                            ok = True
                            break

                break

        if ok:
            raise docutils.nodes.SkipChildren()

        self._fail(node)

    def unknown_visit(self, node):
        pass

    def _get_line_no(self, node):
        line_no = node.line
        if line_no is None and node.parent:
            return self._get_line_no(node.parent)
        return line_no

    def _fail(self, node):
        line_no = self._get_line_no(node)
        raise ValueError(
            "%s:%d: Line limited to a maximum of 79 characters." %
            (node.source, line_no))


class BaseDocTest(testtools.TestCase):

    root = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

    def check_structure(self, filename, root):
        def do_check(filename, node, expected_node):
            expected_titles = expected_node.keys()
            real_titles = [section.title for section in node.subsections]

            for t in expected_titles:
                self.assertIn(t, real_titles, filename)

                expected_sub = expected_node[t]
                sub = node.get_subsection(t)

                if expected_sub is not None:
                    do_check(filename, sub, expected_sub)


        # Fuel Specs have only one top-level section, with the document
        # content. So we can pick it up and pass it down as document
        # root.
        node = _RstSectionWrapper(root).subsections[0]
        do_check(filename, node, self.expected_structure)

    def check_lines_wrapping(self, filename, root):
        root.walk(_CheckLinesWrapping(root))

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
            with io.open(filename, encoding='utf-8') as f:
                data = f.read()

            ast = _rst2ast(data, filename)

            self.check_structure(filename, ast)
            self.check_lines_wrapping(filename, ast)
            self.check_no_cr(filename, data)
