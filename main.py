import data_preprocessor
import data_trainer

if __name__ == '__main__':
    data_preprocessor.classificate_file('review.csv')
    data_preprocessor.extract_test_data(10000)
    data_trainer.train()
