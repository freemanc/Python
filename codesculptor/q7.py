n = 1000
numbers = range(2, n)

results = []

while len(numbers) > 0:
    results.append(numbers[0])
    numbers = [num for num in numbers if num % results[-1] != 0]
    
print len(results)
