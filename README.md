# tdmelodic_userdict
### preparation
※If you can not use tdmelodic, please refer [tdmelodic](https://github.com/PKSHATechnology-Research/tdmelodic)
```
vi `mecab-config --dicdir`/tdmelodic/dicrc
```
add these
```
node-format-yomi = %m\t%f[1]\t%f[11]\t%f[17]\t%c\t%phl\n
unk-format-yomi  = %m\t?\t?\t?\t2\t1\n
eos-format-yomi  = EOS\tEOS\t\t
```
example  
```
./tdmelodic_userdict.sh --textfile /path/to/textfile --tdmelodic-dir /path/to/tdmelodic 
```

### Flow of regist dictionary
1. Show yomi and sentence(wakati). If you want to regist anothoer yomi, type 'y'
2. Show each words index. Specify index to regist yomi. You can specify several index like '2 4'.
3. Show target words and current yomi. Type yomi to regist.
4. Check regist yomi type at 3. If you verify this, type 'y'

* type enter
    - show next sentence when status is 1.
    - return 1. when status is 2 or 3.
    - return 3. when status is 4

* another typing on status 1.
    - prev: show previous sentence and can regist new yomi.
    - drop (num): drop registed yomi. num is registed yomi's index. If you do not input num, drop latest registed yomi.
