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
        seq_wo_digits = get_filename_wo_digits_or_extension(popped, "_") 
        # get_str_wo_last_part(popped, "_")

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
                    if seq_wo_digits == get_filename_wo_digits_or_extension(
                            file_name, "_"):
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

    return seq_names_container


def get_extension(str):
    return str[str.rfind(".") + 1:]


def get_file_wo_extension(str):
    return str[:str.rfind(".")]


def has_digits(str, divider):

    digits = get_last_digits(str, divider)
    print("---------- digits")
    print(digits)
    if digits.isnumeric():
        return True
    else:
        return False


def get_last_digits(str, divider):
    """
    Will currently return anything before the extension, so a really crappy
    implementation
    """
    # Hacky way of checking files with spaces and dots, by turning them into
    # underscores
    str_wo_extension = get_file_wo_extension(str)
    str_only_underscores = str_wo_extension.replace(" ", "_")
    str_only_underscores = str_wo_extension.replace(".", "_")

    return_str = str_only_underscores[str_only_underscores.rfind("_") + 1:]

    return return_str


def get_filename_wo_digits_or_extension(str, divider):
    digits = get_last_digits(str, divider)
    return str[:str.find(digits)-1]


def get_divider_pre_digits(str, divider):
    digits = get_last_digits(str, divider)
    digits_start = str.find(digits)
    return str[digits_start-1: digits_start]
