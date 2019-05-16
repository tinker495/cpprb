import unittest

import numpy as np

from cpprb import ReplayBuffer as nowReplayBuffer
from cpprb.experimental import ReplayBuffer,PrioritizedReplayBuffer

class TestExperimentalReplayBuffer(unittest.TestCase):
    def test_buffer(self):

        buffer_size = 256
        obs_shape = (15,15)
        act_dim = 5

        N = 512

        rb = nowReplayBuffer(buffer_size,obs_shape=obs_shape,act_dim=act_dim)
        erb = ReplayBuffer(buffer_size,{"obs":{"shape": obs_shape},
                                        "act":{"shape": act_dim},
                                        "rew":{},
                                        "next_obs":{"shape": obs_shape},
                                        "done":{}})

        for i in range(N):
            obs = np.full(obs_shape,i,dtype=np.double)
            act = np.full(act_dim,i,dtype=np.double)
            rew = i
            next_obs = obs + 1
            done = 0

            rb.add(obs,act,rew,next_obs,done)
            erb.add(obs=obs,act=act,rew=rew,next_obs=next_obs,done=done)

        s = rb._encode_sample(range(buffer_size))
        es = erb._encode_sample(range(buffer_size))

        np.testing.assert_allclose(s["obs"],es["obs"])
        np.testing.assert_allclose(s["act"],es["act"])
        np.testing.assert_allclose(s["rew"],es["rew"])
        np.testing.assert_allclose(s["next_obs"],es["next_obs"])
        np.testing.assert_allclose(s["done"],es["done"])

        erb.sample(32)

    def test_add(self):
        buffer_size = 256
        obs_shape = (15,15)
        act_dim = 5

        rb = ReplayBuffer(buffer_size,env_dict={"obs":{"shape": obs_shape},
                                                "act":{"shape": act_dim},
                                                "rew":{},
                                                "next_obs": {"shape": obs_shape},
                                                "done": {}})

        self.assertEqual(rb.get_next_index(),0)
        self.assertEqual(rb.get_stored_size(),0)

        obs = np.zeros(obs_shape)
        act = np.ones(act_dim)
        rew = 1
        next_obs = obs + 1
        done = 0

        rb.add(obs=obs,act=act,rew=rew,next_obs=next_obs,done=done)

        self.assertEqual(rb.get_next_index(),1)
        self.assertEqual(rb.get_stored_size(),1)

        with self.assertRaises(KeyError):
            rb.add(obs=obs)

        self.assertEqual(rb.get_next_index(),1)
        self.assertEqual(rb.get_stored_size(),1)

if __name__ == '__main__':
    unittest.main()
