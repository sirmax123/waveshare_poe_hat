# Простой скрипт для вывода на экран данных
* https://www.waveshare.com/poe-hat-b.htm
За основу взят официальный пример и немного переработан


# использование
* Скопировать файлы в соответвии с путями (корень репозитория соответвует корню системы
* `apt -y install python3-smbus python3-netifaces python3-willow` (`python3-rpi.gpio`).
* `vi  /boot/config.txt`; uncoment `dtparam=i2c_arm=on`
```
cat /boot/config.txt  | grep i2c
dtparam=i2c_arm=on
```
* add `i2c-dev` to `/etc/modules`
* reboot (что бы включить I2C
* указать правильный интерфейс (если он не eth0) в файле /etc/default/poe_hat
* `systemctl  start poe-hat-screen`
* `systemctl  status poe-hat-screen`
* `systemctl  enable poe-hat-screen`

# возможные проблемы
Проверить что i2c работает можно например так:
```
i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: 20 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
Ошибка вида 
```
Traceback (most recent call last):
  File "/usr/local/poe_hat/poe_hat.py", line 22, in <module>
    POE = POE_HAT_B.POE_HAT_B(font_size=12, font_name='Courier_New.ttf', string_height_in_pixels=10)
  File "/usr/local/poe_hat/lib/waveshare_POE_HAT_B/POE_HAT_B.py", line 36, in __init__
    self.i2c = smbus.SMBus(1)
FileNotFoundError: [Errno 2] No such file or directory
```
означает что i2c не включен (нет файла /dev/i2c-1), скорее всего это настройка в /boot/config.txt или не загружены модули
