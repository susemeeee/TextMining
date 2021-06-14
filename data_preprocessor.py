import codecs
import csv
import os
import shutil
import random


def classificate_file(filename):
    fp = codecs.open(filename, "r")
    reader = csv.reader(fp, delimiter=",", quotechar='"')

    positive_count = 1
    negative_count = 1
    for cell in reader:
        try:
            if int(cell[3]) > 3:
                f = open(make_filename(positive_count, True, False), "w")
                positive_count += 1
            else:
                f = open(make_filename(negative_count, False, False), "w")
                negative_count += 1

            f.write(cell[4])
            f.close()
        except ValueError:
            continue


def make_filename(count, positive, extract):
    new_filename = "../data/"

    if extract:
        new_filename += "test/"
    else:
        new_filename += "train/"

    if positive:
        new_filename += "pos/review_pos_"
    else:
        new_filename += "neg/review_neg_"

    new_filename += str(count)
    new_filename += ".txt"

    return new_filename


def extract_test_data(data_count):
    positive_path = "../data/train/pos"
    negative_path = "../data/train/neg"
    pos_file_list = os.listdir(positive_path)
    neg_file_list = os.listdir(negative_path)

    pos_numbers = set()
    neg_numbers = set()
    pos_file_count = len(pos_file_list)
    neg_file_count = len(neg_file_list)

    for i in range(0, data_count):
        random_index = random.randrange(1, pos_file_count + 1)
        while random_index in pos_numbers:
            random_index = random.randrange(1, pos_file_count + 1)

        pos_numbers.add(random_index)

        random_index = random.randrange(1, neg_file_count + 1)
        while random_index in neg_numbers:
            random_index = random.randrange(1, neg_file_count + 1)

        neg_numbers.add(random_index)

    for n in pos_numbers:
        shutil.move(make_filename(n, True, False), make_filename(n, True, True))
    for n in neg_numbers:
        shutil.move(make_filename(n, False, False), make_filename(n, False, True))
