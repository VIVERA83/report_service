Тестовое задание.

запуск
```bash
python main.py "data/data1.csv" "data/data2.csv" "data/data3.csv" --report payout
```
main.py
```python
# порядок вывода отчета на экран по столбцам.
# ключ - имя поля: 
# значение - новое название столбца, пробел означает '_'
# сортировка по ключам.
columns = {
    "department": " ",
    "name": "name",
    "hours_worked": "hours",
    "hourly_rate": "rate",
    "payout": "payout",
},
# под итог в группах, выводится под соответствующем столбцом
subtotal_columns = ["hours_worked", "payout"],
# группировка по столбцу
group = "department",

```


![img.png](img.png)

