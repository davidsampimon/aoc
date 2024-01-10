import ctypes

g_list = [1, 2, 3]

def myfunc():
    l_dict = {"foo": 1}
    return id(l_dict), l_dict

def myfunc_2():
    h_list = [9, 10, 11]
    return h_list


if __name__ == "__main__":
    myfunc()
    obj_id, l_dict = myfunc()
    my_list = myfunc_2()
    my_list.append(7)
    del l_dict
    tmp_list = [3, 2, 1]
    print(obj_id)
    print(ctypes.cast(obj_id, ctypes.py_object).value)