# wallet

# Добавим приход
```
python wallet.py data -i 10000 -x "Ура 10000"
```
# Добавим расход
```
python wallet.py data -o 7000 -x "Подруга подкинула проблем 7000"
python wallet.py data -o 4000 -x "Подруга подкинула проблем 4000"
python wallet.py data -o 4000 -x "Подруга подкинула проблем столькоже"
```
# Просмотреть все
```
python wallet.py data 
```
# Найти все с суммой 4000
```
python wallet.py data -s 4000
```
# Найти все с включением в описание Подруга
```
python wallet.py data -c Подруга
```
# Редактировать запись с id == 3
```
python wallet.py data -e 3 -t 5.5.24/10:22 -i 5000 -x "Подруга подкинула бабла"
```
# Удалить запись c id == 2
```
python wallet.py data -r 2
```
# Просмотреть все
```
python wallet.py data 
```
# Найти все для 5.5.24 за сутки
```
python wallet.py data -d 5.5.24
```
# Найти все для интервала с 5.5.24 по 10.5.24 не включительно
```
python wallet.py data -d 5.5.24-10.5.24
```

