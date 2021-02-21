import re


a = 'as\ndf\nasdfffMTkkkk'

print([re.sub(r'[\n]*.*(?=MT)','',a)])

print(a[a.index('MT'):])