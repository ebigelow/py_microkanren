# microkanren in python

Translation of: https://github.com/jasonhemann/microKanren

I struggled a bit with some small details of translating scheme to python - note my reimplementation of `cons` and `cdr`. I think the py3 types help a lot with readability, though.

Unfortunately this still has at least one bug somewhere, since the `'ground appendo'` tests fail.

