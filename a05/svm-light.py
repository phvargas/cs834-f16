import os
import sys
from time import strftime, localtime, time
from nltk.corpus import reuters
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
import gzip
from sklearn.feature_extraction.text import TfidfVectorizer

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  December 13, 2016 at 19:07:58'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

cachedStopWords = stopwords.words("english")
word_dic = {}
word_set = set()


def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # creating vocabulary
    # create_vocabulary()

    # upload vocabulary
    idx = 0
    with open('words', 'r') as f:
        for record in f:
            idx += 1
            word_dic[record.strip()] = idx
            word_set.add(record.strip())

    #find_features('bank')

    # create training and test reuters doc-id
    # write_pos_train()
    # write_neg_train()

    # create training file
    #write_train_data('train.dat', 'w', 'positive.dat', '1')
    #write_train_data('train.dat', 'a', 'negative.dat', '-1')

    # create test file
    write_train_data('test.dat', 'w', 'positive-test.dat', '+1')
    write_train_data('test.dat', 'a', 'negative-test.dat', '-1')

    # collection_stats()

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.4f seconds' % (time()-start))
    return


def collection_stats():
    # List of documents
    documents = reuters.fileids()
    print(str(len(documents)) + " documents")

    train_docs = list(filter(lambda doc: doc.startswith("train"), documents))
    print(str(len(train_docs)) + " total train documents")

    test_docs = list(filter(lambda doc: doc.startswith("test"), documents))
    print(str(len(test_docs)) + " total test documents")

    # List of categories
    categories = reuters.categories()
    print(categories)
    print(str(len(categories)) + " categories")

    # Documents in a category
    category_docs = reuters.fileids("acq")

    # Words for a document
    document_id = category_docs[0]
    document_words = reuters.words(category_docs[0])
    print(document_words)

    # Raw document
    # print(type(reuters.raw(document_id)))
    for document_id in documents:
        text = tokenize(reuters.raw(document_id))
        if 'icx' in text and 'inc' in text and 'said' in text:
            print('Getting tfidf for %s --------->' % document_id)
            tfidf_text = tokenize(reuters.raw(document_id))
            tfidf = tf_idf(reuters.raw(document_id))
            print(tfidf_text)
            print(tfidf)

    # get_after(406429, 50)

    return


def write_train_data(train_file, mode, train_data_file, pos_neg):
    # get training data
    train_data = []
    with open(train_file, mode) as w_file:
        with open(train_data_file, 'r') as f:
            for record in f:
                record = record.strip()
                # include index
                train_data.append(record)

                # get TFIDF features for document
                features = tf_idf(reuters.raw(record))

                unorder_list= {}

                print(pos_neg, end=' ')
                w_file.write('%s ' % pos_neg)
                for key, value in features:
                    unorder_list[word_dic[key]] = value
                    # print('%d:%f' % (word_dic[key], value), end=' ')

                for key in sorted(unorder_list):
                    print('%d:%f' % (key, unorder_list[key]), end=' ')
                    w_file.write(' %d:%f' % (key, unorder_list[key]))

                print()
                w_file.write('\n')
    return


def find_features(feature):
    feature = tokenize(feature)[0]
    documents = reuters.fileids()

    id_array = []
    for id in documents:
        doc = reuters.raw(id)
        first_line = doc.split('\n')[0]
        if feature in tokenize(first_line) and len(doc) > 500:
            print('<----------- %s -------------->' % id)
            print(doc)
            print(len(doc))
            id_array.append(id)

    print(id_array)
    print(len(id_array))
    categories = reuters.categories()
    print(categories)

    return id_array


def get_after(line_no, number_lines):
    line_counter = 0
    with gzip.open('reuters21578.tar.gz', mode='rt', encoding='iso-8859-1') as file:
        for line in file:
            line_counter += 1
            if line_no <= line_counter <= line_no + number_lines:
                print(line.strip())
    return


# Return the representer, without transforming
def tf_idf(docs):
    tfidf = TfidfVectorizer(min_df=1, vocabulary=word_set,
                        use_idf=True, sublinear_tf=True, max_df=0.98,
                        norm='l2')
    doc_tokenize = tokenize(docs)
    tfidf.fit(doc_tokenize)

    return feature_values(' '.join(doc_tokenize), tfidf)


def feature_values(doc, representer):
    doc_representation = representer.transform([doc])
    features = representer.get_feature_names()

    return [(features[index], doc_representation[0, index])
                 for index in doc_representation.nonzero()[1]]


def tokenize(text):
    min_length = 3
    words = map(lambda word: word.lower(), word_tokenize(text))
    words = [word for word in words if word not in cachedStopWords]
    tokens = (list(map(lambda token: PorterStemmer().stem(token), words)))
    p = re.compile('[a-zA-Z]+')
    filtered_tokens = list(filter(lambda token: p.match(token) and len(token)>=min_length, tokens))
    return filtered_tokens


def write_pos_train():
    doc_id = ['test/14826', 'test/14882', 'test/15095', 'test/15271', 'test/15313', 'test/15368', 'test/15500',
              'test/15618', 'test/15653', 'test/15725', 'test/15737', 'test/15798', 'test/15871', 'test/15890',
              'test/15911', 'test/15916', 'test/15927', 'test/15975', 'test/16079', 'test/16126', 'test/16525',
              'test/17686', 'test/18519', 'test/19101', 'test/19480', 'test/19672', 'test/19835', 'test/19918',
              'test/19947', 'test/20382', 'test/20469', 'test/21031', 'test/21502', 'test/21506', 'test/21567',
              'test/21570', 'training/10011', 'training/10175', 'training/1023', 'training/10275', 'training/1067',
              'training/10845', 'training/10873', 'training/10882', 'training/10956', 'training/10959', 'training/11183',
              'training/11208', 'training/11230', 'training/11316', 'training/11658', 'training/11778', 'training/11885',
              'training/12052', 'training/1210', 'training/12361', 'training/12417', 'training/12428', 'training/1257',
              'training/12754', 'training/12887', 'training/13094', 'training/13123', 'training/13170', 'training/13179',
              'training/13269', 'training/13294', 'training/1347', 'training/1399', 'training/1478', 'training/1640',
              'training/1863', 'training/1907', 'training/2044', 'training/2115', 'training/2172', 'training/228',
              'training/2456', 'training/2688', 'training/275', 'training/2767', 'training/2973', 'training/2977',
              'training/3017', 'training/3048', 'training/311', 'training/3282', 'training/3285', 'training/3324',
              'training/3339', 'training/3340', 'training/3556', 'training/3901', 'training/3955', 'training/4022',
              'training/4028', 'training/4039', 'training/4101', 'training/4103', 'training/4129', 'training/4296',
              'training/4785', 'training/501', 'training/5134', 'training/5175', 'training/5185', 'training/5371',
              'training/5471', 'training/5531', 'training/5973', 'training/6127', 'training/6189', 'training/6623',
              'training/6626', 'training/684', 'training/6926', 'training/6959', 'training/6968', 'training/7336',
              'training/7357', 'training/75', 'training/7531', 'training/7579', 'training/7957', 'training/7962',
              'training/8149', 'training/8982', 'training/9060', 'training/9166', 'training/9222',
              'training/924', 'training/9592', 'training/9738', 'training/9763', 'training/9865', 'training/9905']

    with open('positive.dat', 'w') as f:
        for record in doc_id[:100]:
            f.write('%s\n' % record)

    with open('positive-test.dat', 'w') as f:
        for record in doc_id[101:131]:
            f.write('%s\n' % record)
    return


def write_neg_train():
    doc_id = ['test/14951', 'test/15287', 'test/15290', 'test/15306', 'test/15313', 'test/15893', 'test/16094',
              'test/16225', 'test/16357', 'test/17443', 'test/17923', 'test/18554', 'test/19165', 'test/19555',
              'test/19982', 'test/20186', 'test/20649', 'training/10043', 'training/10324', 'training/105',
              'training/10636', 'training/11043', 'training/11225', 'training/11260', 'training/11451',
              'training/11706', 'training/11771', 'training/1215', 'training/12563', 'training/12787', 'training/176',
              'training/1975', 'training/2175', 'training/2436', 'training/254', 'training/2557', 'training/267',
              'training/2936', 'training/2942', 'training/3010', 'training/303', 'training/313', 'training/3330',
              'training/3401', 'training/3770', 'training/4031', 'training/4047', 'training/4048', 'training/4138',
              'training/4172', 'training/4289', 'training/4525', 'training/46', 'training/4630', 'training/4833',
              'training/5152', 'training/5315', 'training/5800', 'training/5908', 'training/6344', 'training/6946',
              'training/7529', 'training/7611', 'training/8132', 'training/8161', 'training/8446', 'training/8624',
              'training/8683', 'training/9163', 'training/991', 'training/9959', 'test/15666',
              'test/16171', 'test/16196', 'test/17477', 'test/17759', 'test/18150', 'test/18565', 'test/18599',
              'test/18700', 'test/18744', 'test/18858', 'test/18902', 'test/19367', 'test/19534', 'test/19775',
              'test/20389', 'test/21561', 'training/10015', 'training/10720', 'training/10903', 'training/1105',
              'training/11437', 'training/11444', 'training/11541', 'training/11830', 'training/11880', 'training/1226',
              'training/1572', 'training/1711', 'training/1848', 'training/2965', 'training/3204', 'training/3855',
              'training/3888', 'training/3950', 'training/4035', 'training/4507', 'training/5345', 'training/5391',
              'training/5506', 'training/5683', 'training/5791', 'training/6058', 'training/6062', 'training/6086',
              'training/6125', 'training/6163', 'training/6581', 'training/6585', 'training/6598', 'training/6606',
              'training/6746', 'training/6994', 'training/7001', 'training/7037', 'training/7150', 'training/7216',
              'training/7336', 'training/7515', 'training/7625', 'training/8117', 'training/8134', 'training/833',
              'training/8598', 'training/8623', 'training/8820', 'training/8835', 'training/9795', 'training/9933',
              'training/9982']

    doc_id = ['test/14843', 'test/14913', 'test/15055', 'test/15364', 'test/15410', 'test/15431', 'test/15467',
              'test/15543', 'test/15615', 'test/15816', 'test/15841', 'test/15987', 'test/16063', 'test/16111',
              'test/16118', 'test/16119', 'test/16150', 'test/16177', 'test/16189', 'test/16312', 'test/16399',
              'test/16434', 'test/16565', 'test/16619', 'test/16644', 'test/16853', 'test/17041', 'test/17470',
              'test/17872', 'test/17896', 'test/18488', 'test/18564', 'test/18609', 'test/18642', 'test/18875',
              'test/18904', 'test/18911', 'test/19022', 'test/19075', 'test/19167', 'test/19198', 'test/19307',
              'test/19371', 'test/19412', 'test/19511', 'test/19512', 'test/19541', 'test/20226', 'test/20262',
              'test/20279', 'test/20324', 'test/20340', 'test/20384', 'test/20744', 'test/20794', 'test/20834',
              'test/21028', 'test/21248', 'test/21322', 'test/21342', 'test/21477', 'test/21497', 'test/21510',
              'test/21535', 'test/21539', 'training/100', 'training/10025', 'training/10049', 'training/10347',
              'training/10354', 'training/10357', 'training/10358', 'training/10382', 'training/10625', 'training/10632',
              'training/10644', 'training/10654', 'training/10710', 'training/10754', 'training/1076', 'training/109',
              'training/11123', 'training/11203', 'training/11234', 'training/11244', 'training/11349', 'training/11817',
              'training/11848', 'training/1193', 'training/11982', 'training/12084', 'training/12197', 'training/12333',
              'training/12394', 'training/12397', 'training/12400', 'training/12410', 'training/12422', 'training/12437',
              'training/12480', 'training/12576', 'training/12731', 'training/12732', 'training/12795', 'training/12848',
              'training/13231', 'training/13262', 'training/13321', 'training/13530', 'training/13543', 'training/14715',
              'training/14779', 'training/1560', 'training/1724', 'training/1858', 'training/1919', 'training/1933',
              'training/1960', 'training/1995', 'training/2097', 'training/220', 'training/2228', 'training/2725',
              'training/281', 'training/2810', 'training/2827', 'training/2956', 'training/3002', 'training/3007',
              'training/3043', 'training/3068', 'training/3128', 'training/3131', 'training/3133', 'training/3137',
              'training/3192', 'training/3222', 'training/3351', 'training/3360', 'training/3411', 'training/3435',
              'training/3449', 'training/3483', 'training/3493', 'training/3528', 'training/3534', 'training/3539',
              'training/3542', 'training/3825', 'training/4012', 'training/4019', 'training/4067', 'training/4088',
              'training/4297', 'training/441', 'training/4548', 'training/4600', 'training/4604', 'training/4654',
              'training/4666', 'training/4717', 'training/4835', 'training/5042', 'training/5070', 'training/5113',
              'training/5156', 'training/5201', 'training/5206', 'training/5253', 'training/5255', 'training/5271',
              'training/5272', 'training/5323', 'training/5330', 'training/5453', 'training/5609', 'training/5672',
              'training/5719', 'training/6158', 'training/6178', 'training/6246', 'training/6352', 'training/6369',
              'training/6384', 'training/6453', 'training/6483', 'training/6511', 'training/6658', 'training/6770',
              'training/6961', 'training/7012', 'training/7030', 'training/7310', 'training/7386', 'training/7428',
              'training/7539', 'training/7568', 'training/7576', 'training/7587', 'training/7609', 'training/7614',
              'training/7710', 'training/7733', 'training/7970', 'training/8064', 'training/8069', 'training/8096',
              'training/81', 'training/8168', 'training/8591', 'training/8606', 'training/8607', 'training/8657',
              'training/8658', 'training/8710', 'training/8806', 'training/8829', 'training/9048', 'training/9055',
              'training/9142', 'training/9224', 'training/9479', 'training/9675', 'training/9730', 'training/9769',
              'training/9783', 'training/9841', 'training/9871', 'training/9940']

    with open('negative.dat', 'w') as f:
        for record in doc_id[:100]:
            f.write('%s\n' % record)

    with open('negative-test.dat', 'w') as f:
        for record in doc_id[101:131]:
            f.write('%s\n' % record)
    return


def create_vocabulary():
    documents = reuters.fileids()
    for document_id in documents:
        text = tokenize(reuters.raw(document_id))
        for word in text:
            word_set.add(word)

    with open('words', 'w') as f:
        for record in word_set:
            f.write('%s\n' % record)
    return

if __name__ == '__main__':
    main()
    sys.exit(0)