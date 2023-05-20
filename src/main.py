# from pydantic import BaseModel
# from utils import fetch_post
import joblib
import pandas as pd
# import json
from sentiment_analyzer import sentiment_analyzer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


spam = joblib.load(
    './models/spam_detection/SpamClassificationModel')

df = pd.read_csv(
    './data/spam_test.csv')


@app.get("/")
async def main():
    return {"message": "This is main real app naja"}


@app.get("/test_fetch_post/", status_code=200)
# def fetch_post_ss(company_name: str, start_date: str, end_date: str):
def fetch_post_ss():
    count_pos = 0
    count_neg = 0
    count_neu = 0

    response = []

    respose_template = {
        'date': '',
        'sentiment': '',
        'positive': '',
        'negative': '',
        'neutral': '',
    }
    is_ham = False
    date = ''
    for i in df.iterrows():
        # summary the result after encouter the new tweet
        if isinstance(i[1].Tweet, str):
            # not the 1st row and prev replies not spam
            if i[0] != 0 and is_ham:
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

                count = count_pos+count_neg+count_neu

                percent_pos = round(count_pos*100/count, 3)
                percent_neg = round(count_neg*100/count, 3)
                percent_neu = round(count_neu*100/count, 3)

                response_list = respose_template.copy()
                response_list['date'] = date
                response_list['sentiment'] = sentiment
                response_list['positive'] = str(percent_pos)+'%'
                response_list['negative'] = str(percent_neg)+'%'
                response_list['neutral'] = str(percent_neu)+'%'

                response.append(response_list)

                count = 0
                count_pos = 0
                count_neg = 0
                count_neu = 0
            elif i[0] == 0:
                date = i[1].Date[:10]

            if spam.predict([i[1].Tweet]) == 'ham':
                is_ham = True
                date = i[1].Date[:10]
            else:
                is_ham = False

        if is_ham == True and isinstance(i[1].Reply, str):
            result = sentiment_analyzer(i[1].Reply)[0]
            if result == 'positive':
                count_pos += 1
            elif result == 'negative':
                count_neg += 1
            elif result == 'neutral':
                count_neu += 1
        # else:
        #     continue

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

    count = count_pos+count_neg+count_neu

    percent_pos = round(count_pos*100/count, 3)
    percent_neg = round(count_neg*100/count, 3)
    percent_neu = round(count_neu*100/count, 3)

    response_list = respose_template
    response_list['date'] = date
    response_list['sentiment'] = sentiment
    response_list['positive'] = str(percent_pos)+'%'
    response_list['negative'] = str(percent_neg)+'%'
    response_list['neutral'] = str(percent_neu)+'%'

    response.append(response_list)
    # json_response = json.dumps(response)

    return response


# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}


# class Data(BaseModel):
#     data1: str
#     data2: int


# @app.post("/create-data/{id}")
# def create_data(id: int, data: Data):
#     if id == 0:
#         response = "id is zero"

#     return data.data1
