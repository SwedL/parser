import os


res = 0

# files = os.listdir('images')
#
# for file in files:
#     res += os.path.getsize('images/' + file)

for root, dirs, files in os.walk('images'):
    print(root)
    print(dirs)
    print(files)
    for f in files:
        res += os.path.getsize(os.path.join(root, f))

print(res)
