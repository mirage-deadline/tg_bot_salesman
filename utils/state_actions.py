state_d = {}

def get_state(user_id):

    try:
        state = state_d[f'{user_id}_state']
    except KeyError:
        state = 0