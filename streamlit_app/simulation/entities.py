from soil.agents import FSM, state, default_state, prob
import logging

level = logging.DEBUG

class OpinionLeader(FSM):
    """
    Opinion Leader soil configuration.
    An opinion leader is an influencer inside twitter, an user with lots of followers.

    Args:
        Extend FSM (soil object): Type of base agent into soil simulation
    """

    defaults = {
        "prob_neighbor_spread": 0.7,
        "type": 1,
    }

    @default_state
    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id="not_exposed"):
            if prob(self["prob_neighbor_spread"]):
                neighbor.expose(type=1, directed=1)


class Bot(FSM):
    """
    Bot entity soil configurations
    A bot is a node that simulate a twitter bot with news spreading functionalities

    Args:
        Extend FSM (soil object): Type of base agent into soil simulation
    """

    defaults = {
        "prob_neighbor_spread": 0.3,
        "type": 2,
    }

    @default_state
    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id="not_exposed"):
            if prob(self["prob_neighbor_spread"]):
                neighbor.expose(type=2, directed=1)


class User(FSM):
    """
    User agent soil configurations
    Simulate an user on twitter

    Args:
        Extend FSM (soil object): Type of base agent into soil simulation
    """

    defaults = {
        "prob_neighbor_spread": 0.05,
        "prob_search_spread": 0.1,
        "prob_be_infected": 0.2,
        "infected_type": 0,
        "directed": 1
    }

    @default_state
    @state
    def not_exposed(self):
        if prob(self["prob_search_spread"]):
            self.set_state(self.exposed)

    @state
    def exposed(self):
        if prob(self["prob_be_infected"]):
            self.set_state(self.infected)

    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id=self.not_exposed.id):
            if prob(self["prob_neighbor_spread"]):
                neighbor.expose(type=self["infected_type"], directed=0)

    ### REMOVE AFTER CHECK ###
    def old_expose(self, type, directed):
        if not self.state["id"] == self.infected.id:
            self.set_state(self.exposed)
            self["infected_type"] = type

    ### NEW WXPOSE ###
    # da calibrare???
    def expose(self, type, directed):
        count_neighbor = 0
        prob_neighbor = 0

        for neighbor in self.get_neighboring_agents():
            if neighbor.state['id'] == self.exposed.id:
                prob_neighbor += 0.4
            if neighbor.state['id'] == self.infected.id:
                prob_neighbor += 0.9

            count_neighbor += 1

        prob_neighbor /= count_neighbor

        if (not self.state['id'] == self.infected.id and prob(prob_neighbor)):
            self.set_state(self.exposed)
            self['infected_type'] = type
            self["directed"] = directed