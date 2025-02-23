#Random name suffixes for a file for identification
import string
import random

N = 7
res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
print("tab_"+res)
