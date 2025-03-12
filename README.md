# FloatingParser System

floatingparser — это библиотека для обработки логов FloatingServer, которая позволяет создать статистику по журналам событий.

# Особенности:  

- Простота использования: python "file_name.py" [args]
- Поддержка форматов логов: Поддерживает формат логов ".txt".

# Как начать работу с Floating Parser? 

1. Установите Floating Parser с помощью pip:
   
   `pip install floatingparser`
   
2. Импортируйте библиотеку в ваш проект:
   
   `import floatingparser as fp`
   
3. Создайте объект FloatingParser:
   
   `parser = fp.FloatingStart()`

4. Запустите ваш файл через командную строку и укажите нужные аргументы*:

   `python "file_name.py" [args]`

*-Список аргументов можно вывести с помощью --help (-h)
