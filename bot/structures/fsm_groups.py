from aiogram.fsm.state import State, StatesGroup


class PostStates(StatesGroup):
    """ Состояния для постов
    """
    waiting_for_select = State()
    waiting_for_text = State()
    waiting_for_url = State()
    waiting_for_budget = State()
    waiting_for_pr_type = State()
    waiting_for_price_url = State()
    waiting_for_price_publication = State()
    waiting_for_post_subs_min = State()
