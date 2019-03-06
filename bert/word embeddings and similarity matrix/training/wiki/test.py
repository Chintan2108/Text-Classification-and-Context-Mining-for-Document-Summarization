import difflib
import mwparserfromhell
# + = first arg
# - = second arg

text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor.  In nec mauris eget magna consequat
convalis. Nam sed sem vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
tristique enim. Donec quis lectus a justo imperdiet tempus."""

text1_lines = text1.splitlines()

text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor. In nec mauris eget magna consequat
convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a
justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text2_lines = text2.splitlines()

# import pandas as pd

# df = pd.read_csv('./results/Coffee_editComments.csv')

# text1lines = df['content'][1]
# text2lines = df['content'][0]


# #print(text1lines)
# temp = open('test.txt', 'w', encoding='utf-8')
# text1lines = mwparserfromhell.parse(text1lines)
# #print(text1lines)
# for line in text1lines.split('\n'):
#     temp.write(line)
#     print('***************************************************************')

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
#print('\n'.join(diff))
for df in diff:
    print(df)
    # if ('?' in df):
    #     continue
    # if ('-' in df):
    #     print(df)
#print('.\n'.join(diff))

