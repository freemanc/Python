score = raw_input("Enter the score:")
try: 
    s = float(score)
    if s < 0:
        print 'out of range'
    elif s > 1:
        print 'out of range'
    else:
        if s >= 0.9:
            letter = 'A'
        elif s >= 0.8:
            letter = 'B'
        elif s >= 0.7:
            letter = 'C'
        elif s >= 0.6:
            letter = 'D'
        else:
            letter = 'F'
        print letter
except:
    print 'not a number'
