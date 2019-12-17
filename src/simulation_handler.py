#!/usr/bin/env python

class SimulationHandler():
    
    def __init__(self):
        self.setup()

    def setup(self):
        """
        Performs initial simulation setup
        """
        self.initialize_physics_params()
        self.pause()
            
    def reset(self):
        """
        Resets the simulation to its initial state
        """
        raise NotImplementedError()

    def pause(self):
        """
        Pauses the simulation
        """
        raise NotImplementedError()
        
    def unpause(self):
        """
        Unpauses the simulation
        """
        raise NotImplementedError()

    def initialize_physics_params(self):
        """
        Might be implemented to update physics parameters at startup
        """
        pass