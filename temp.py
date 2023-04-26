import os


res = 0

files = os.listdir('IMG')

for file in files:
    res += os.path.getsize('IMG/' + file)

print(res)
