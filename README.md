# Poliyoy - стратегическая игра-проект

![image](https://user-images.githubusercontent.com/35405876/116817313-638efe80-ab6e-11eb-947c-0109cff77668.png)

# Игровая модель и описание
Игра представляет собой упрощенную версию стратегии Civilization

Вы играете за одну из двух стран против другой страны (~~бота~~) на случайно генерируемой карте, состоящей из шестиугольных плиток.
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
Добро пожаловать в новую версию проекта! Давайте ознакомимся с архитектурой. Гексагональная карта в игре задается с помощью плиток, а плитка - элемент класса Hex. Это спрайт, который умеет рендерить сам себя. Hex хранит свою текстуру гексагона, позицию и т.п., а также умеет клонировать себя и изменять свои параметры. Чтобы создать карту, нужно создать объект класса HexMap. HexMap хранит в себе список плиток, занимается инициализацией карты, размещением на ней фракций. HexMap решает вопросы позиционирования на карте (считается сложная математика, которая по пиксельным координатам вычисляет позицию в сетке плиток), в нем прописаны все необходимые методы для комфортной работы с плитками и картой в целом (например, есть метод, который позволяет получить координаты 6 соседних клеток). SpriteList(Hex) позволяет очень быстро рендерить объекты на карте (в связи с тем, что такой объект должен быть один, объекты других классов вынуждены размещать юнитов для рендеринга через HexMap). 

В нашей парадигме, объект на карте неразрывно связан с плиткой - фактически, это и есть плитка с подвешенным к ней объектом. Да, здесь применяется паттерн "Декоратор", который позволяет подключить дополнительную логику к нашему Hex, а именно связать объекты AbstractEntity и их спрайты с плиткой. Когда мы говорили о том, что в HexMap хранятся объекты Hex, мы немного вас обманули - HexMap как раз работает с TileDecorator, что в общем-то достаточно удобно. 

"Ядро" проекта - класс Game : arcade.Window, занимается отрисовкой и не только, через этот класс пользователь взаимодействует с игрой: здесь есть методы рендеринга, предварительной настройки карты и UI игры, а также методы обработки нажатий клавиш мыши. Так, например, выбрав плитку на карте, вы можете нажав кнопочку поместить на плитку деревню, которая будет приносить доход. С классом Game связан синглтон MapState, который хранит важную информацию о состоянии карты и игры и который доступен для других объектов, использующих эту информацию.

Фракции в игре представлены классом Fraction, через объекты этого же класса можно вызывать билдеров и директоров для создания сущностей, также в них содержится информация об всех параметрах фракции (занимаемая территория, постройки и юниты и т.п.). На старте игры на карту случайным образом помещаются по зданию на каждую фракцию - импровизированные столицы фракций, а также занимается изначальная территория в 6 клеток для каждой страны (может быть меньше, если столица находится близко к краю карты TODO).

# Part 3 - передвижение/захват юнитов, денежные отношения и команды
Команды пользователя (например, от кнопок размещения юнитов) передаются системе согласно паттерну Command. Поддерживаются команды спавна и движения сущностей.
Также была завершена логика захвата клеток, уничтожения юнитов и реализованы основные функции игры. Добавлена базовая экономика (сущности создаются за денежные единицы и приносят/отнимают деньги) To be continued

TODO: условия в move_to можно заменить на CoR

![image](https://user-images.githubusercontent.com/35405876/115785805-a3185680-a3c8-11eb-89fb-a6c1615a31a8.png)


# Инструкции
Клетка под защитой, если на нее не может наступить разведчик.

- кнопка V - создать деревню (приносит 5 единиц дохода за ход)
- кнопка W - создать воина, самый сильный юнит в игре, способен уничтожать себе подобных и более слабых юнитов, а также ходить по защищенным клеткам. При создании воина шесть соседних клеток становятся защищенными.
- кнопка S - создать разведчика, легкий юнит, способен захватывать незащищенные клетки и уничтожать себе подобных
- кнопка T - создать башню - защитное сооружение, аналогично воину, защищает шесть соседних клеток, но не может двигаться (логично) и атаковать

Для передвижения юнита кликните левой кнопкой мыши на клетку с юнитов и кликните правой кнопкой на желаемую клетку (куда нужно передвинуть юнита). Вы можете ходить только в определенном радиусе клеток, подсвеченным серым.


# Dev stack
- python
- arcade (графическая библиотека)
- pillow
- numpy
- easyAI (maybe)
- ...

# References
- [Antiyoy](https://play.google.com/store/apps/details?id=yio.tro.antiyoy.android&hl=ru&gl=US)
- [Civ6](https://www.epicgames.com/store/ru/p/sid-meiers-civilization-vi)
