"""Jsonification Functions for python-mssqlclient."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mock

from datetime import datetime

from mssqlcli import formats


def test_stringify_on_basic_dict():
    obj = {'now': datetime(2016, 10, 20, 21, 10, 36, 621341)}
    assert formats.stringify(obj) == {
        'now': '2016-10-20 21:10:36.621341'
    }


def test_stringify_on_basic_list():
    obj = [datetime(2016, 10, 20, 21, 10, 36, 621341)]
    assert formats.stringify(obj) == [
        '2016-10-20 21:10:36.621341'
    ]


def test_stringify_on_nested_dict():
    obj = {
        "top_level": {
            "now": datetime(2016, 10, 20, 21, 10, 36, 621341)
        }
    }
    assert formats.stringify(obj) == {
        "top_level": {
            "now": '2016-10-20 21:10:36.621341'
        }
    }


def test_stringify_on_nested_list():
    obj = {'nows': [datetime(2016, 10, 20, 21, 10, 36, 621341)]}
    assert formats.stringify(obj) == {'nows': ['2016-10-20 21:10:36.621341']}


expected_plaintext_json_response = """{
    "results": {
        "now": "2016-10-20 21:10:36.621341"
    }
}"""


def test_jsonify_no_pygments():
    obj = {'now': datetime(2016, 10, 20, 21, 10, 36, 621341)}
    with mock.patch.dict('sys.modules', {'pygments': None}):
        assert formats.jsonify(obj) == expected_plaintext_json_response


expected_pygments_json_response = (
    '{\n    \x1b[34;01m"results"\x1b[39;49;00m: {\n'
    '        \x1b[34;01m"now"\x1b[39;49;00m: \x1b[33m'
    '"2016-10-20 21:10:36.621341"\x1b[39;49;00m\n    }\n}\n'
)


def test_jsonify_with_pygments():
    obj = {'now': datetime(2016, 10, 20, 21, 10, 36, 621341)}
    assert formats.jsonify(obj) == expected_pygments_json_response


expected_csv_outputs = [
    (
        'one,two\r\n'
        'red,blue\r\n'
        '2016-10-20 21:10:36.621341,black\r\n'
    ),
    (
        'two,one\r\n'
        'blue,red\r\n'
        'black,2016-10-20 21:10:36.621341\r\n'
    )
]


def test_csvify():
    obj = [
        {
            "one": "red",
            "two": "blue"
        },
        {
            "one": datetime(2016, 10, 20, 21, 10, 36, 621341),
            "two": "black"
        }
    ]
    assert formats.csvify(obj) in expected_csv_outputs