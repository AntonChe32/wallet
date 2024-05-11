import argparse
import datetime
import json


# Класс исключения
class EInvDateFormat(Exception):
    pass

# Распечатать запись
def print_rec(r):
    """ Распечатать запись """
    print("%d\t%s\t%s\t%d\t%s"%(r["id"], r["date"].strftime("%d.%m.%y/%H:%M"),
                                "Расход" if r["category"] == "outgoing" else "Приход",
                                   r["summ"],r["desc"]))


class DB:
    """
    Класс для работы с данными и конфигурацией
    """
    def __init__(self):
        """
        по ключу conf - хранится конфгурция
        по ключу data - хранятся данные
        last_id - последний идентификатор записи
        """
        self.db = {}
        self.db["conf"] = {}
        self.db["data"] = []
        self.last_id = -1

    def load(self, name:str):
        """
        @name - имя файла
        Загружает конфигурацию и данные из файла в формате json
        """
        try:
            self.db = json.load(open(name, "rt"))
            _id = 0
            for d in self.db["data"]:
                # Конвертировать все строки с датой в обьекты datetime
                d["date"] = datetime.datetime.fromisoformat(d["date"])
                if d["id"] > _id:
                    _id = d["id"]
            self.last_id = _id
        except FileNotFoundError:
            pass

    def save(self, name:str):
        """
        @name - имя файла
        Сохранить в фаил
        """
        for d in self.db["data"]:
            # Конветировать все обьекты datetime в строки
            d["date"] = d["date"].isoformat()
        json.dump(self.db, open(name, "wt"))

    def append_incoming(self, summ:int, desc:str=""):
        """
        @summ - сумма
        @desc - описание
        Добавить запись прихода
        """
        self.last_id += 1
        # Добавить запись прихода
        self.data_add = {"id":self.last_id,"date":datetime.datetime.now(), "summ":summ, "category":"incoming","desc":desc}

    def append_outgoing(self, summ:int, desc:str=""):
        """
        @summ - сумма
        @desc - описание
        Добавить запись расхода
        """
        self.last_id += 1
        self.data_add = {"id":self.last_id,"date":datetime.datetime.now(), "summ":summ, "category":"outgoing","desc":desc}

    def edit(self, id, e):
        r = self.get_by_id(id)
        for i in e:
            r[i] = e[i]


    def get_by_id(self, id) -> {}:
        """
        @id - идентфикатор записи
        Получить запись по id
        """
        for r in self.data_get:
            if r["id"] == id:
                return r

    def find(self,  dates:str, summ:int, desc:str) -> []:
        """
        @dates - дата или диапазон дат 5.5.24 или 5.5.24-10.5.24
        @summ - сумма
        @desc - подстрока описания
        Если значение  None - то соответствует всем записям
         Поиск записей
        """
        dd = ()
        if dates is not None:
            dd = dates.split("-")
        if len(dd) == 1:
            # Если нет разделителя "-" значит указана одна дата
            bd = datetime.datetime.strptime(dd[0], "%d.%m.%y")
            # Диапазон + сутки
            ed = datetime.datetime.fromtimestamp(bd.timestamp()+24*60*60)
        elif len(dd) == 2:
            # Разделитель есть значит даты 2е
            bd = datetime.datetime.strptime(dd[0], "%d.%m.%y")
            ed = datetime.datetime.strptime(dd[1], "%d.%m.%y")
        elif len(dd) == 0:
            pass
        else:
            raise EInvDateFormat()
        for r in self.data_get:
            if (dates is None or ( r["date"] >= bd and r["date"] < ed )) and \
                    (summ is None or ( r["summ"] == summ )) and \
                    (desc is None or (desc in r["desc"])):
                yield r
        return

    def iter(self):
        for i in self.data_get:
            yield i
    def remove(self, id:int):
        """
        @id - Идентификатор удаляемой записи
        Удалить запись с id
        """
        self.db["data"].remove(self.get_by_id(id))

    def __getattr__(self, item):
        if item.startswith("conf_"):
            return self.db["conf"][item[5:]]
        elif item == "data_get":
            return self.db["data"]
        # чтобы не было рекурсии
        return self.__getattribute__(item)

    def __setattr__(self, key, value):
        if key.startswith("conf_"):
            self.db["conf"][key[5:]]=value
        if key == "data_add":
            self.db["data"].append(value)
        else:
            # чтобы не было рекурсии
            object.__setattr__(self, key, value)
