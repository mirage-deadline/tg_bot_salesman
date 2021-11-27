from typing import Union
from states.food import States
from transitions import Machine


state_table = {}
transitions = [
    ['pizza', States.DIALOG_START, States.CHOOSE_SIZE],
    ['size', States.CHOOSE_SIZE, States.CHOOSE_PAYMENT],
    ['payment', States.CHOOSE_PAYMENT, States.MAKE_SURE],
    ['cancel', '*', States.DIALOG_START]]

def create_base_state(user_id: int):
    user_state = Machine(states=States, transitions=transitions, initial=States.DIALOG_START)
    state_table[f'{user_id}_state'] = user_state

def get_state(user_id: int) -> Union[object, bool]:
    
    try:
        state = state_table[f'{user_id}_state']
    except KeyError:
        state = States.DIALOG_START

    return state

def add_state(user_id: int, prev_trigger: str, trigger_action: str) -> None:
    
    user_state = Machine(states=States, transitions=transitions, initial=prev_trigger)
    user_state.trigger(trigger_action)
    state_table[f'{user_id}_state'] = user_state.state.value
    