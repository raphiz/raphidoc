import os
import subprocess
import collections

from raphidoc import utils


def test_is_in_path():
    # Assuning, ls and cat are allways in the path (VERY UGLY :( )
    assert utils.is_in_path('ls', 'cat')


def test_is_not_in_path():
    # Assuning, ls and cat are allways in the path (VERY UGLY :( )
    assert not utils.is_in_path('ls', 'cat', 'lkajdslkasdlkajsdjadslkjasldjlkajsdl')


def test_is_not_in_path():
    assert not utils.is_in_path('lkajdslkasdlkajsdjadslkjasldjlkajsdl')


def test_wkhtmltopdf(mocker):
    # Patch subprocess - since we want to verify the command that was actually called
    class MockProcess():
        def communicate(self):
            return '\n'.encode(), '\n'.encode()
    mocker.patch('subprocess.Popen', return_value=MockProcess())

    # Setup an ordered config, to be able to verify the call
    config = collections.OrderedDict(
        sorted({'javascript-delay': 200, 'margin-bottom': '2cm', 'flags': ['outline']}.items(),
               key=lambda t: t[0]))

    utils.wkhtmltopdf(config, 'foo.html', 'baa.pdf')

    subprocess.Popen.assert_called_once_with(['wkhtmltopdf', '--outline', '--javascript-delay',
                                              '200', '--margin-bottom', '2cm',
                                              'foo.html', 'baa.pdf'],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
['wkhtmltopdf', '--outline', '--margin-bottom', '2cm', '--javascript-delay', '200', 'foo.html', 'baa.pdf']
['wkhtmltopdf', '--outline', '--javascript-delay', '200', '--margin-bottom', '2cm', 'foo.html', 'baa.pdf']
