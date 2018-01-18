# Python Finite State Machine

Simple Finite State Machine implementation in Python 3. 


## Installation

```bash
pip install git+https://github.com/nourchawich/pyfsm
```

## Usage

```python
from pyfsm import FSM

# Initialise
fsm = FSM(initial='new', transitions=[
    {'name': 'age', 'src': 'new', 'dst': 'old'},
    {'name': 'renew', 'src': 'old', 'dst': 'new'},
    {'name': 'expire', 'src': 'old', 'dst': 'expired'},
])

# Get current state
print(fsm.current)  # new

# Apply transition
fsm.apply('age')
print(fsm.current)  # old

fsm.apply('age')  # Raises FSMError if the transition can not be applied

# Check whether a transition can be applied
fsm.apply('expire')
print(fsm.current)  # expired
print(fsm.can('renew'))  # False
```

## Running Tests

```bash
python -m unittest tests
```


## Todo

* Identify final state.
* Add callbacks.
  * Allow passing arguments when applying transitions.
* Print transitions/states graph.
* Record transitions history.
