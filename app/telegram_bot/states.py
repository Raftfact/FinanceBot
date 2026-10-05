from aiogram.fsm.state import State, StatesGroup


class TransactionStates(StatesGroup):
    waiting_for_amount = State()
    
    waiting_for_category = State()
    
    waiting_for_new_category = State()