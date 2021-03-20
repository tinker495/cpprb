import unittest

import numpy as np

from cpprb import ReplayBuffer, PrioritizedReplayBuffer


class TestReplayBuffer(unittest.TestCase):
    def test_basic(self):
        """
        Basic Test Case

        Loaded buffer have same transitions with saved one.
        """
        buffer_size = 4
        env_dict = {"a": {}}

        rb1 = ReplayBuffer(buffer_size, env_dict)
        rb2 = ReplayBuffer(buffer_size, env_dict)

        a = [1, 2, 3, 4]

        rb1.add(a=a)

        fname = "basic.npz"
        rb1.save_transitions(fname)
        rb2.load_transitions(fname)

        t1 = rb1.get_all_transitions()
        t2 = rb2.get_all_transitions()

        np.testing.assert_allclose(t1["a"], t2["a"])

    def test_smaller_buffer(self):
        """
        Load to smaller buffer

        Loaded buffer only stored last buffer_size transitions
        """
        buffer_size1 = 10
        buffer_size2 = 4
        env_dict = {"a": {}}

        rb1 = ReplayBuffer(buffer_size1, env_dict)
        rb2 = ReplayBuffer(buffer_size2, env_dict)

        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        fname = "smaller.npz"
        rb1.save_transitions(fname)
        rb2.load_transitions(fname)

        t1 = rb1.get_all_transitions()
        t2 = rb2.get_all_transitions()

        np.testing.assert_allclose(t1["a"][-buffer_size2:],t2["a"])

    def test_load_to_filled_buffer(self):
        """
        Load to already filled buffer

        Add to transitions
        """
        buffer_size1 = 10
        buffer_size2 = 10
        env_dict = {"a": {}}

        rb1 = ReplayBuffer(buffer_size1, env_dict)
        rb2 = ReplayBuffer(buffer_size2, env_dict)

        a = [1, 2, 3, 4]
        b = [5, 6]

        rb1.add(a=a)
        rb2.add(a=b)

        fname="filled.npz"
        rb1.save_transitions(fname)
        rb2.load_transitions(fname)

        t1 = rb1.get_all_transitions()
        t2 = rb2.get_all_transitions()

        np.testing.assert_allclose(t1["a"], t2["a"][len(b):])

if __name__ == "__main__":
    unittest.main()
