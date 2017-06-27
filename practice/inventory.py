# Inventory


def display_inventory(inventory):
    print("Inventory:")
    for i, n in inventory.items():
        print(str(n) + ' ' + i)

    print("Item Counts: " + str(len(inventory)))


def add_to_investory(investory, added_items):
    for item in added_items:
        if item in investory:
            investory[item] += 1
        else:
            investory[item] = 1

    return investory


stuff = {'ロープ': 3, '薬草': 5, 'たいまつ': 2, 'メダル': 8, '矢': 11}
display_inventory(stuff)

add_to_investory(stuff, ['ロープ', 'メダル', '毒消し草'])
display_inventory(stuff)
