import asyncio, random, os
from dotenv import load_dotenv
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from constants import BLOCK_USERS
import App.keyboards as kb
import App.Components.payment as pay

load_dotenv
router = Router()
bot = Bot(token=os.getenv('BOT_TOKEN'))


@router.message(CommandStart())
async def start(message : Message):
   msg = isBlock(message, f'Привет {message.from_user.first_name}! Этот бот сделает тебе информатику.\n\n/buy - заказать дз\n/price - узнать цены\n/help - инструкция')
   await message.answer(text=msg)


@router.message(Command('price'))
async def price(message : Message):
   msg = isBlock(message, '💵<b>Прайс:</b>\n\nТесты - 100₽\nДЗ - 350₽\nКР - 450₽\nАР - 500₽\n\n<b>Четверти (9 класс)</b>\n1 Четверть - 1000₽\n2 Четверть - 1000₽\n3 Четверть - 1450₽\n4 Четверть - 550₽')
   await message.answer(text=msg, parse_mode='html')


@router.message(Command('buy'))
async def buy(message : Message):
   await kb.reset_weeks_9_grade()
   
   if not isBlockById(message.from_user.id):
      await message.answer(text='Выберите класс:', reply_markup=kb.choice_grade_keyboard)
   else:
      await message.answer(text=isBlock(message, ''))


@router.callback_query(F.data == '8 класс')
async def is_8_grade(callback : CallbackQuery):
   await callback.answer('❌ 8 класс пока недоступен.')


@router.callback_query(F.data == '9 класс')
async def is_9_grade(callback : CallbackQuery):
   await callback.answer()
   
   if not isBlockById(callback.from_user.id):
      await callback.message.edit_text(text='Выберите четверть:', reply_markup=kb.choice_quarter_grade_9_keyboard)


@router.callback_query(F.data == 'Вернуться к выбору класса')
async def back_to_choice_grade(callback : CallbackQuery):
   await callback.answer()
   
   if not isBlockById(callback.from_user.id):
      await callback.message.edit_text('Выберите класс:', reply_markup=kb.choice_grade_keyboard)


@router.callback_query(F.data.in_(kb.quarters_9_grade))
async def quar_1_grade_9(callback : CallbackQuery):
   await callback.answer()
   
   index = kb.quarters_9_grade.index(callback.data)
   kb.ind = callback.data
   # Очищаем галочки, и добавляем только к выбранной четверти
   #for i in range(len(kb.quarters_9_grade)):
   #   if kb.quarters_9_grade[i] != callback.data:
   #      kb.quarters_9_grade[i] = kb.quarters_9_grade[i].replace(' ✅', '')
   #   else:
   #      kb.quarters_9_grade[i] += ' ✅'
   
   await callback.message.edit_text('Выберите недели:', reply_markup=await kb.weeks_91_keyboard())
   print(kb.quarters_9_grade, '\n', kb.ind)


@router.callback_query(F.data.in_(kb.weeks_9_grade[2]))
async def choices_weeks_91(callback : CallbackQuery):
   print(kb.ind)
   
   await callback.answer()
   
   quar_index = kb.quarters_9_grade.index(kb.ind)
   week_index = kb.weeks_9_grade[quar_index].index(callback.data)
   
   if ' ✅' in kb.weeks_9_grade[quar_index][week_index]:
      kb.weeks_9_grade[quar_index][week_index] = kb.weeks_9_grade[quar_index][week_index].replace(' ✅', '')
   else:
      kb.weeks_9_grade[quar_index][week_index] += ' ✅'
   
   await callback.message.edit_reply_markup(reply_markup=await kb.weeks_91_keyboard())
   


@router.callback_query(F.data == 'Отменить заказ')
async def cancel_order(callback : CallbackQuery):
   await callback.answer()
   pay.is_order = False
   for i in range(len(kb.quarters_9_grade)): kb.quarters_9_grade[i] = kb.quarters_9_grade[i].replace(' ✅', '')
   await kb.reset_weeks_9_grade()
   await callback.message.edit_text('Заказ отменен.')


@router.callback_query(F.data == 'Подтвердить заказ')
async def confirm_order(callback : CallbackQuery):
   await callback.answer()
   
   weeks_in_order = [i.replace(' неделя ✅', '') for i in kb.weeks_9_grade[0] if '✅' in i]
   test_price = sum(100 for i in weeks_in_order if f'{i} неделя' in kb.TST_weeks_9)
   work_price = sum(350 for i in weeks_in_order if f'{i} неделя' in kb.HMW_weeks_9)
   
   pay.is_order = True
   order_price = test_price + work_price
   formatted_weeks = ', '.join(weeks_in_order)
   label = f"{callback.from_user.id}_{random.randint(1000, 9999)}" # Уникальная метка для заказа
   link = await pay.create_order(order_price, label)               # Создаем заказ и получаем ссылку на оплату
   
   if not isBlockById(callback.from_user.id):
      await callback.message.edit_text(
         f'📚<b>Заказ:</b>\nИнформатика 9 класс: {formatted_weeks}\n\n<b>Стоимость:</b>\n{order_price}₽\n\n<i>Проверка оплаты через 1-2 мин.</i>',
         parse_mode='html',
         reply_markup=await kb.create_order_keyboard(link)
      )
      
   # Проверяем оплату через 60 секунд
   await asyncio.sleep(60)
   token = os.getenv("YOOMONEY_TOKEN") # Токен для проверки
   is_paid = await pay.check_payment(token, label)
   
   if is_paid:
      await callback.message.answer("✅ Платеж успешно прошел! Спасибо.")
      try:
         await bot.send_message(chat_id=-1002321866801,
                                message_thread_id=3,
                                text=f'<b>Новый платеж!</b>\n{order_price}₽\n\n<span class="tg-spoiler"><b>Заказ:</b>\nИнформатика 9 класс: {formatted_weeks}\n\n<b>Заказчик:</b>\n{callback.from_user.full_name} (@{callback.from_user.username})</span>', parse_mode='html')
      except Exception as e:
         print(f'Error append history: {e}')
   elif pay.is_order:
      await callback.message.answer("Похоже, у вас не получилось произвести оплату. Если возникли вопросы или что-то не работает, то обратитесь в поддержку: @KodersUp")

   
# Проверка на блокировку человека
def isBlock(message : Message, msg):
   if message.from_user.id in BLOCK_USERS:
      return f'❌ {message.from_user.first_name}, к сожалению тебе запрещено пользоваться ботом =('
   else:
      return msg

# Проверка по ID
def isBlockById(id): return id in BLOCK_USERS