from enum import Enum
import logging

# Add basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transition:
    """
    FSM transition definition
    """

    def __init__(self, name, src, dst):
        """
        :param str or Enum name: transition name
        :param str or list[str] or Enum or list[Enum] src: allowed sources
        :param str or Enum dst: transition destination
        """
        self.name = name
        self.src = [src] if isinstance(src, (str, Enum)) else src
        self.dst = dst

    def __repr__(self):
        return f'Transition: {self.name}'

    def __hash__(self):
        return str(self)


class FSMError(Exception):
    pass


class FSM:
    """
    Finite State Machine
    """

    def __init__(self, initial, transitions=None):
        """
        :param str or Enum initial: initial state
        :param list[dict] or list[Transition] transitions: list of allowed transitions
        """
        self.current = initial
        self.transitions_map = {}
        if not transitions:
            transitions = []
        self.add_transitions(transitions=transitions)

    def __repr__(self):
        return f'FSM: {self.current}'

    def add_transition(self, transition):
        """
        Add the given transition
        :param dict or Transition transition: transition definition
        """
        if not isinstance(transition, Transition):
            if not {'name', 'src', 'dst'} <= set(transition):
                logger.warning('Transition definition must contain name, src, and dst')
                return

            transition = Transition(name=transition['name'], src=transition['src'], dst=transition['dst'])

        if transition.name not in self.transitions_map:
            self.transitions_map[transition.name] = {}

        for src in transition.src:
            self.transitions_map[transition.name][src] = transition.dst
            logger.debug(f'Added transition {transition.name} from {src} to {transition.dst}')

    def add_transitions(self, transitions):
        """
        Add the given list of transitions
        :param list[dict] or list[Transition] transitions: list of transition definitions to add
        """
        for transition in transitions:
            self.add_transition(transition=transition)

    def apply(self, transition):
        """
        Apply the given transition
        :param str or Enum transition: transition name
        """
        if not self.can(transition=transition):
            msg = f'Can not apply {transition} on {self.current}'
            logger.warning(msg)
            raise FSMError(msg)
        self.current = self.transitions_map[transition][self.current]

    def can(self, transition):
        """
        Return whether the given transition is possible assuming current state
        :param str or Enum transition: transition name
        :rtype: bool
        """
        return transition in self.transitions_map and self.current in self.transitions_map[transition]
