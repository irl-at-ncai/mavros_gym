#!/usr/bin/env python3
"""
Defines the RobotSimEnv class.
"""

import rospy
import gym
from mavros_gym_msgs.msg import RLExperimentInfo


class RobotSimEnv(gym.Env):
    """
    The base class that interacts with the simulator through 'sim_handler' to
    give a valid training sequence of the environment using any reinforcement
    learning algorithm.

    Parameters
    ----------
    sim_handler: SimulationHandler
        The underlying class that deals with a given type of simulator such as
        airsim or gazebo.
    """

    def __init__(self, sim_handler):
        self.sim_handler = sim_handler
        self.episode_num = 0
        self.cumulated_episode_reward = 0
        self.reward_pub = \
            rospy.Publisher('/openai/reward', RLExperimentInfo, queue_size=1)

    def step(self, action):
        """
        Executed each at time step of simulation. The action is
        executed and next observations coming from the environment are
        returned.

        Parameters
        ----------
        action: Action of any type
            Action of any type which is handled by the _set_action() function
            defined at a lower level of hierarchy.

        Returns
        -------
        obs: Observation of any type
            An array of observation data as obtained by _get_obs() function
            also defined at a lower level of hierarchy.
        reward: Reward generated by the action according to _compute_reward().
        done: Whether the episode should finish according to _is_done().
        info: Any additional info about the training step.
        """

        self.sim_handler.unpause()
        self._set_action(action)
        self.sim_handler.pause()
        obs = self._get_obs()
        done = self._is_done(obs)
        info = {}
        reward = self._compute_reward(obs, done)
        self.cumulated_episode_reward += reward
        return obs, reward, done, info

    def reset(self):
        """
        Executed at first time step of simulation. Performs the initialation of
        the environment episode and returns the initial
        observation from the environment.

        Returns
        -------
        obs: Observation of any type
            An array of observation data as obtained by _get_obs() function
            also defined at a lower level of hierarchy.
        """
        self._pre_reset()
        self.sim_handler.pause()
        self.sim_handler.reset()
        self._set_init_pose()
        self._init_env_variables()
        self._update_episode()
        obs = self._get_obs()
        return obs

    def close(self):
        """ Performs cleanup operations to close the environment. """

    def _update_episode(self):
        """
        Publishes the accumulated reward of the episode and
        increases the episode number by one.
        """
        self._publish_reward_topic(
            self.cumulated_episode_reward, self.episode_num)
        self.episode_num += 1
        self.cumulated_episode_reward = 0

    def _publish_reward_topic(self, reward, episode_number=1):
        """
        This function publishes the given reward in the reward topic for
        easy access from ROS infrastructure.

        Parameters
        ----------
        reward: Float
            Episode reward
        episode_number: int
            Episode number
        """
        reward_msg = RLExperimentInfo()
        reward_msg.episode_number = episode_number
        reward_msg.episode_reward = reward
        self.reward_pub.publish(reward_msg)

    def _pre_reset(self):
        """
        Performs operations required prior to simulation state reset
        """
        raise NotImplementedError()

    def _set_init_pose(self):
        """
        Sets the Robot in its init pose
        """
        raise NotImplementedError()

    def _check_all_systems_ready(self):
        """
        Checks that all the sensors, publishers and other simulation systems
        are operational.
        """
        raise NotImplementedError()

    def _get_obs(self):
        """
        Returns the observation.
        """
        raise NotImplementedError()

    def _init_env_variables(self):
        """
        Inits variables needed to be initialised each time we reset at the
        start of an episode.
        """
        raise NotImplementedError()

    def _set_action(self, action):
        """
        Applies the given action to the simulation.
        """
        raise NotImplementedError()

    def _is_done(self, observations):
        """
        Indicates whether or not the episode is done
        (the robot has fallen for example).
        """
        raise NotImplementedError()

    def _compute_reward(self, observations, done):
        """
        Calculates the reward to give based on the observations given.
        """
        raise NotImplementedError()

    def _env_setup(self, initial_qpos):
        """
        Initial configuration of the environment. Can be used to configure
        initial state and extract information from the simulation.
        """
        raise NotImplementedError()


class WorldState():
    """
    The base class composed of all the possible world data that can be
    obtained from the world and is used in training in concrete terms.
    """
    def __init__(self):
        pass

    def camera(self, camera_index):
        """ Should return the camera image at camera_index. """
        raise NotImplementedError()

    def camera_depth(self, camera_index):
        """ Should return the camera image with depth at camera_index. """
        raise NotImplementedError()

    @property
    def collision_check(self):
        """ Returns the collision response. """
        raise NotImplementedError()
