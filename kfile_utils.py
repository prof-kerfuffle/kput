import os


def list_files_w_ext(dir, ext):
    fileList = []

    for file in os.listdir(dir):
        if file[-len(ext):] == ext:
            fileList.append(file)

    return fileList


def list_files(dir):
    fileList = []

    for file in os.listdir(dir):
        fileList.append(file)

    return fileList


def get_files_wo_str(dir, str):
    return_list = []
    all_files = list_files(dir)

    # return_list = all_files

    files_w = []

    for file in all_files:
        #
        # check if file is dir
        #
        if os.path.isdir(dir + "\\" + file) is False:
            #
            # .find returns -1 if string is not found
            #
            if (file.find(str) == -1):
                return_list.append(file)
                # files_wo_str.append ()
                return_list.append(file)

    return return_list


def get_file_seqs(dir, divider):
    #    return_list = []
    all_files = list_files(dir)

    files_w_digits = []

    for file in all_files:
        #
        # check if file is dir
        #
        if os.path.isdir(dir + "\\" + file) is False:
            #
            # .find returns -1 if string is not found
            #

            #            print (has_digits (file, divider))
            #

            if has_digits(file, divider):
                files_w_digits.append(file)

    seq_names_container = []

    timeout = 0
    while (len(files_w_digits) > 0 and timeout < 500):
        timeout += 1
        # print (timeout)
        popped = files_w_digits.pop(0)
        seq_wo_digits = get_str_wo_last_part(popped, "_")

        found_seq_i = -1

        # if list is empty, add first seq_name, so there s something
        # to compare to
        if len(seq_names_container) == 0:
            seq_names_container.append([popped])
        # print ("added_first")
        # else loop through the sublists looking for a matching string
        # name, minus the digits
        else:
            for seq_name_container_i in range(len(seq_names_container)):
                # for s in seq_names:
                for file_name in seq_names_container[seq_name_container_i]:
                    if seq_wo_digits == get_str_wo_last_part(file_name, "_"):
                        found_seq_i = seq_name_container_i
                        continue
                    if found_seq_i >= 0:
                        continue

            # if a sub array has been found containing the same seq file
            # name (without the digits), add it to that sub array
            if found_seq_i >= 0:
                seq_names_container[seq_name_container_i].append(popped)
            # else create a new sub array
            else:
                seq_names_container.append([popped])

    # print ("seq seq_names_container")
    # print (seq_names_container)

    # for f in files_w_digits:

    # if (file.find (str) == -1):
    #     return_list.append (file)
    #     #files_wo_str.append ()
    #     return_list.append (file)

    # print (files_w_digits)
    return seq_names_container

# checks if the last part of the name consists of digits
# example: name_1001


def has_digits(str, divider):
    digits = get_last_digits(str, divider)
    if digits.isnumeric():
        return True
    else:
        return False


def get_last_digits(str, divider):
    split = str.split(divider)
    return_str = split[len(split)-1]
    return_str = return_str.split(".")[0]
    return return_str


def get_str_wo_digits(str, divider):
    split = str.split(divider)
    appended = ""

    for i in range(len(split)):
        #    for f in split:
        appended += split[i]
    return_str = appended
    # return_str = split [len(split)-1]
    # return_str = return_str.split (".")[0]
    return return_str


def get_str_wo_last_part(str, separator):
    return_str = ""

    #
    # str.rfind will return the last instance of a str
    #
    return_str = str[:str.rfind(separator)]
    return return_str
