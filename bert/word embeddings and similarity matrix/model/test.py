a = {4,21}
b = {6}
c = {9}
d = {11}
e = {18,4}
f = {4,21}
g = {23,11}
h = {25}

setlist = [a,b,c,d,e,g,f,h]
# setlist = [{8}, {46,9}, {18,10}, {18,67}, {107,19}, {144, 29}, {108, 38}, {50},
#             {53, 99}, {54, 67}, {63,99}, {73}, {74}, {67,75}, {76,177}, {78},
#             {81}, {83}, {93}, {18,94}, {67,102}, {74,103}, {107,114}, {108, 117}, {113, 168},
#             {67,114}, {119}, {120}, {123}, {128}, {75, 129}, {135}, {145, 144}, {145,67}, {67,151}, {54, 152}, {108, 54}, {162, 114}, {163}, {166,18}, {168,99}, {170,168}, {190,175}, {183,128}, {18, 187}, {190,99}]
# setlist = [{4,21}, {6}, {9}, {11}, {18,4}, {4,21}, {23,11}, {25}]
# setlist = frozenset(setlist)
# setlist = list(setlist)
#setlist = [{'4- To create gardens more.parks in each locality. Good roads without potholes. To grow trees on either side of the road. Escalator to be installed at sky walk for senior citizens. Good conveyance in the form of bus. Auto. Cabs. Metro. And rail. Good drainage without over flowing in rainy season. Good shelter near bus stop. Wash rooms or toilet near bus stop. With good maintainance.\n', '21- Though there has been efforts to improve the standard of footpaths, they end up being encroached by the illegal vendors and petty shops and forcing the pedestrians to walk on the roads and risk their lives. On many newly laid footpaths, the existing telephone exchange boxes or other utilities are not removed or relocated. These again forces pedestrians to walk on road.\n'}, {'6- Bangalore need to be planned properly \n'}, {'9- Until implemented, the plan is not satisfactory.\n'}, {'11- Please get our footpaths and greenary back. \n'}, {'4- To create gardens more.parks in each locality. Good roads without potholes. To grow trees on either side of the road. Escalator to be installed at sky walk for senior citizens. Good conveyance in the form of bus. Auto. Cabs. Metro. And rail. Good drainage without over flowing in rainy season. Good shelter near bus stop. Wash rooms or toilet near bus stop. With good maintainance.\n', '18- Build big arterial roads for sub urban networks\n'}, {'4- To create gardens more.parks in each locality. Good roads without potholes. To grow trees on either side of the road. Escalator to be installed at sky walk for senior citizens. Good conveyance in the form of bus. Auto. Cabs. Metro. And rail. Good drainage without over flowing in rainy season. Good shelter near bus stop. Wash rooms or toilet near bus stop. With good maintainance.\n', '21- Though there has been efforts to improve the standard of footpaths, they end up being encroached by the illegal vendors and petty shops and forcing the pedestrians to walk on the roads and risk their lives. On many newly laid footpaths, the existing telephone exchange boxes or other utilities are not removed or relocated. These again forces pedestrians to walk on road.\n'}, {'23- Roads are damaged from Doddamara to mahaveer orchids apartment. Please requesting to fix it as there are many incidents happening\n', '11- Please get our footpaths and greenary back. \n'}, {'25- Good thoughts, and will be helpful if implemented in a time bound manner.\n'}]


# index = 0
# for i in range(len(setlist)):
#     print(index)
#     for j in setlist[index+1:]:
#             if len(setlist[index] & j) > 0:
#                 print('union')
#                 print(setlist[index])
#                 print(j)
#                 setlist[index] = setlist[index].union(j)
#                 setlist = list(filter((j).__ne__, setlist))
#                 #setlist.remove(j)
#                 print(setlist)
#                 index = 0
#             else:
#                 index += 1

# print(setlist)

for i in setlist:
    print('i')
    print(i)
    print()
    for j in setlist:
        if i == j:
            continue
        print('j')
        print(j)
        print()
        if len(i & j) > 0 and i!=j:
            if i & j == i:
                setlist = list(filter((i).__ne__, setlist))
                continue
            if i & j == j:
                setlist = list(filter((j).__ne__, setlist))
                continue
            print(setlist)
            print(i)
            print(j)
            setlist.append(i.union(j))
            #print(setlist[setlist.index(i)])
            #setlist[setlist.index(i)] = i.union(j)
            if i > j:
                setlist = list(filter((j).__ne__, setlist))
            else:
                setlist = list(filter((i).__ne__, setlist))
            print(setlist)
    print()
print(setlist)
