from random import choice


def checkAllSystems() -> str:
    return "Everything is working!"

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent'
    elif 'test' in lowered:
        return checkAllSystems()
    else:
        return choice["I don't understand are you sure you got the right command there buddy?", "What are you talking about ? ", "Sorry i didn't understand that"]