# Сайт веломарафонского клуба "Цепная реакция"

### Адрес
https://brevet.omskvelo.ru

### О сайте
Цель работы:
- систематизация разрозненной информации о деятельности веломарафонского движения в г. Омск
- автоматизация организации и документооборота
- мотивация участников на новые подвиги :)

### Стек
Python | Django | Bootstrap | PostgreSQL | Gunicorn | Nginx | Docker

### Deployment "с чистого листа"
1. Создать пользователя
```
adduser brevet
usermod -aG sudo brevet
su brevet
```

2. Сгенерировать SHH-ключ (у себя)
```

```

3. Установить Nginx, Docker, Git
```
sudo apt-get install docker
sudo usermod -aG docker brevet
sudo apt-get install nginx
sudo apt-get install git
```



### .gitignore
В исходный код не вошли необходимые для работы файлы:
- .env - файл, содержащий приватные ключи. Вместо него приведён шаблон .env.example.
- static\brevet\img\\* - статические изображения.
