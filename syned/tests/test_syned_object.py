from collections import OrderedDict
import pytest
from syned.syned_object import SynedObject

@pytest.mark.parametrize("text,expected", [
    ([("mock_index_1", "first_result", "second_result")], OrderedDict(mock_index_1=("first_result", "second_result"))),
    ([("mock_index_2", "third_result", "forth_result")], OrderedDict(mock_index_2=("third_result", "forth_result"))),
    ([("mock_index_3", "fifth_result", "sixth_result")], OrderedDict(mock_index_3=("fifth_result", "sixth_result"))),
])
def test_set_support_text(text, expected):
    syned_object = SynedObject()
    syned_object._set_support_text(text)
    assert syned_object._support_dictionary == expected
