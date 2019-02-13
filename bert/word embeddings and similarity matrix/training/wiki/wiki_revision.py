import pywikibot

site = pywikibot.Site(u'en', fam=u'wikipedia')
wpage = pywikibot.Page(site, u'Coffee')

wpHist = wpage.fullVersionHistory(total=5)

for i in wpHist:
    print(i[3])