# traders
Проект предназначен для удобного тестирования стратегий торговых ботов
Данные берем из апишки ТИ

## Структура
### Боты (Генераторы сигналов)
В папке `bots` каждый бот подчиняется базовому интерфейсу, что позволяет удобно тестировать разные стратегии

* `bots.wide_ranging_day_bot.bot.WideRangeDayBot` бот основан на принципе широкодиапазонного дня, подробнее см реализацию

#### Пример использования бота
```python
from bots.wide_ranging_day_bot.bot import WideRangeDayBot

# history_candles: List[Candle] - список сделок на модели tinvest
# new_candle: Candle - следующий за последним элементом history_candles 
generate_signal = WideRangeDayBot(history_candles)  # список может быть пустым
decision = generate_signal(new_canlde)  # buy
decision = generate_signal(newer_canlde)  # pass
decision = generate_signal(newest_canlde)  # sell
...
```

`decision` определяет видение тренда сигнального бота 

### Утилиты тестирования
#### Для симуляции сделок и расчета доходности страЉтегии бота:
* `sim.traders.Buffett` позволяет сгенерировать сделки пассивного инвестирования (используется как референс)
* `sim.traders.OnePaperHistoryWideRangeTrader` позволяет сгенерировать сделки по сигналам `WideRangeDayBot` 
* `sim.models.DealsView` позволяет рассчитать доходность сделок
* `sim.models.Deal` модель сделки, поддерживает `sum()` для суммирования стоимости списка сделок

#### Пример использования трейдеров на основе `OnePaperHistoryBaseTrader`

```python
from sim import OnePaperHistoryWideRangeTrader

trader = OnePaperHistoryWideRangeTrader(is_short_on=True)
active_deals = trader.create_deals(history_candles)
print("active deals:")
[print(deal) for deal in active_deals]
# >> active deals:
# >> deal: sell 1 paper(s) by 26.47,  total_cost: 26.48$
# >> deal: buy  1 paper(s) by 19.61,  total_cost: -19.62$
```
вызов объекта возвращает список сделок `List[Deal]`

#### Трейдер референс - `Baffett`
```python
from sim import Baffet

passive_deals = Baffet().create_deals(history_candles)
print("passive deals:")
[print(deal) for deal in passive_deals]
# >> passive deals:
# >> deal: buy  1 paper(s) by 16.47,  total_cost: -16.48$
# >> deal: sell 1 paper(s) by 19.61,  total_cost: 19.62$
```
#### Пример расчета доходности сделок
```python
from sim.models import DealsView

# fist_candle - candle, по которому производится первая сделка
# при пассивном инвестировании, от нее и считаем доходность
# active_deals: List[Deal]
active_deals_view = DealsView(active_deals, fist_candle)
print(f"profit active {active_deals_view}")
#>> profit active Total result: 6.86$, 41.65%, deals count: 2
```

## Установка
Устанавливаем python 3.8

Устанавливаем зависимости:

```pip intstall -r requirements.txt```

Кладем TINKOFF_SANDBOX_TOKEN в .env

Токен можно взять тут
https://tinkoffcreditsystems.github.io/invest-openapi/auth/

### Запускаем дефолтный прогон тикетов:

```python main.py```
