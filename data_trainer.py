import nltk
from sklearn.datasets import load_files
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def train():
    # 파일 디렉토리 열기
    reviews_train = load_files("../data/train/", encoding="cp949")
    reviews_test = load_files("../data/test/", encoding="cp949")

    #학습데이터, 테스트 데이터와 그에 대한 정답
    text_train, y_train = reviews_train.data, reviews_train.target
    text_test, y_test = reviews_test.data, reviews_test.target

    # 리뷰의 학습 데이터에 대한 BOW 생성(CountVectorizer 사용)
    vect = CountVectorizer().fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)

    # 나이브베이즈 분류 기법
    train_naivebayes(x_train, y_train, x_test, y_test)
    #Logistic Regression 분류 기법
    train_logisticregression(x_train, y_train, x_test, y_test)

    # 최소 등장 토큰 수를 부여하고 BOW 생성
    for i in range(2, 11):
        vect = CountVectorizer(min_df=i).fit(text_train)
        x_train = vect.transform(text_train)
        x_test = vect.transform(text_test)
        print("min_df: " + str(i) + " 적용")
        train_logisticregression(x_train, y_train, x_test, y_test)
        
    # 최대 등장 토큰 수를 부여하고 BOW 생성
    for i in range(1, 11):
        if 100 % i != 0:
            continue

        vect = CountVectorizer(max_df=(100/i)).fit(text_train)
        x_train = vect.transform(text_train)
        x_test = vect.transform(text_test)
        print("max_df: " + str(100/i) + " 적용")
        train_logisticregression(x_train, y_train, x_test, y_test)
    
    # 불용어 제거
    vect = CountVectorizer(stop_words="english").fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)
    print("불용어 제거 적용")
    train_logisticregression(x_train, y_train, x_test, y_test)

    # TF-IDF 사용해서 BOW 생성
    vect2 = TfidfVectorizer().fit(text_train)
    x_train2 = vect2.transform(text_train)
    x_test2 = vect2.transform(text_test)
    print("TF-IDF로 BOW 생성")
    train_logisticregression(x_train2, y_train, x_test2, y_test)

    # n-gram 방식 적용
    vect = CountVectorizer(ngram_range=(2, 2)).fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)
    print("n-gram 방식 적용(Bigram)")
    train_logisticregression(x_train, y_train, x_test, y_test)

    vect = CountVectorizer(ngram_range=(1, 3)).fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)
    print("n-gram 방식 적용(1-gram ~ trigram)")
    train_logisticregression(x_train, y_train, x_test, y_test)

    # stemming 기능 추가
    vect = CountVectorizer(tokenizer=tokenize).fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)
    print("stemming 기능 추가")
    train_logisticregression(x_train, y_train, x_test, y_test)

    # 가장 정답률이 높은 경우
    vect = CountVectorizer(ngram_range=(1, 5)).fit(text_train)
    x_train = vect.transform(text_train)
    x_test = vect.transform(text_test)
    print("n-gram 방식 적용(1-gram ~ 5-gram)")
    train_logisticregression(x_train, y_train, x_test, y_test)


# 나이브베이즈 분류 기법 사용
def train_naivebayes(x_train, y_train, x_test, y_test):
    nb = MultinomialNB()
    nb.fit(x_train, y_train)
    pre = nb.predict(x_test)

    #정답률 계산
    ac_score = metrics.accuracy_score(y_test, pre)
    print("NaiveBayes 사용 정답률: ", ac_score)


# LogisticRegression 분류 기법 사용
def train_logisticregression(x_train, y_train, x_test, y_test):
    clf = LogisticRegression()
    clf.max_iter = 2000
    clf.fit(x_train, y_train)
    pre = clf.predict(x_test)

    #정답률 계산
    ac_score = metrics.accuracy_score(y_test, pre)
    print("Logistic Regression 사용 정답률: ", ac_score)


# stemming 기능
def tokenize(text):
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))

    return stemmed
