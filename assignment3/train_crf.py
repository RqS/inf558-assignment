import pycrfsuite
import spacy

nlp = spacy.load("en")

train_text = []
train_label = []
with open("train_text.txt", "r") as train_f:
    for line in train_f:
        train_text.append(nlp(line.strip().decode("utf-8")))
with open("train_label.txt", "r") as train_f:
    for line in train_f:
        train_label.append(line.strip().split())

test_text = []
test_label = []
with open("test_text.txt", "r") as train_f:
    for line in train_f:
        test_text.append(nlp(line.strip().decode("utf-8")))
with open("test_label.txt", "r") as train_f:
    for line in train_f:
        test_label.append(line.strip().split())

def create_feature(doc, i):
    token = doc[i]
    features = [
        'word.orth=' + token.orth_,
        'word.lemma=' + token.lemma_,
        'word.istitle=' + str(token.is_title),
        'word.isdigit=%s' % str(token).isdigit(),
        'word.likenum=%s' % token.like_num,
    ]
    if i > 0:
        token1 = doc[i-1]
        features.extend([
            '-1:word.orth=' + token1.orth_,
            '-1:word.lemma=' + token1.lemma_,
            '-1:word.istitle=' + str(token1.is_title),
            '-1:word.isdigit=%s' % str(token1).isdigit(),
            '-1:word.likenum=%s' % token1.like_num,
        ])
    if i > 1:
        token2 = doc[i-2]
        features.extend([
            '-2:word.orth=' + token2.orth_,
            '-2:word.lemma=' + token2.lemma_,
            '-2:word.istitle=' + str(token2.is_title),
            '-2:word.isdigit=%s' % str(token2).isdigit(),
            '-2:word.likenum=%s' % token2.like_num,
        ])
    if i > 2:
        token3 = doc[i-3]
        features.extend([
            '-3:word.orth=' + token3.orth_,
            '-3:word.lemma=' + token3.lemma_,
            '-3:word.istitle=' + str(token3.is_title),
            '-3:word.isdigit=%s' % str(token3).isdigit(),
            '-3:word.likenum=%s' % token3.like_num,
        ])

    if i < len(doc)-1:
        token1 = doc[i+1]
        features.extend([
            '+1:word.orth=' + token1.orth_,
            '+1:word.lemma=%s' % token1.lemma_,
            '+1:word.istitle=' + str(token1.is_title),
            '+1:word.isdigit=%s' % str(token1).isdigit(),
            '+1:word.likenum=%s' % token1.like_num,
        ])
    if i < len(doc)-2:
        token2 = doc[i+2]
        features.extend([
            '+2:word.orth=' + token2.orth_,
            '+2:word.lemma=%s' % token2.lemma_,
            '+2:word.istitle=' + str(token2.is_title),
            '+2:word.isdigit=%s' % str(token2).isdigit(),
            '+2:word.likenum=%s' % token2.like_num,
        ])
    if i < len(doc)-3:
        token3 = doc[i+3]
        features.extend([
            '+3:word.orth=' + token3.orth_,
            '+3:word.lemma=%s' % token3.lemma_,
            '+3:word.istitle=' + str(token3.is_title),
            '+3:word.isdigit=%s' % str(token3).isdigit(),
            '+3:word.likenum=%s' % token3.like_num,
        ])

    return features

X_train = [[create_feature(d, i) for i in range(len(d))] for d in train_text]
y_train = train_label

X_test = [[create_feature(d, i) for i in range(len(d))] for d in test_text]
y_test = test_label

trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(X_train, y_train):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,
    'c2': 1e-3,
    'max_iterations': 50,
    'feature.possible_transitions': True
})

trainer.train('assignment3')
tagger = pycrfsuite.Tagger()
tagger.open('assignment3')

predict = []
for test in X_test:
    predict.append(tagger.tag(test))

tp = 0
tn = 0
fp = 0
fn = 0
for i in range(len(y_test)):
    for j in range(len(y_test[i])):
        if y_test[i][j] == predict[i][j]:
            if y_test[i][j] != "irrelevant":
                tp += 1
            else:
                tn += 1
        else:
            if predict[i][j] != "irrelevant":
                fp += 1
            else:
                fn += 1

precision = float(tp)/(tp+fp)
recall = float(tp)/(tp+fn)
f = 2*precision*recall / (precision + recall)
print "precision: " + str(precision)
print "recall: " + str(recall)
print "f: " + str(f)