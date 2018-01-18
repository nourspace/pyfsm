from pyfsm import FSM, FSMError

import unittest

from enum import Enum
from unittest.mock import patch


class AdTransition(Enum):
    ACTIVATE = 'ACTIVATE'
    EXPIRE = 'EXPIRE'
    LIMIT = 'LIMIT'
    REMOVE = 'REMOVE'
    REJECT = 'REJECT'


class AdState(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    LIMITED = 'LIMITED'
    OUTDATED = 'OUTDATED'
    REMOVED = 'REMOVED'
    REJECTED = 'REJECTED'


DEFAULT_AD_TRANSITIONS = [
    {'name': AdTransition.ACTIVATE, 'src': [AdState.NEW, AdState.LIMITED, AdState.OUTDATED], 'dst': AdState.ACTIVE},
    {'name': AdTransition.LIMIT, 'src': AdState.NEW, 'dst': AdState.LIMITED},
    {'name': AdTransition.EXPIRE, 'src': AdState.ACTIVE, 'dst': AdState.OUTDATED},
    {'name': AdTransition.REMOVE, 'src': AdState.OUTDATED, 'dst': AdState.REMOVED},
]


class FSMTests(unittest.TestCase):

    def setUp(self):
        self.fsm = FSM(initial=AdState.NEW, transitions=DEFAULT_AD_TRANSITIONS)

    def _is(self, state):
        return self.fsm.current == state

    def _can(self, transition):
        return self.fsm.can(transition=transition)

    def _apply(self, transition):
        self.fsm.apply(transition=transition)

    def test_init(self):
        assert self.fsm.current == AdState.NEW

    def test_can(self):
        assert self._can(AdTransition.ACTIVATE)
        assert not self._can(AdTransition.EXPIRE)
        assert not self._can(AdTransition.REMOVE)

    def test_apply(self):
        self._apply(AdTransition.ACTIVATE)
        assert self._is(AdState.ACTIVE)

        self._apply(AdTransition.EXPIRE)
        assert self._is(AdState.OUTDATED)

        with self.assertRaises(FSMError):
            self._apply(AdTransition.LIMIT)

    def test_add_transition(self):
        assert not self._can(AdTransition.REJECT)
        self.fsm.add_transition({'name': AdTransition.REJECT, 'src': AdState.NEW, 'dst': AdState.REJECTED})
        assert self._can(AdTransition.REJECT)

    @patch('pyfsm.logger.warning')
    def test_add_invalid_transition(self, pyfsm_logger):
        self.fsm.add_transition({})
        assert pyfsm_logger.called_with('Transition definition must contain name, src, and dst')
