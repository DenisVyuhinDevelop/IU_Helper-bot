from yoomoney import Quickpay, Client
import asyncio

is_order = True

async def create_order(sum, label):
   # Создаем ссылку на оплату
   quickpay = Quickpay(
      receiver="4100118950644678",  # ID вашего кошелька
      quickpay_form="shop",
      targets="Оплата заказа",
      paymentType="SB",  # Способ оплаты (например, 'SB' - Сбербанк)
      sum=sum,
      label=label
   )
   
   # Возвращаем ссылку на оплату
   return quickpay.redirected_url

import time

async def check_payment(token, label):
   client = Client(token)
   history = client.operation_history(label=label)
   
   # Проверяем несколько раз с интервалом
   retries = 5  # Количество попыток
   if is_order:
      for _ in range(retries):
         time.sleep(10)  # Пауза в 10 секунд перед повторной проверкой
         history = client.operation_history(label=label)
         
         for operation in history.operations:
            if operation.status == "success" and operation.label == label:
               return True
   return False