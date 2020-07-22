from soil.agents import FSM, state, default_state, prob
import logging


class NotActive(FSM):
    '''
    A not active twitter user(tweets published  in two months <= 4).
    '''
    defaults = {
        'prob_neighbor_spread': 0.1,
        'prob_search_spread': 0.1,
        'prob_be_infected': 0.2,
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
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id:
            self.set_state(self.exposed)


class AlmostActive(NotActive):
    '''
    An almost active twitter user (4 < tweets published  in two months < 16).
    '''
    defaults = {
        'prob_neighbor_spread': 0.2,
        'prob_search_spread': 0.2,
        'prob_be_infected': 0.3,
    }

    level = logging.DEBUG

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
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id:
            self.set_state(self.exposed)


class Active(AlmostActive):
    '''
    An active twitter user (tweets published  in two months >= 16).
    '''

    defaults = {
        'prob_neighbor_spread': 0.4,
        'prob_search_spread': 0.4,
        'prob_be_infected': 0.4,
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
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id: #
            self.set_state(self.exposed)
