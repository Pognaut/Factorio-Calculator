import math
from csv import writer
from typing import LiteralString
import pandas as pd
from io import StringIO


def num_assem(items, number_sec, cat, depth, level):
   assems = math.ceil(number_sec / (float(df.at[items,'craftNum']) / float(df.at[items,'craftingTime'] / level)))  #items / (craftime/numcrafted) rounded up
   dict_add(assem_cat, items, assems)
   frame_add(items + '-assemblers', depth)
   frame_next(assems)
   return assems, cat

def num_smelt(items, number_sec, cat, depth, level):
   assems = math.ceil(number_sec / (float(df.at[items,'craftNum']) / float(df.at[items,'craftingTime'] / level)))  #items / (craftime/numcrafted) rounded up
   dict_add(cat, items, assems)
   frame_add(items + '-smelters', depth)
   frame_next(assems)
   return assems, cat

def num_refine(items, number_sec, cat, depth):
   assems = math.ceil(number_sec / (float(df.at[items,'craftNum']) / float(df.at[items,'craftingTime'])))  #items / (craftime/numcrafted) rounded up
   dict_add(cat, items, assems)
   frame_add(items + '-oil-refineries', depth)
   frame_next(assems)
   return assems, cat

def num_chem(items, number_sec, cat, depth):
   assems = math.ceil(number_sec / (float(df.at[items,'craftNum']) / float(df.at[items,'craftingTime'])))  #items / (craftime/numcrafted) rounded up
   dict_add(cat, items, assems)
   frame_add(items + '-chemical-plants', depth)
   frame_next(assems)
   return assems, cat

def ingreds(items, number_sec):
    lst = []
    i = 0
    b = 0
    while b == 0:
        plc = df.at[items,'ingredient'+str(i)]
        plc = str(plc)
        if plc == 'nan':
            b = 1
        else:
            plc = plc.split(":")
            plc[1] = (float(plc[1]) * float(number_sec)) / float(df.at[items,'craftNum'])
            lst.append(plc)
        i += 1
    return lst

def recursive_loop(lst, number_sec, depth):
    depth += 1
    for item in lst:
        if df.at[item[0],'ResourceType'] == ('basic' or 'liquid' or 'nuclear'):
            dict_add(item_cat, item[0], item[1])
            frame_add(item[0], depth)
            frame_next('Basic')
            frame_add((item[0]+'/sec'), depth)
            frame_next((item_cat[item[0]]))
            item_logger(item[0], all_items, type_test(item[0]))

        else:
            dict_add(item_cat, item[0], item[1])
            if df.at[item[0],'ResourceType'] == 'regular':
                num_assem(item[0], item[1], assem_cat, depth, assembler_level)

            elif df.at[item[0],'ResourceType'] == 'smelted':
                num_smelt(item[0], item[1], assem_cat, depth, smelter_level)

            elif df.at[item[0],'ResourceType'] == 'refined':
                num_refine(item[0], item[1], assem_cat, depth)

            elif df.at[item[0],'ResourceType'] == 'chem':
                num_chem(item[0], item[1], assem_cat, depth)

            frame_add((item[0]+'/sec'), depth)
            frame_next((item_cat[item[0]]))
            recursive_loop(ingreds(item[0], item[1]), number_sec, depth)
            item_logger(item[0], all_items, type_test(item[0]))

def type_test(item):
    return df.at[item,'ResourceType']

def total_print_out(dit):   #the numbers mason what do they mean
    print('\nTotals:------------------------------------')
    for resource in dit:
        print('') #for extra line

        if resource == item:
            print(resource)
        else:
            print(resource[0])

        print('\tNum/Sec:', end=' ')

        if resource == item:
            print(math.ceil(item_cat[resource]))
        else:
            print(math.ceil(item_cat[resource[0]]))

        if resource == item:
            im_too_tired_fo_ths = resource
        else:
            im_too_tired_fo_ths = resource[0]

        if df.at[im_too_tired_fo_ths,'ResourceType'] == 'regular': 
            if resource == item:
                plc = assem_cat[resource]
            else:
                plc = assem_cat[resource[0]]
            a_lst.append(plc)
            print('\tAssemblers:', end=' ') 
            print(plc)

        elif df.at[im_too_tired_fo_ths,'ResourceType'] == 'smelted':
            if resource == item:
                plc = assem_cat[resource]
            else:
                plc = assem_cat[resource[0]]
            s_lst.append(plc)
            print('\tSmelters:', end=' ') 
            print(plc)

        elif df.at[im_too_tired_fo_ths,'ResourceType'] == 'refined':
            if resource == item:
                plc = assem_cat[resource]
            else:
                plc = assem_cat[resource[0]]
            r_lst.append(plc)
            print('\tOil Refineries:', end=' ') 
            print(plc)

        elif df.at[im_too_tired_fo_ths,'ResourceType'] == 'chem':
            if resource == item:
                plc = assem_cat[resource]
            else:
                plc = assem_cat[resource[0]]
            c_lst.append(plc)
            print('\tChemical Plants:', end=' ')
            print(plc)

    if sum(a_lst) != 0:
        print('\n\nTotal Assemblers:', end=' ')
        print(sum(a_lst))

    if sum(s_lst) != 0:
        print('\nTotal Smelters:', end=' ')
        print(sum(s_lst))

    if sum(r_lst) != 0:
        print('\nTotal Oil Refineries:', end=' ')
        print(sum(r_lst))

    if sum(c_lst) != 0:
        print('\nTotal Chemical Plants:', end=' ')
        print(sum(c_lst))


def dict_add(cat, item, vari):
    if item in cat.keys():
        cat[item] += vari
    else:
        cat[item] = vari

def item_logger(item, dit, item_type):
    IDK_bruh = [item, item_type]
    if item not in dit:
        dit = dit.append(IDK_bruh)
    return dit


def frame_add(ipt, depth):
    SD.append('\n' + depth * (',') + str(ipt) + ',')


def frame_next(ipt):
    SD.append(str(ipt) + ',')



df = pd.read_csv('items.csv',)
df = df.set_index('name')
print('If you dont want to export do not type anything and hit enter')
file_name = input('File name: ')+'.xlsx'
while 1==1:
    assembler_level = input('Enter assembler level by typing the corresponding letter:\nAssembler 1: A\nAssembler 2: B\nAssembler 3: C\n').upper()
    if assembler_level == 'A':
        assembler_level = .5
        break
    elif assembler_level == 'B':
        assembler_level = .75
        break
    elif assembler_level == 'C':
        assembler_level = 1.25
        break
    else:
        print('Please type A, B, or C')

while 1==1:
    smelter_level = input('Enter smelter type by typing the corresponding letter:\nStone Furnace: A\nSteel or Electric Furnace: B\n').upper()
    if smelter_level == 'A':
        smelter_level = 1
        break
    elif smelter_level == 'B':
        smelter_level = 2
        break
    else:
        print('Please type A or B')




while 1 == 1:

    while 1==1:
        item_w_space = (input('Item: '))
        item_w_dash = item_w_space.replace(" ", "-")
        item = item_w_dash.lower()
        if item not in df['supported_items'].values:
            print(f'{item} not in supported items')
        else:
            break

    print(item, end='')
    num_sec = float(input('/sec: '))

    SD = [item + ',' + str(num_sec) + 48 * ',']
    assem_cat = {}
    item_cat = {item: num_sec}
    all_items = [item]
    depth = 0

    num_assem(item, num_sec, assem_cat, depth, assembler_level)
    ingredients = ingreds(item, num_sec)
    recursive_loop(ingredients, num_sec, depth)

    a_lst = []
    s_lst = []
    r_lst = []
    c_lst = []

    total_print_out(all_items)

    if len(a_lst) !=0:
        frame_add('Total Assemblers:', 0)
        frame_next(sum(a_lst))
    if len(s_lst) !=0:
        frame_add('Total Smelters:', 0)
        frame_next(sum(s_lst))
    if len(r_lst) !=0:
        frame_add('Total Oil Refineries:', 0)
        frame_next(sum(r_lst))
    if len(c_lst) !=0:
        frame_add('Total Chemical Plants:', 0)
        frame_next(sum(c_lst))

    SD = ''.join(map(str, SD))
    OP = pd.read_csv(StringIO(SD))

    if file_name != '.xlsx':
        with pd.ExcelWriter(file_name, mode = 'a', if_sheet_exists = 'replace') as writer:
            OP.to_excel(writer, sheet_name = item, index = False, header= False)

    loop = input('\nAnother? (y/n): ')
    if loop == 'n':
        break
