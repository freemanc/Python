Python Notes
============

## Basics

```
x = raw_input(‘Enter x:’)
print ‘x =’, x	# space introduced
```

- variable names: **start** with letters or underscore (not number); case sensitive
- conversion functions: int(), float(), str(), type()
- math operators: power(**), modulus(%), add(+) works for strings
- other functions: max('Aa')='a'

## Conditional Statements

**Cautious about indent and space!**

```
if condition 1:
	statements 1
elif condition 2:
	statements 2
else:
	statements 3
```

```
# try to run statements 1. If blows up, not resulting error but run statements 2 instead.
try:
	statements 1
except:
	statements 2
```

## Writing Functions

```
def function_name(arg1, arg2, …):
	statements
	return var 
	# return statement can be missing, 
	# which is referred to as a “non-fruitful” function
```

## Loops and Iteration

- while loop (indefinite) ('break' and 'continue')
- for loop (definite)
- 'is' and 'is not': logical operators (means "exactly the same", not to overuse)

## Strings

- string type: read and convert
- indexing: start from 0; len(str)
- slicing: [a:b], b is the one beyond NOT included; [a:];[:b]; [:]
- loop through a string
- concatenating: +
- 'in' operator used with string
- string comparison ==, <, >
- string library: search, replace, strip white space, etc.

## Files

- open('filename', MODE), MODE = 'r', 'w', return a file_handle
- newline character: \n, is treated as length 1 and as white space(rstrip)
- loop over file_handle, which is a list of lines
- string.functions, 'startswith', 'in' operator
- skipping with 'continue'
- file_handle.read(): read the whole file into a single string

## Lists

- concept of a collection; lists and definite loops
- indexing and lookup; list mutability
- functions: len, min, max, sum; slicing lists
- list methods: append, remove; sorting lists
- splitting strings into lists of words; using split to parse strings

## Dictionaries

- dictionaries (aka. associative arrays) are another collection (key/value); vs lists (linear)

```
## construct a dictionary purse
purse = dict()
purse['money'] = 12
purse['tissue'] = 3
purse['candy'] = 15
## alternative
purse = {'money':12, 'tissue':3, 'candy':15}
```

- important pattern: the most common word (use dictionary to record frequency for each word)
- using the get() method: dict.get('keyname', 0)

```
counts = dict()
names = ['csev','cwen','csev','zqian','cwen']
for name in names:
	counts[name] = counts.get(name, 0) + 1
print counts
```

- for-loop with dictionaries: loop over the keys
- writing dictionary loops
	- list(dict): return a list of keys
	- dict.keys(): return a list of keys
	- dict.values(): return a list of values
	- dict.items(): return a list of (key:value) pairs/**tuples**

```
for key,value in dict.items():
	print key,value
```

## Tuples

- tuple syntax: 'count', 'index'
- mutability (not)
- comparability
- sortable (a list of tuples)
- tuples in assignment statements

```
(x, y) = (4, 'fred')
a, b = (99, 98)
```

- tuples in functions (adv)

```
## List Comprehension
c = {'a':10, 'b':1, 'c':22}
print sorted( [ (v,k) for k,v in c.items() ] )
```

- using sorted() on tuple to return a list
- **sorting dictionaries** by either key or value(create a temperary reversed tuples' list)