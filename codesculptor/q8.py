num_slow = 1000
num_fast = 1
rate_slow = 1.2
rate_fast = 1.4

year = 1

while num_fast <= num_slow:
    num_slow *= rate_slow
    num_fast *= rate_fast
    year += 1
    
print year-1