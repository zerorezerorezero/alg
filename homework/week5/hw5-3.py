# 自製 map
def my_map(func, data):
    if data == []:
        return []

    return [func(data[0])] + my_map(func, data[1:])


# 自製 filter
def my_filter(func, data):
    if data == []:
        return []

    if func(data[0]):
        return [data[0]] + my_filter(func, data[1:])
    else:
        return my_filter(func, data[1:])


# 自製 reduce
def my_reduce(func, data, initial):
    if data == []:
        return initial

    return my_reduce(
        func,
        data[1:],
        func(initial, data[0])
    )


# 一次泡沫排序的「一趟」
def bubble_pass(data):
    if len(data) <= 1:
        return data

    a = data[0]
    b = data[1:]

    # 找出後面比 a 小的元素
    smaller = my_filter(lambda x: x < a, b)

    if smaller:
        # 找出最小值
        minimum = my_reduce(lambda x, y: x if x < y else y,
                            smaller,
                            smaller[0])

        # 把 minimum 放到前面
        remaining = my_filter(lambda x: x != minimum, data)

        return [minimum] + bubble_pass(remaining)

    else:
        return [a] + bubble_pass(b)


# 泡沫排序
def bubble_sort(data):
    if len(data) <= 1:
        return data

    result = bubble_pass(data)

    # 如果排序前後一樣，代表已經完成
    if result == data:
        return result

    return bubble_sort(result)


data = [9, 5, 3, 8, 1, 2]

print("原始資料：", data)
print("排序結果：", bubble_sort(data))