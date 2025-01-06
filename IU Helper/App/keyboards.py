from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

HMW_weeks_9 = ['6 неделя', '7 неделя', '13 неделя', '17 неделя', '23 неделя', '25 неделя', '27 неделя', '34 неделя',]
TST_weeks_9 = ['2 неделя', '3 неделя', '4 неделя', '5 неделя', '8 неделя', '11 неделя', '12 неделя', '14 неделя', '15 неделя', '16 неделя', '21 неделя', '22 неделя', '24 неделя', '26 неделя', '28 неделя', '29 неделя', '32 неделя', '33 неделя', '35 неделя', '36 неделя']

choice_grade_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text='8 класс', callback_data='8 класс'),
   InlineKeyboardButton(text='9 класс', callback_data='9 класс')]
])

quarters_9_grade = [f'{i} Четверть' for i in range(1, 5)]
ind = '1 Четверть'

choice_quarter_grade_9_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text='1 Четверть', callback_data='1 Четверть')],
   [InlineKeyboardButton(text='2 Четверть', callback_data='2 Четверть')],
   [InlineKeyboardButton(text='3 Четверть', callback_data='3 Четверть')],
   [InlineKeyboardButton(text='4 Четверть', callback_data='4 Четверть')],
   [InlineKeyboardButton(text='⬅️ назад', callback_data='Вернуться к выбору класса')],
])

weeks_9_grade = [
   [f'{i} неделя' for i in range(2, 9)],
   [f'{i} неделя' for i in range(11, 18)],
   [f'{i} неделя' for i in range(21, 30)],
   [f'{i} неделя' for i in range(32, 37)]
]


async def weeks_91_keyboard() -> InlineKeyboardMarkup:
   keyboard = InlineKeyboardBuilder()
   # index = next((i for i, item in enumerate(quarters_9_grade) if ' ✅' in item), -1)
   
   for i in weeks_9_grade[quarters_9_grade.index(ind)]:
      keyboard.add(InlineKeyboardButton(text=i, callback_data=i))
   
   keyboard.adjust(2)
   keyboard.row(
      InlineKeyboardButton(text='Отмена', callback_data='Отменить заказ'),
      InlineKeyboardButton(text='✔️ Подтвердить', callback_data='Подтвердить заказ'),
   )
   
   return keyboard.as_markup()


# Очищаем галочки
async def reset_weeks_9_grade():
   for quar in range(4):
      for week in range(len(weeks_9_grade[quar])):
         weeks_9_grade[quar][week] = weeks_9_grade[quar][week].replace(' ✅', '')


async def create_order_keyboard(pay_link: str) -> InlineKeyboardMarkup:
   return InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text='Оплатить', url=pay_link)],
      [InlineKeyboardButton(text='Отмена', callback_data='Отменить заказ')]
   ])
   
def get_quarter_index():
   r = ''
   for i in quarters_9_grade:
      if ' ✅' in i:
         r = i
   
   return quarters_9_grade.index(r)