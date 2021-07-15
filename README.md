# tdmelodic_userdict

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
    - show next sentence when it is 1.
    - return 1. when it is 2 or 3.
    - return 3. when it is 4

* another typing on 1.
    - prev: show previous sentence and can regist new yomi.
    - drop (num): drop registed yomi. num is regist yomi's index. If you do not input num, drop latest regist yomi.
