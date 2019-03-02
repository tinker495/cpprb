import numpy as np
import unittest, time
from multiprocessing import Process
from cpprb import *

def timer(f,N_times,name,*args,**kwargs):
        start = time.perf_counter()
        for _ in range(N_times):
            f(*args,**kwargs)
        end = time.perf_counter()
        print("{}: {} time execution".format(name,N_times))
        print("{} s".format(end - start))


class TestMultiProcessReplayBuffer(unittest.TestCase):
    class_name = "MultiProcessing"
    buffer_size = 1024 * 256
    N_add = round(buffer_size * 1.5)
    N_time = 10

    obs_dim = 3
    act_dim = 1

    add_dim = 100

    @classmethod
    def setUpClass(cls):
        print(f"{cls.class_name}")
        cls.rb = ProcessSharedReplayBuffer(cls.buffer_size, cls.obs_dim, cls.act_dim)

    def test_write_address(self):
        buffer_size = 256
        add_dim = 5
        tsrb = ProcessSharedReplayBuffer(buffer_size, self.obs_dim, self.act_dim)

        def write(_rb,end,n=1):
            rb = _rb.init_worker()
            obs = np.ones(shape=(add_dim,self.obs_dim)) * n
            act = np.zeros(shape=(add_dim,self.act_dim))
            rew = np.ones((add_dim))
            next_obs = np.ones(shape=(add_dim,self.obs_dim))
            done = np.zeros((add_dim))
            for i in range(0,end,add_dim):
                rb.add(obs,act,rew,next_obs,done)

        q = [Process(target=write,args=(tsrb,50,i)) for i in range(1,8)]
        for qe in q:
            qe.start()

        for qe in q:
            qe.join()

        b = tsrb._encode_sample(range(buffer_size))
        print(b['obs'])
        self.assertTrue(np.isin(b['obs'],[range(1,8)]).all())

    def test_speed(self):
        def f(rb,end):
            obs = np.ones(shape=(self.obs_dim))
            act = np.zeros(shape=(self.act_dim))
            next_obs = np.ones(shape=(self.obs_dim))
            for i in range(0,end):
                rb.add(obs,act,1.0,next_obs, 0)

        def g(rb,end):
            obs = np.ones(shape=(self.add_dim,self.obs_dim))
            act = np.zeros(shape=(self.add_dim,self.act_dim))
            rew = np.ones((self.add_dim))
            next_obs = np.ones(shape=(self.add_dim,self.obs_dim))
            done = np.zeros((self.add_dim))
            for i in range(0,end,self.add_dim):
                rb.add(obs,act,rew,next_obs,done)

        def Multi_(_f):
            def func(rb,end):
                q = [Process(target=lambda rb,end: _f(rb.init_worker(),end),
                             args=(rb,end //8,)) for _ in range(8)]
                for qe in q:
                    qe.start()
                for qe in q:
                    qe.join()
            return func

        def Multi_f(rb,end):
            Multi_(f)(rb,end)

        def Multi_g(rb,end):
            Multi_(g)(rb,end)

        print("Test for single process with 1 point")
        timer(lambda: f(self.rb,self.N_add),self.N_time,
              "Single process adding 1 time-point")

        print("Test for single process with 100 point")
        timer(lambda: g(self.rb,self.N_add),self.N_time,
              "Single process adding {} time-point".format(self.add_dim))

        print("Test for multi process with 1 point")
        timer(lambda: Multi_(f)(self.rb,self.N_add),self.N_time,
              "Multi process adding 1 time-point")

        print("Test for multi process with 100 point")
        timer(lambda: Multi_(g)(self.rb,self.N_add),self.N_time,
              "Multi process adding {} time-point".format(self.add_dim))

class TestMultiProcessPrioritizedReplayBuffer(TestMultiProcessReplayBuffer):
    class_name = "MultiProcessPrioritizedReplayBuffer"
    alpha = 0.5

    @classmethod
    def setUpClass(cls):
        print(f"{cls.class_name}")
        cls.rb = ProcessSharedPrioritizedReplayBuffer(cls.buffer_size,
                                                      cls.obs_dim,
                                                      cls.act_dim,
                                                      alpha = cls.alpha)

if __name__ == '__main__':
    unittest.main()