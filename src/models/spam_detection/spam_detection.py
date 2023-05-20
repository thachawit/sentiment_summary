import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import ClassifierMixin


class SpamDetector(ClassifierMixin):
    def __init__(self) -> None:
        self.clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                  alpha=1e-3, random_state=42,
                                  max_iter=5))
        ])

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)

    # TODO: make this work
    # def create_job(self):
    #    joblib.dump(txt_cl, "SpamClassificationModel")
    #    clf = joblib.load('SpamClassificationModel')
    #
    #    clf.predict(
    #        ["sup, gift steam 50$ balance for you, just claim it hhttps://steanmcomnmunity.com/takes/75651898414512"])


# # why encode latin? ans ใช้ utf-8 ไม่เวิคเลย ใช้ latin
# df = pd.read_csv("spam.csv", encoding='latin')

# df_1 = df.dropna(axis='columns')
# # df_1["v1"] = df_1["v1"].replace(['ham','spam'],[0,1])
# df_1.head()

# df_1.isnull().sum()

# num = int(df_1.shape[0]*0.8)
# X_train = df_1["v2"][:num]
# y_train = df_1["v1"][:num]
# X_test = df_1["v2"][num:]
# y_test = df_1["v1"][num:]


# # Training model


# # Parameter tuning
# parameters = {
#     'vect__ngram_range': [(1, 1), (1, 3)],
#     'tfidf__use_idf': (True, False),
#     'clf__alpha': (1e-2, 1e-3),
# }

# gs_clf = GridSearchCV(txt_cl, parameters, cv=5, n_jobs=-1)
# gs_clf = gs_clf.fit(X_train, y_train)

# gs_clf.best_score_

# for param_name in sorted(parameters.keys()):
#     print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))

# predicted = gs_clf.predict(X_test)

# np.mean(predicted == y_test)
# predicted


# # Evaluate the model

# cm = metrics.confusion_matrix(y_test, predicted)
# sns.heatmap(cm, annot=True)

# # New model
# new_tweets = ['I saw their new baby for the first time.',
#               "Congratulations! You've won a $1,000 Walmart gift card. Go to http://bit.ly/12345678 tp claim now."]
# new_predicted = txt_cl.predict(new_tweets)

# new_predicted

# # Save the model
