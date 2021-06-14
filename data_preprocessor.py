import codecs
import csv


def classificate_file(filename):
    fp = codecs.open(filename, "r")
    reader = csv.reader(fp, delimiter=",", quotechar='"')

    positive_count = 1
    negative_count = 1
    for cell in reader:
        try:
            if int(cell[3]) > 3:
                f = open(make_filename(positive_count, True), "w")
                positive_count += 1
            else:
                f = open(make_filename(negative_count, False), "w")
                negative_count += 1

            f.write(cell[4])
            f.close()
        except ValueError:
            continue


def make_filename(count, positive):
    new_filename = "../data/train/"

    if positive:
        new_filename += "pos/review_pos_"
    else:
        new_filename += "neg/review_neg_"

    new_filename += str(count)
    new_filename += ".txt"

    return new_filename
