# grid-commutators

## Установка

Устанавливаем cygwin, в нем устанавливаем следующие пакеты
* git
* gcc-g++
* make
* autoconf
* automake
* python38-pip
* python38-zmq
* python38-ipython

Запускаем консоль cygwin, в ней выполняем следующие команды: (то что в угловых скобках - надо заменить)
```
git clone https://github.com/vermaseren/form.git
cd form
autoreconf -i
./configure
make -j <количество ядер на вашей машине>
make install
cd ..
pip3.8 install python-form
git clone https://github.com/FeelUsM/grid-commutators.git
```

Если хотите поиграться с питоном и формом, выполните следующие команды
```
pip3.8 install jupyter
ln -s /cygdrive/c/Users/<USERNAME>/<YOUR WORK DIRECTORY>/ work
```

## Примеры

пример математики находится в `C:\cygwin64\home\<USERNAME>\grid-commutators\test.nb`

для запуска юпитер-ноутбука выполняйте следующую команду
`jupyter notebook`

примеры в папке grid-commutators
