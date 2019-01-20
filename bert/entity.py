import inflect

engine = inflect.engine()

entity = input('Enter Entity: ')
#plural toggles b/w singular and plural, and we need to use this since we must cover w2vec
#i.e, if input is 'vehicle', we must cover 'vehicle' as well as 'vehicles'
plural = engine.plural(entity)


read = open('Environment.txt', 'r')
write = open('Result.txt', 'w', encoding='utf-8')

for sentence in read:
        s = list(map(str.lower, sentence.split(' ')))
        if (entity in s) or (plural in s):
                write.write(sentence)