# Методы

{% hint style="info" %}
Методы указывают объекту, что нужно сделать и как это нужно сделать.  
Объекты Python всегда имеют методы, даже если вы не определяете их самостоятельно.  Например, Python добавляет в каждый объект метод `__str__()`, который возвращает строковое представление объекта.
{% endhint %}

#### Статические методы и методы экземпляра

Объекты Python поддерживают два типа методов: `статические` методы и `методы экземпляра`.

`Статические методы` применяются ко всем объектам определенного типа и могут вызываться без создания экземпляра класса, к которому принадлежат методы.

`Методы экземпляра` применяются к конкретному объекту или экземпляру класса.

{% hint style="info" %}
**Примечание**

С технической точки зрения, Python поддерживает третий тип методов — `методы класса`. Методы класса похожи на статические методы, но они работают на уровне класса, а не на уровне объекта. Методы класса часто не используются, но если используются, то обычно для создания фабрик объектов. Дополнительные сведения о методах класса см. в разделе 

[Простое объяснение экземпляров, классов и статических методов в Python.](https://realpython.com/instance-class-and-static-methods-demystified/)
{% endhint %}

#### Пример статического метода

Класс `math` Python содержит несколько статических методов, которые помогают выполнять математические операции. Например, следующая инструкция вычисляет квадратный корень из 4:

```python
root = math.sqrt(4)
```

Можно написать похожий класс с именем `mathops`, который будет содержать ваши собственные математические операторы:

```python
class mathops:
    @staticmethod
    def square(val):
        return val * val
```

Ключевое слово `@staticmethod`, которое является "декоратором" метода, говорит Python, что `square` является статическим методом, а не методом экземпляра.

