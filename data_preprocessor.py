import codecs
import csv
import os
import shutil
import random


# csv 파일을 열어 review를 txt 파일로 각각 변환
def classificate_file(filename):
    fp = codecs.open(filename, "r")
    reader = csv.reader(fp, delimiter=",", quotechar='"')

    positive_count = 1
    negative_count = 1
    for cell in reader:
        try:
            #평점이 4, 5인 경우 긍정적인 평가, 나머지는 부정적인 평가로 간주
            if int(cell[3]) > 3:
                f = open(make_filename(positive_count, True, False), "w", encoding="cp949")
                positive_count += 1
            else:
                f = open(make_filename(negative_count, False, False), "w", encoding="cp949")
                negative_count += 1

            f.write(cell[4])
            f.close()
        except ValueError:
            continue


#디렉토리, 파일 이름 작성
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


# csv파일에서 추출한 review들을 랜덤으로 테스트 데이터로 사용
def extract_test_data(data_count):
    positive_path = "../data/train/pos"
    negative_path = "../data/train/neg"
    #디렉토리에 있는 모든 파일 가져오기
    pos_file_list = os.listdir(positive_path)
    neg_file_list = os.listdir(negative_path)

    pos_numbers = set()
    neg_numbers = set()
    pos_file_count = len(pos_file_list)
    neg_file_count = len(neg_file_list)

    #랜덤으로 사용할 파일 번호 선정
    for i in range(0, data_count):
        random_index = random.randrange(1, pos_file_count + 1)
        while random_index in pos_numbers:
            random_index = random.randrange(1, pos_file_count + 1)

        pos_numbers.add(random_index)

        random_index = random.randrange(1, neg_file_count + 1)
        while random_index in neg_numbers:
            random_index = random.randrange(1, neg_file_count + 1)

        neg_numbers.add(random_index)

    #긍정적인 review와 부정적인 review 각각 test 데이터로 사용하기 위해 디렉토리 변경
    for n in pos_numbers:
        shutil.move(make_filename(n, True, False), make_filename(n, True, True))
    for n in neg_numbers:
        shutil.move(make_filename(n, False, False), make_filename(n, False, True))
