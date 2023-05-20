from sentiment_analyzer import sentiment_analyzer
import joblib
import pandas as pd
import glob
import pandas as pd

# Get a list of file paths matching the CSV file pattern
csv_files = glob.glob('./Jan_csv/*.csv')
spam = joblib.load(
    './models/spam_detection/SpamClassificationModel')

whole_jan_response = []

count_for_checking = 0

text = ""
count_pos = 0
count_neg = 0
count_neu = 0

response_template = {
    'date': '',
    'sentiment': '',
    'positive': '',
    'negative': '',
}


# Loop through each CSV file
for csv_file in csv_files:
    # Read CSV file
    df = pd.read_csv(csv_file, encoding='utf-8')

    for i in df.iterrows():
        # print(i[1].Date)
        if isinstance(i[1].Tweet, str):
            text = i[1].Tweet

        elif isinstance(i[1].Reply, str):
            text = i[1].Reply

        if spam.predict([text])[0] == "ham":
            sentiment = (sentiment_analyzer(text))[0]
            if sentiment == 'positive':
                count_pos += 1
            if sentiment == 'neutral':
                count_neu += 1
            if sentiment == 'negative':
                count_neg += 1

    if count_pos > count_neu:
        if count_pos > count_neg:
            sentiment = "positive"
        elif count_pos == count_neg:
            sentiment = "neutral"
        else:
            sentiment = "negative"
    else:
        if count_neu > count_neg:
            sentiment = "neutral"
        else:
            sentiment = "negative"

    print(count_pos, count_neu, count_neg, 'summary', sentiment)

    total_text_spam_excluded = count_pos+count_neu+count_neg

    percent_pos = round(count_pos*100/total_text_spam_excluded, 3)
    percent_neg = round(count_neg*100/total_text_spam_excluded, 3)
    percent_neu = round(count_neu*100/total_text_spam_excluded, 3)

    # print('percentage: ', percent_neu, percent_neg,
    #       percent_pos, percent_pos+percent_neu+percent_neg)

    # print('Total Data:', total_text_spam_excluded)

    response_each_day = response_template.copy()
    response_each_day['date'] = csv_file
    response_each_day['sentiment'] = sentiment
    response_each_day['positive'] = str(percent_pos)+'%'
    response_each_day['negative'] = str(percent_neg)+'%'
    response_each_day['neutral'] = str(percent_neu)+'%'

    whole_jan_response.append(response_each_day)
    print('1 file is DONE')

    count_for_checking += 1


print(count_for_checking)
print(whole_jan_response)

df = pd.DataFrame(whole_jan_response)
df.to_csv('./whole_jan_sentiment_summary/jan_sentiment.csv', )

# def get_sentiment_summary_and_each_percentage():
# text = ""
# count_pos = 0
# count_neg = 0
# count_neu = 0

# response_template = {
#     'date': '',
#     'sentiment': '',
#     'positive': '',
#     'negative': '',
#     'neutral': '',
# }

# date_list = []
# for i in df.iterrows():

# if isinstance(i[1].Tweet, str):
#     text = i[1].Tweet

# elif isinstance(i[1].Reply, str):
#     text = i[1].Reply

# if spam.predict([text])[0] == "ham":
#     sentiment = (sentiment_analyzer(text))[0]
#     if sentiment == 'positive':
#         count_pos += 1
#     if sentiment == 'neutral':
#         count_neu += 1
#     if sentiment == 'negative':
#         count_neg += 1

#     print(count_neu, count_neg, count_pos)

# total_text_spam_excluded = count_pos+count_neu+count_neg

# percent_pos = round(count_pos*100/total_text_spam_excluded, 3)
# percent_neg = round(count_neg*100/total_text_spam_excluded, 3)
# percent_neu = round(count_neu*100/total_text_spam_excluded, 3)

# print('percentage: ', percent_neu, percent_neg,
#     percent_pos, percent_pos+percent_neu+percent_neg)

# print('Total Data:', total_text_spam_excluded)

# response_template['date'] = 'date'
# response_template['sentiment'] = sentiment
# response_template['positive'] = str(percent_pos)+'%'
# response_template['negative'] = str(percent_neg)+'%'
# response_template['neutral'] = str(percent_neu)+'%'


# return df

# Save the DataFrame as a Feather file


# get_sentiment_summary_and_each_percentage()

# df.to_feather('path/to/save/file.feather')


# is_ham = False
# date = ''

# for i in df.iterrows():
#     # summary the result after encouter the new tweet
#     if isinstance(i[1].Tweet, str):
#         # not the 1st row and prev replies not spam
#         if i[0] != 0 and is_ham:
#             if count_pos > count_neu:
#                 if count_pos > count_neg:
#                     sentiment = "positive"
#                 elif count_pos == count_neg:
#                     sentiment = "neutral"
#                 else:
#                     sentiment = "negative"
#             else:
#                 if count_neu > count_neg:
#                     sentiment = "neutral"
#                 else:
#                     sentiment = "negative"

#             count = count_pos+count_neg+count_neu

#             percent_pos = round(count_pos*100/count, 3)
#             percent_neg = round(count_neg*100/count, 3)
#             percent_neu = round(count_neu*100/count, 3)

#             response_list = response_template.copy()
#             response_list['date'] = date
#             response_list['sentiment'] = sentiment
#             response_list['positive'] = str(percent_pos)+'%'
#             response_list['negative'] = str(percent_neg)+'%'
#             response_list['neutral'] = str(percent_neu)+'%'

#             response.append(response_list)

#             count = 0
#             count_pos = 0
#             count_neg = 0
#             count_neu = 0
#         elif i[0] == 0:
#             date = str(i[1].Date)

#         if spam.predict([i[1].Tweet]) == 'ham':
#             is_ham = True
#             date = str(i[1].Date)
#         else:
#             is_ham = False

#     if is_ham == True and isinstance(i[1].Reply, str):
#         result = sentiment_analyzer(i[1].Reply)[0]
#         if result == 'positive':
#             count_pos += 1
#         elif result == 'negative':
#             count_neg += 1
#         elif result == 'neutral':
#             count_neu += 1
#     # else:
#     #     continue

# if count_pos > count_neu:
#     if count_pos > count_neg:
#         sentiment = "positive"
#     elif count_pos == count_neg:
#         sentiment = "neutral"
#     else:
#         sentiment = "negative"
# else:
#     if count_neu > count_neg:
#         sentiment = "neutral"
#     else:
#         sentiment = "negative"

# count = count_pos+count_neg+count_neu

# percent_pos = round(count_pos*100/count, 3)
# percent_neg = round(count_neg*100/count, 3)
# percent_neu = round(count_neu*100/count, 3)

# response_list = response_template
# response_list['date'] = date
# response_list['sentiment'] = sentiment
# response_list['positive'] = str(percent_pos)+'%'
# response_list['negative'] = str(percent_neg)+'%'
# response_list['neutral'] = str(percent_neu)+'%'

# response.append(response_list)
# json_response = json.dumps(response)

# return response
