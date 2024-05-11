import argparse
import datetime
from operator import attrgetter
import dmodel
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def main():
    parser = argparse.ArgumentParser(description="Микро бухгалтерия, для кошелька")
    # subparse = parser.add_subparsers(title="action", dest="action")
    group = parser.add_mutually_exclusive_group()
    # Приход - опция задающая количество поступивших денег
    group.add_argument("-i", "--incoming", dest="incoming", help="Приход", type=int)
    # Расход - опция задающая количество израсходованных денег
    group.add_argument("-o", "--outgoing", dest="outgoing", help="Расход", type=int)
    # Задает фильтрацию по дате
    parser.add_argument("-d", "--find-by-date", dest="fbd", help="Поиск по дате 5.5.24 - только за это день или 5.5.24-6.5.24 тоже самое только диапазон", type=str)
    # Задает фильтрацию по сумме
    parser.add_argument("-s", "--find-by-summ", dest="fbs", help="Поиск по сумме", type=int)
    # Задает фильтрацию по включению в описание
    parser.add_argument("-c", "--find-by-desc", dest="fbc", help="Поиск по включению в описание", type=str)
    # Описание
    parser.add_argument("-x", "--desc", dest="desc", help="Описание", type=str)
    # Определяет дату и время в режиме редактирования
    parser.add_argument("-t", "--datetime", dest="datetime", help="Дата/Время - 8.5.24/10:24",type=str)
    # Режим редактирования -i и -o пределяют категорию и сумму, -x описание, -t дату/время
    parser.add_argument("-e", "--edit", dest="edit", help="Редактирование записи с id, -i и -o пределяют категорию и сумму, -x описание, -t дату/время", type=int)
    parser.add_argument("-r", "--remove", dest="remove", help="Удаление записи с id", type=int)
    # Один или более файлов для обработки
    parser.add_argument("files", metavar="data_files", type=str, nargs="+", help="Файлы данных")
    args = parser.parse_args()
    # если описание не определено то равно пустой строке
    if args.desc is None:
        args.desc = ""
    # для всех файлов
    for f in args.files:
        # Создать объект хранилища
        db = dmodel.DB()
        # Загрузить данные из файла
        db.load(f)
        # Если режим редактирования
        if args.edit is not None:
            # Создать пустую запись
            r = {}
            # Если установлен ключ  -i
            if args.incoming is not None:
                r["category"] = "incoming"
                r["summ"] = args.incoming
            # Если установлен ключ -o
            if args.outgoing is not None:
                r["category"] = "outgoing"
                r["summ"] = args.outgoing
            # Если установлен ключ -t
            if args.datetime is not None:
                r["date"] = datetime.datetime.strptime(args.datetime, "%d.%m.%y/%H:%M")
            # Если установлен ключ -x
            if args.desc is not None:
                r["desc"] = args.desc
            # Редактировать запись
            db.edit(args.edit, r)
        # Режим добавления записи
        elif args.remove is not None:
            db.remove(args.remove)
        else:
            if args.incoming is not None:
                # Добавить приход
                db.append_incoming(args.incoming, desc=args.desc)
            if args.outgoing is not None:
                # Добавить расход
                db.append_outgoing(args.outgoing, desc=args.desc)
            # Всего прищло
            i = 0
            # Всего ушло
            o = 0
            # Фильтруем по условиям поиска
            for r in db.find(args.fbd, args.fbs, args.fbc):
                dmodel.print_rec(r)
                if r["category"] == "incoming":
                    # Считаем общий приход
                    i += r["summ"]
                else:
                    # Считаем общий расход
                    o += r["summ"]
            # Напечатать приход, расход, баланс
            print("Приход:%d - Расход:%d = Баланс:%d"%(i, o, i-o))
        # Сохранить данные
        db.save(f)


if __name__ == "__main__":
    main()
