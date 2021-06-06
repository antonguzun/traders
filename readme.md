# traders
Проект предназначен для удобного тестирования стратегий торговых ботов

1. [Боты](#Боты)
2. [Утилиты](#Утилиты)
3. [Клиенты](#Клиенты)
4. [Установка](#Установка)
5. [Ресерч](#Ресерч)

## Боты
Они же генераторы сигналов к сделкам.

В папке `bots` каждый бот подчиняется базовому интерфейсу.

* `bots.wide_ranging_day_bot.bot.WideRangeDayBot` бот основан на принципе широкодиапазонного дня ("Технический анализ. Полный курс" - Швагер Джек Д., стр. 651)
* `bots.run_day_breakout_bot.bot.RunDayBreakoutBot` бот основан на идее пробоя "дней с ускорением" ("Технический анализ. Полный курс" - Швагер Джек Д., стр. 661)

[Сводные результаты](https://docs.google.com/spreadsheets/d/1wf5TFp-be7NA-CUFTeJP__qhKkk7ryCaWQHjIkndQ4g/edit?usp=sharing)

### Пример использования бота
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

## Утилиты
#### Трейдеры - классы для симуляции сделок на исторических данных по сигналам ботов:
* `sim.traders.Buffett` позволяет сгенерировать сделки пассивного инвестирования (используется как референс)
* `sim.traders.OnePaperHistoryWideRangeTrader` генерит сделки по сигналам `WideRangeDayBot` 
* `sim.traders.OnePaperHistoryRunDayBreakoutTrader` генерит сделки по сигналам `RunDayBreakoutBot`
  

#### Другие утилиты:
* `sim.models.Deal` модель сделки, поддерживает `sum()` для суммирования стоимости списка сделок
* `sim.models.DealsView` позволяет рассчитать доходность сделок
* `sim.utils.printers.TradingPrinter` вычисляет разницу двух разных трейдеров, получает данные с помощью клиента, выводит результат в консоль
* `sim.utils.result_savers.SummaryTradeResultsCsvSaver` создает csv файл со сводными результатами ботов, использует классы трейдеров для генерации сделок

### Пример использования трейдеров на основе `BaseTrader`
```python
from sim import OnePaperHistoryWideRangeTrader

trader = OnePaperHistoryWideRangeTrader(is_short_on=True)
active_deals = trader.create_deals(history_candles)
print("active deals:", *active_deals, sep="\n")
# >> active deals:
# >> deal: sell 1 paper(s) by 26.47,  total_cost: 26.48$
# >> deal: buy  1 paper(s) by 19.61,  total_cost: -19.62$
```
вызов объекта возвращает список сделок `List[Deal]`

### Трейдер референс `Baffett`
```python
from sim import Baffet

passive_deals = Baffet().create_deals(history_candles)
print("passive deals:", *passive_deals, sep="\n")
# >> passive deals:
# >> deal: buy  1 paper(s) by 16.47,  total_cost: -16.48$
# >> deal: sell 1 paper(s) by 19.61,  total_cost: 19.62$
```
### Пример расчета доходности сделок
```python
from sim.models import DealsView

# fist_candle - candle, по которому производится первая сделка
# при пассивном инвестировании, от нее и считаем доходность
# active_deals: List[Deal]
active_deals_view = DealsView(active_deals, fist_candle)
print(f"profit active {active_deals_view}")
# >> profit active Total result: 6.86$, 41.65%, deals count: 2
```

### Пример использования готовых классов вывода
```python
from datetime import datetime

from app.clients.tinkoff import TIClient
from app.settings import TINKOFF_SANDBOX_TOKEN
from bots.run_day_breakout_bot.models import RunDayBreakoutParams
from sim.traders import OnePaperHistoryRunDayBreakoutTrader
from sim.utils.printers import TradingPrinter


client = TIClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
trader = OnePaperHistoryRunDayBreakoutTrader(
    RunDayBreakoutParams(3, 3), is_short_on=True
)
printer = TradingPrinter(client, trader)

printer.print_history_trading(
    ticker="AMD",
    _from=datetime(year=2020, month=5, day=10),
    _to=datetime(year=2021, month=5, day=10),
)
# >> TICKER AMD
# >> date range: from 2020-05-11 to 2021-05-07
# >> active deals:
# >> 2020-05-28: sell 1 paper(s) by 51.74,  total_cost: 51.77$
# >> ...
# >> 2021-05-07: buy  1 paper(s) by 78.81,  total_cost: -78.85$
# >> profit active 	Total result: 	-13.52$, 	-24.26%, 	deals count: 10
# >> profit passive 	Total result: 	23.08$, 	41.41%, 	deals count: 2
# >> profit effect -65.67%
# >> ________________________
```

## Клиенты
Все модули проекта завязаны на сущность `app.common.models.candle.Candle` для отвязки от типа данных конкретного источника.

Сущность `Candle` содержит в себе класс-методы для создания объекта на основе данных из другого клиента.

Все клиенты должны поддерживать базовый интерфейс и выдавать данные в базовых моделях.
* `app.clients.tinkoff.TIClient` класс клиента апи тинькова

## Установка
Устанавливаем python 3.8

Устанавливаем зависимости:

```pip intstall -r requirements.txt```

Кладем TINKOFF_SANDBOX_TOKEN в .env

Токен можно взять тут
https://tinkoffcreditsystems.github.io/invest-openapi/auth/

### Запускаем дефолтный прогон тикетов:

```python main.py```


### Ресерч
* Оптимизация и подбор параметров для стратегии `WideRangeDayBot` https://github.com/antonguzun/traders/blob/master/research/optimize_wide_range.ipynb

Установка зависимостей:

```pip intstall -r requirements_additional.txt```

запуск юпитера:

```jupiter lab```
