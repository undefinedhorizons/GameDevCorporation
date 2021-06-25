from utils import get_game

def switch_state(instance):
    if instance.text == get_game().current_state:
        get_game().set_state('none')
        return

    get_game().set_state(instance.text)