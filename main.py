import data_preprocessor

if __name__ == '__main__':
    data_preprocessor.classificate_file('review.csv')
    data_preprocessor.extract_test_data(10000)
