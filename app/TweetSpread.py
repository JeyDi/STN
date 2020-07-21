from soil.agents import FSM, state, default_state, prob
import logging


class NotActive(FSM):
    '''
    A not active twitter user(??? tweet).
    '''
    defaults = {
        'prob_neighbor_spread': 0.2,
        'prob_search_spread': 0.2,
        'prob_be_infected': 1,
    }

    @default_state
    @state
    def not_exposed(self):
        if prob(self.env['prob_search_spread']):
            self.set_state(self.exposed)

    @state
    def exposed(self):
        if prob(self.env['prob_be_infected']):
            self.set_state(self.infected)

    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id=self.not_exposed.id):
            if prob(self.env['prob_neighbor_spread']):
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id:
            self.set_state(self.exposed)


class AlmostActive(NotActive):
    '''
    An almost active twitter user(??? tweet).
    '''
    defaults = {
        'prob_neighbor_spread': 0.4,
        'prob_search_spread': 0.4,
        'prob_be_infected': 1,
    }

    level = logging.DEBUG

    @default_state
    @state
    def not_exposed(self):
        if prob(self.env['prob_search_spread']):
            self.set_state(self.exposed)

    @state
    def exposed(self):
        if prob(self.env['prob_be_infected']):
            self.set_state(self.infected)

    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id=self.not_exposed.id):
            if prob(self.env['prob_neighbor_spread']):
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id:
            self.set_state(self.exposed)


class Active(AlmostActive):
    '''
    An active twitter user(??? tweet).
    '''

    defaults = {
        'prob_neighbor_spread': 0.5,
        'prob_search_spread': 0.5,
        'prob_be_infected': 1,
    }


    @default_state
    @state
    def not_exposed(self):
        if prob(self.env['prob_search_spread']):
            self.set_state(self.exposed)

    @state
    def exposed(self):
        if prob(self.env['prob_be_infected']):
            self.set_state(self.infected)

    @state
    def infected(self):
        for neighbor in self.get_neighboring_agents(state_id=self.not_exposed.id):
            if prob(self.env['prob_neighbor_spread']):
                neighbor.expose()

    def expose(self):
        if not self.state['id'] == self.infected.id: #
            self.set_state(self.exposed)
