from soil.agents import FSM, state, default_state, prob
import logging


class OpinionLeader(FSM):
    '''
    .
    '''
    defaults = {
        'prob_neighbor_spread': 0.7,
        'type': 1,
    }

    @default_state
    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id="not_exposed"):
            if prob(self['prob_neighbor_spread']):
                neighbor.expose(1)


class Bot(FSM):
    '''
    .
    '''
    defaults = {
        'prob_neighbor_spread': 0.3,
        'type': 2,
    }

    level = logging.DEBUG

    @default_state
    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id="not_exposed"):
            if prob(self['prob_neighbor_spread']):
                neighbor.expose(2)


class User(FSM):
    '''
    .
    '''

    defaults = {
        'prob_neighbor_spread': 0.05,
        'prob_search_spread': 0.1,
        'prob_be_infected': 0.2,
        'infected_type': 0,
    }


    @default_state
    @state
    def not_exposed(self):
        if prob(self['prob_search_spread']):
            self.set_state(self.exposed)

    @state
    def exposed(self):
        if prob(self['prob_be_infected']):
            self.set_state(self.infected)

    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id=self.not_exposed.id):
            if prob(self['prob_neighbor_spread']):
                neighbor.expose(self['infected_type'])

    def expose(self, type):
        if not self.state['id'] == self.infected.id: #
            self.set_state(self.exposed)
            self['infected_type'] = type
            #print(self['infected_type'])
