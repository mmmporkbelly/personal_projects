"""
A simple FSM that shows the endstate for a basic TCP session
Users can enter a list of actions, and the endstate will be shown

Seido Karasaki (yakitategohan on GitHub)
v1 2/3/2023
"""


def traverse_TCP_states(events):
    # Possible list of actions stored in dictionary

    actions = {
        'CLOSED': {
            'APP_PASSIVE_OPEN': 'LISTEN',
            'APP_ACTIVE_OPEN': 'SYN_SENT'
        },
        'LISTEN': {
            'RCV_SYN': 'SYN_RCVD',
            'APP_SEND': 'SYN_SENT',
            'APP_CLOSE': 'CLOSED'
        },
        'SYN_RCVD': {
            'APP_CLOSE': 'FIN_WAIT_1',
            'RCV_ACK': 'ESTABLISHED'
        },
        'SYN_SENT': {
            'RCV_SYN': 'SYN_RCVD',
            'RCV_SYN_ACK': 'ESTABLISHED',
            'APP_CLOSE': 'CLOSED'
        },
        'ESTABLISHED': {
            'APP_CLOSE': 'FIN_WAIT_1',
            'RCV_FIN': 'CLOSE_WAIT'
        },
        'FIN_WAIT_1': {
            'RCV_FIN': 'CLOSING',
            'RCV_FIN_ACK': 'TIME_WAIT',
            'RCV_ACK': 'FIN_WAIT_2'
        },
        'CLOSING': {
            'RCV_ACK': 'TIME_WAIT'
        },
        'FIN_WAIT_2': {
            'RCV_FIN': 'TIME_WAIT'
        },
        'TIME_WAIT': {
            'APP_TIMEOUT': 'CLOSED'
        },
        'CLOSE_WAIT': {
            'APP_CLOSE': 'LAST_ACK'
        },
        'LAST_ACK': {
            'RCV_ACK': 'CLOSED'
        }
    }
    # Initial state
    state = "CLOSED"

    # Iterate through events
    for action in events:
        # Change state if the given action is possible in current state
        if action.upper() in actions[state].keys():
            state = actions[state][action.upper()]
        else:
            return 'ERROR'

    # Return final state
    return state
