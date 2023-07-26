"""
Логика игры "Поле чудес"

Играют в игру три человека.
Загадывается определенное слово из списка. Каждый игрок по очереди говорит определенную букву и крутит барабан.

После прокрута барабана может 100,200,500,1000 очков, сектор "+"(можно открыть одну любую букву в слове),
сектор "Приз"(это либо 2000 очков, либо какой-то приз(но если игрок выбирает приз, то он выбывает из игры)),а также
пропуск хода.

Если она есть в слове, то ход игрока продолжается
и он выбирает буквы до тех пор, пока не отгадает слово или не ошибется.

При ошибке ход переходит следующему игроку
и так по кругу пока слово не отгадают.

У каждого игрока есть две попытки отгадать слово полностью.

При первой неудаче ход переходит к следующему игроку,
при второй же игрок вылетает из игры.

Победит тот кто отгадает слово.

За каждую отгаданную букву игроки получают очки.

В конце за очки можно будет купить призы.
"""
import random
import time
words = ["камень", "компьютер", "телевизор", "холодильник", "ножницы", "книга", "сертификат", "гравюра", "котёнок",
         "календарь", "пульт", "фонарь", "квартира", "система", "картинка", "дверь", "динамики", "самолёт", "ковёр",
         "тетрадь", "калькулятор", "кокос", "миндаль", "город", "колонки"]
game_wheel=[100,200,300,500,1000,"Сектор приз",0]
prizes_from_sector_prize=["сковородка","миксер","кофемолка","кофемашина","стол","стул"]
word = random.choice(words)
print(word)
split_word = list(word)
hidden_word = list("-" * len(word))

player_1 = input("Имя первого игрока:")
player_2 = input("Имя второго игрока:")
player_3 = input("Имя третьего игрока:")

score_1 = 0
score_2 = 0
score_3 = 0

attempts_1 = 2
attempts_2 = 2
attempts_3 = 2

names = [player_1, player_2, player_3]
current_player = names[0]
players = {player_1: [score_1, attempts_1], player_2: [score_2, attempts_2], player_3: [score_3, attempts_3]}


def display_game_board():
    print(names)
    print(" ".join(hidden_word))
    print("Ход игрока:", current_player)

"""111--111--111"""
def get_player_input():
    print("Крутим барабан")
    a=-1
    b=0
    game_wheel1 = game_wheel * 3
    for i in range(random.randint(5,10)):
        a += 2
        print(game_wheel1[a-1],"--|",game_wheel1[a],"|--",game_wheel1[a+1])
        b+=0.33
        time.sleep(b)

    chosen_sector=game_wheel1[a]
    if chosen_sector=="Сектор приз":
        print("Сектор приз на барабане")
        option=input("Выбирайте: приз или 2000 очков")
        if option=="приз":
            print("Вы выбрали приз,поэтому вы получаете",random.choice(prizes_from_sector_prize))
            update_game_state(player_variant=option)
        elif option=="2000 очков":
            chosen_sector=2000
            player_variant = input(
                "Введите одну букву или попробуйте сразу угадать слово,но помните,у вас на это 2 попытки,по истечению которых вы вылетаете из игры:")
            while player_variant == "":
                player_variant = input("Вы ничего не ввели,напишите одну букву или целое слово:")
            update_game_state(player_variant=player_variant,chosen_sector=chosen_sector)
    else:
        print("На барабане упало",chosen_sector)


    player_variant = input(
        "Введите одну букву или попробуйте сразу угадать слово,но помните,у вас на это 2 попытки,по истечению которых вы вылетаете из игры:")
    while player_variant == "":
        player_variant = input("Вы ничего не ввели,напишите одну букву или целое слово:")
    update_game_state(player_variant=player_variant)


def update_game_state(player_variant,chosen_sector):
    global current_player
    if player_variant=="приз":
        names.insert(0, names.pop(-1))
        names.remove(current_player)
        print("меняем игрока")
        current_player = names[0]
    elif len(player_variant) == 1:
        if player_variant in split_word:
            for i in range(len(word)):
                if split_word[i] == player_variant:
                    hidden_word[i] = player_variant
                    players[current_player][0] +=chosen_sector
        else:
            names.insert(0, names.pop(-1))
            print("меняем игрока")
            current_player = names[0]



    else:
        if player_variant == word:
            if hidden_word == list("-" * len(word)):
                players[current_player][0] += 1000
                print("Игрок", current_player, ", вы победили")
                buy_prizes()
            else:
                print("Игрок", current_player, ", вы победили")
                players[current_player][0] += 200
                buy_prizes()
        else:
            players[current_player][1] -= 1
            if players[current_player][1] == 0:
                print("Игрок", current_player, "вылетает из игры")

                names.insert(0, names.pop(-1))
                names.remove(current_player)
                print("меняем игрока")
                current_player = names[0]
                if len(players) == 1:
                    buy_prizes()
            else:
                names.insert(0, names.pop(-1))
                print("меняем игрока")
                current_player = names[0]



def buy_prizes():
    list_prizes = {"Велосипед": 300, "Ноутбук": 400, "Компьютер": 500, "Машина": 1000}
    print('\n'.join("{}: {}".format(k, v) for k, v in list_prizes.items()))
    print("Очков у вас:", players[current_player][0])
    variant = input("Введите название предмета,который вы бы хотели забрать:")
    while players[current_player][0] <= list_prizes[variant]:
        variant = input("Не хватает очков на это.Выберите что то другое:")


def main():
    while hidden_word != split_word and len(players) != 1:
        display_game_board()
        get_player_input()


main()
