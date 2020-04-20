from unittest import TestCase

from config.utils import merge_dicts


class TestMerge(TestCase):

    def test_should_merge_deep_dicts(self):
        # given
        a_dict = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
        b_dict = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}
        # when
        merged = dict(merge_dicts(a_dict, b_dict))
        # then
        expected = {'first': {'all_rows': {'pass': 'dog', 'fail': 'cat', 'number': '5'}}}

        self.assertEqual(expected, merged)
