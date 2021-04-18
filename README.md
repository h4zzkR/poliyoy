# Poliyoy - стратегическая игра-проект

# Игровая модель и описание
Игра представляет собой упрощенную версию стратегии Civilization

Вы играете за одну из двух стран против другой страны (бота) на случайно генерируемой карте, состоящей из шестиугольных плиток.
Игрок на старте имеет некоторое количество денежных единиц. Каждый ход их количество увеличивается на n-ое число.

Изначально у игрока есть своя территория в виде клеток, на которых он может размещать юнитов/постройки, которые могут как добавлять монеты за каждый ход,
так и расходовать их.

Каждая клетка карты приносит определенное количество денег за ход. Вы можете захватывать территории путем создания боевых юнитов и размещения их на захватываемой клетке, атаковать противников с помощью этих юнитов, строить защитные здания и держать оборону против врага.


Ваша задача - захватить всю территорию противника.

# Типы юнитов и построек
- мечник -- боевой юнит ближнего боя, тратит монеты каждый ход
- лучник -- облегченный боевой дальнобойный юнит, тратит монеты каждый ход
- ферма -- постройка, приносит монеты каждый ход
- защитная башня -- защитное дальнобойное сооружение, тратит монеты каждый ход

# Part 1 - создание сущностей
Объекты, которые игрок может располагать на карте - это сущности типа AbstractEntity. 
От этого класса наследуются два основных типа - AbstractUnit - перемещаемые юниты, для которых предусмотрен метод перемещения и AbstractBuilding - постройки.
Каждая сущность принадлежит определенной фракции - могут быть лучники красных, мечники синих и т.п.

Несмотря на то, что в игре всего две фракции, хорошим тоном будет считаться разработка с заделом на будущее. Что, если у нас будет множество фракций и юнитов?
Эту проблему решает паттерн Builder. С помощью классов UnitBuilder и BuildingBuilder мы модем создавать требуемые объекты различных фракций с различными параметрами. Параметры создаваемых объектов не привязаны к типу объекта (в нашей схеме все объекты - AbstractEntity), мы можем определить общие характеристики, а тип указать потом с помощью задания объекту определенного id.

Параметры юнитов и построек прописаны в json файле, поэтому создадим класс, который может считывать эти данные и руководить строителем. Каждый тип сущности имеет уникальный id, который прописан в том же файле.

Для удобства создания обектов предусмотрен класс Director, который обращается к классу Builder и взаимодействует с ним, посылая ему нужные параметры создания объектов. В логику Director вшиты методы создания типов, также можно обратиться к нему через метод build_entity(id, position). С помощью методов fraction0, fraction1, fraction(id) можно присваивать объектам фракции. Теперь если мы захотим расширить список типов наших юнитов (или построек), нужно будет дописать всего один метод в классе UnitDirector, а также прописать новому типу сущности характеристики в json файле.

Мы можем создавать объекты с заданными характеристиками. Но этих объектов может быть много и все они одной природы. Поручим создание новых объектов самим объектам. Это можно сделать с помощью паттерна Прототип, все наши объекты copiable, т.е. их можно клонировать. Так мы сможем при надобности создавать новые объекты от старых, без обращения к директору.

![unitCreation(1)](https://user-images.githubusercontent.com/35405876/111896446-bc755e00-8a2a-11eb-8a40-1aef4e0e451b.png)


# Part 2 - размещение юнитов, логика ходов, карта и паттерны
- To be continued


# Dev stack
- python
- arcade (графическая библиотека)
- pillow
- numpy
- ...

# References
- [Antiyoy](https://play.google.com/store/apps/details?id=yio.tro.antiyoy.android&hl=ru&gl=US)
- [Civ6](https://www.epicgames.com/store/ru/p/sid-meiers-civilization-vi)
