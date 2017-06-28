# Align Table to Right Side

def align_table(table):
    max_width = [0] * len(table)
    row_num = len(table) #4
    column_num = len(table[0]) #5
    # datalist = [''] * row_num # '' * 5
    # tmptable = [datalist] * column_num # datalist * #4
    # tmptable =[[]]
    tmptable = [[0 for i in range(row_num)] for j in range(column_num)]
    print(column_num)
    print(row_num)
    for i in range(row_num):
        for j in range(column_num):
            tmptable[j][i] = table[i][j]
            # tmptable[j].append(table[i][j])
            width = len(table[i][j])
            print(tmptable[j][i])
            if max_width[i] < width:
                max_width[i] = width

    for i in range(column_num):
        for j in range(row_num):
            print(tmptable[i][j].rjust(max_width[j]), end=' ')

        print('')


align_table([['toritani', 'takayama', 'uemoto', 'itoi', 'umeno'],
             ['maru', 'kikuchi', 'tanaka', 'suzuki', 'arai'],
             ['murata', 'sakamoto', 'nagano', 'kamei', 'ishikawa'],
             ['yamada', 'yuhei', 'nakamura', 'hatakeyama', 'sakaguchi']])
