x = 10
def func():
  a0 = 1
  a1 = 2
  a1 = a1 * a1
  a2 = 10
  a3 = a0 + a1

  if a2 & 1:
    a4 = (a3 - 1 if a1 else a3 - 2)
    print(a4)
  else:
    a5 = a2 + 1
    print(a5)
func()
y = 20
z = x + y
