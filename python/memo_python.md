
# this is just python memo



-
  python -c 'print "A"*100'


- gdb with python
  1. argument 
    (gdb)run $(python -c 'print "A" * 200')

  2. scanf
    (gdb) r <<< $(python -c 'print "A"*1')

- breakpoint
disas main
b *main+20
b function_name
info b
delete br 1

- x
x / [Format] [Address]
x / [Length] [Format] [Address]
x/5x 0x8048680
x/s $r0
x/3i 0x80484a0
