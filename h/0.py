from monitor import monit, report, clear

@monit(1)
def fib(a):
	if a == 0: return 1
	if a == 1: return 1
	return fib(a-1) + fib(a-2)

fib(6)
report(1, limits = {fib:(1,2)})
report(1,limits = {fib:(6,6)})
clear()


@monit(2)
def f(a):
	if a == 0:
		return 1;
	return f(a-1)*a

#f = monit(2)(f) -- monit(2) = convert, wiec monit(2)(f) = convert(f)

@monit(1)
def g(a, b):
	if b == 0:
		return 1
	return g(a, b-1) * f(a)

g(2, 2)

report(2)
report(1)
report(2, limits = {f:(1,2), g:(1,2)})
clear()
