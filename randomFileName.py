#Random name suffixes for a file for identification

N = 7
res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
print("tab_"+res)
