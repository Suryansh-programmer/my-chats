import time
import json
import requests
import random
import os
import zipfile
from aiogram.types.error_evhent import ErrorEvent
import asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from aiogram.enums.parse_mode import ParseMode
import math
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, html
from aiogram.filters.command import Command
from aiogram.client.telegram import TelegramAPIServer
import logging
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, callback_data

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.exceptions import TelegramBadRequest
import aiohttp
import multiprocessing
from aiogram import BaseMiddleware
from aiogram import F
from collections import defaultdict
# Configure logging
logging.basicConfig(level=logging.INFO)

API_TOKEN = '6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4'
dp = Dispatcher()

# Create private Bot API server endpoints wrapper
session = AiohttpSession(
    api=TelegramAPIServer.from_base('http://0.0.0.0:8081/bot'))

# Initialize Bot instance with default bot properties which will be passed to all API calls
bot = Bot(token=API_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.callback_query.middleware(CallbackAnswerMiddleware(cache_time=90))

cookie_account = '__Host-next-auth.csrf-token=5cdb8ae28b8113eadad12ee4758aaa8e1a3b40300a8ffaf03364af5fda16126b%7C66e153f7c083c39df9b337c23af284f0d0f25c45879485654ce7f9858bc2c0ad; _gcl_au=1.1.195046403.1717373706; _fbp=fb.1.1717373712366.1173002811; intercom-id-xc8vmlt4=29fb048b-2a1d-4168-ac9d-80acf0e6bc59; intercom-device-id-xc8vmlt4=fbf7e835-c9a2-4545-b5f1-55a2982ebf08; _ga=GA1.1.2003135614.1717373731; __Secure-next-auth.callback-url=https%3A%2F%2Fapp.leonardo.ai%2F; ab.storage.deviceId.05d8c73d-1a81-4910-9f94-836c0ba47b65=%7B%22g%22%3A%22bf799975-6b8c-095f-67d2-e566223bb05c%22%2C%22c%22%3A1717373709348%2C%22l%22%3A1717376317280%7D; ab.storage.userId.05d8c73d-1a81-4910-9f94-836c0ba47b65=%7B%22g%22%3A%22f8dc50aa-ed47-420e-9ea8-91d521829e64%22%2C%22c%22%3A1717373763663%2C%22l%22%3A1717376317288%7D; _hp2_ses_props.2928600800=%7B%22r%22%3A%22https%3A%2F%2Faccounts.google.com%2F%22%2C%22ts%22%3A1717376316137%2C%22d%22%3A%22app.leonardo.ai%22%2C%22h%22%3A%22%2Fimage-generation%22%7D; __stripe_mid=13a80172-53f9-4553-bcea-873e57c6a4f2a70024; __stripe_sid=cba6ad6c-221e-431a-9154-237aa629de86cf9381; _hp2_id.2928600800=%7B%22userId%22%3A%22540618445651889%22%2C%22pageviewId%22%3A%223470851786939605%22%2C%22sessionId%22%3A%223861280066142552%22%2C%22identity%22%3A%22f8dc50aa-ed47-420e-9ea8-91d521829e64%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; ab.storage.sessionId.05d8c73d-1a81-4910-9f94-836c0ba47b65=%7B%22g%22%3A%22c0233fcf-bf5a-9a34-447b-d67683a5eaf1%22%2C%22e%22%3A1717378256233%2C%22c%22%3A1717376317277%2C%22l%22%3A1717376456233%7D; intercom-session-xc8vmlt4=MnoxQVpJKy9aTWFuZERIb05FOGNVQkpmZVNOSkpZZ1J2VkN2Rlh1eGhLRkU0dUIxUmlCeFNndy9ZWlRnUjU1QS0tUWVBVk9RYldMVk5ONzFNUkRZV1lEZz09--b0fc33621dfa9123c27e303fcc9120e3310d7115; _ga_4J9ZXN1KG8=GS1.1.1717373731.1.1.1717376510.4.0.0; __Secure-next-auth.session-token.0=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..ue3Yp-ncR1Uc3Xm1.1HcLNrASnH5BjQB46lf6wlwIHCbK0-j49k2-KjrZJiccGDcyUQhd91noCYqFWLWRmk23qZJdkw9r9QQj-U_KHkbwCp_w-5XgCGVnMw-gcXm7xnH_sX4Nsb4FvfQU4sEWs4b5WKUZaFIAvLqeJ_HDC-AFvD9IXgOxq4_X5vc-MypKHurf6CzsUUv0smfRTEKWe_PWYXihFKXpYJgqcFgdDSZWEqHQC8LFCVczf55fFCfryy1qhpfy_lNZRVqjZmFtXnD4KXsgTRrGHypdgpMoO4D831kH6cMX5mbXUo_96vLpbUDcCBeCDVziDkHNLDxd_wEFFJnp9srb2AJBh75hf2X3FxY8_8GZYRhMPzyEBFcB26Qr1O6rc7QoROZVdrrC2-e35VcI7MjhVR-y4DSPz6EupvI4nNNoMC1lx2TOlJE31A4BRmgT_1Vz0pHvB7jXEpZOAXF38T-X1N_W2bqUbow5VKznAEVG-ZCHXubpi1e4nXiX-L_jG9Fm1WpuRzww3PsfREWPlMQflhvI7aNrI6he2ma6XiWYIbW53DrP6V7HsSDmee7bJ5HtfSJBLb4J3iz5zNNNizoyfV_m25khE0sCzynO4LRi6DVwQEGse052okhioPGoweGamepFEc5gn_34NPCoxh2DIdXJ5VX9l8G8G54RNUgOsJ2fB0zrsHshJ8uvvLioW_0pfMS3dAW5Nnac79GYum546mf5WsvedtahzM06MW4PzoKqngKiM0IuZlseKKtRNiCdmosLPW856NAKF3SmpZ0ZavkRKEXQdFcmPNogRKIH6Nfvjv8HugOQUSlU8h8-lZ7nyzutT2WvrIhQFRFNqw9nZo1DgCGAAZZQQYwWYWcF95OJMaHP7dzSVu72ka9Te3-mgncWZN80NuC8R5uoadZci6b4nLwSICEpV48idA5dXujiv72MuNAE0F4hh365L2Ivk4lxUMkLld1S5j2bi0QYPQv2BnffVZrLaJuhx8aXo2wiIqg_6vNPs_ABVWbl31uyOFRSmhLFqaQ1TjVkfkbWK4VyIvoO0gImjxrZBTGd8DxK9JOSVLDst6_ivHr69vaJpSjNp4cr_6CKlWmf-B98SeZg6agPmDMV2Unnrf1s_fR1mwR7BDzuN5fvNzekf-_8qoi8DGrq_CVTnMwvyp5wGi6KLvW_5l1XvbbMa6oX4h0EPbD_fky6u5DfyCtG1b-DvC-9F_fHkEBu28rb1mHLyLOBhevVGKnWoQ3rENRr3QkKvGBTDmmGLaAqjxvnMQ56Rt0lAd3_dz0grAXcKF6LqFVbqQaMHjduPy7LDPs9o5zzuuJt4DjFBIBdsDbsnCRe4TN7gLWkLBmQw_72UgbX_QSKkYM7xSwfPmvisprbPoMZUDzZQiwjuxcvzhHUr52bj1HezfB4XclllVCgQIKhbzuoax31YSnwKoy9G1ZP8m7ZtLCTAEB7nyoGROXaowcB6SerytMEpmDzn35hrIYuaWspF3pOygep4pzpuS6jW66f49bN2ong7MjjNkMpr4RPNrgzKxtrCc_Dan1uHCV5V2zOYMkyllkJbfv050mKtHEsclNWmSOytbHt8aKmcbAlzFOLAeXaIx529ab7Rd7HnQ4QrGjCZgVy59HX1P81B-yTkqWqmo1s2K7xNbjM9Q-KR0eq5ZOr06vEnPK8hR2virQ0eNCE7MLVoKgpL72TvkL6AcNH7_GEBGnhuNBDF1FE3wwh9QXaZ5MfZgG9rFUyieSePnZZ90U6EeCDVy7Zjn_HUhMFPk7IboxeHCmlqz4jzJV2Ca_h84GXEHpplCt8i7XT_1NEHCOhHqTzyOKlLdqLaU15Vdee-9MgqenPbv35G54OsLjawRZnIqxn6YRrUn_dVIdxoZHnvhXf9EsMD8CPqopNc1lEAzQC2gubmRtB4-DzfeMr4QdKGT1CoiU2AZ9SFmYuPYlXBXO8pq_AZZRRLhX5XzHxX6_DFFkgP1Mss-mZt8gkzgJQQF79DqwEgFI_gIboyCbA0jbxTWGBgFlQLnKyPiCJrLCEbpLBKIxlWYdRNrPPilBb6gUqRqAyBQ7oQ7_rqAyQS9Ux_hdEytDxf4RojdLIG6JP0zrvzRNQAIIQSHNoQ1ALuVIrDmffkgWs3U-HZ_7gZko32P5F9iMzOWhswmHhOKEVpRlnDjns6bOK1TK9DujrIQTLFW3tvXWVt-wk9OYRa53FMC2HXg1OjzrAWFIbWXphL_hml4-9_qmApFTrmTOjW-grQ2bBjXnuQ4AfYuCeBALWr6Rk-_veLhSBSrjGR2FE_peIuUmhuckAxx8srIttbgqW2O25KGOtmZ5l57iHFw4q-2rRhBHTxcuUWnM_y3xZfoQ55hUJdnFWoNHOwL1Cd4ODihEc-ghZLbXnzhcyaOdXV3woMJBvS3zAGcIoZe6gLs7_L9a308o7bzPy3CYXKz14gKl1SncJqMRsNWHwxUgk4genUFuWKim8v3llvhjO5tuvVyxAkHc0STYvsnd_zelop5UQvMavtA_U5pzuUSzjn3s9q_yZTnMfBx5v0nxntbFTui7MYaKjPCx3aAN5-JlB9aVVSAkoDD3z3WorSrGfDzQm7fnjDfFG5pFBYyMHayqsFn5RM7cIEOJg3thRTJ_QORq0HVHt_pNSc2gkD97AIX9dxqzrj61Y3LcCMm_NUdXunI_sX12hzBEjINKi5rW0GTOKukGr5DNAjsgWyynPaxvHVPBBsjhBbcg1Y8KVDjlBW_O39D_9kE5ZEpmW90GdDc9NxEE0FTod3ac6wyHwRm5OhXl8ucqmj3VClseiFg9TDsja4vEW2hGBISgbGE9GRA_TZumEGQk5LtkBBmkRMlLY-snHiyduzRaZlC5tKJVdJwJw49bEdwO7zZWV9KHYkR4WdOPR_vWEJWvbrMLBbOYjTAuWYPvWauDAiJhi5pIOTqNjaZbzaGRMtXFSlW8FgavgelUuU1RHSpXVleihgWKoIG_HS-F_T05hySuhgzT08LJkV625jYrF9YumnIQbx_rVKxqnU9ebxqS7GfYUv_3N0r817DbpRj2PX0d85bmydFKseDhOj3E395DR5x2MS0r8lsYn5dsB-EcwvTVfN2Odbd5p-E4VMIY0kbBlzOV9A5w57jriqTUAP8eTqs4y_JI4svftzGOBqeolo6HVlZ0ZJDBhW2bKSBoc6Y2n1MTqNpGb-v9wrrxpphB_ILq8YmEWPGBOsucXdcgWn2xTyyV4SxumvYbVuhioSFp3_fZwuQ0OJJqpB-3moX7TvXCVuJdFdQ7GG_5jM4UrJt6qjM4fvMFF8jIs0oZsSJr-EyaHqtgJaK_S3HrrgqhDRurQrP_EAK0VkZlryY-DKjfV--OAVFmOq3f9Gsl_w9-9ZFwgLiaGVTUvoiqyBeVE03Z9cSf88lVhYHMkOWxzvY15XvlPd5FWWpXNHh8IvsQ_pgu_ohtjTiBn9ReLiFz8wgS1aWFv8UgVKa8LY2h_wd03VNxUvpMXPpRjebpAWyf0ZuhD-9txjXfY5_qHguwqJdbsd9YqirdAmNFVbXaeALuo-X8I9nu84e5QFozMyJgwFfhQ5cbUkiHNUn4r6jhR3QLcAfwhndGD9h8xXSBDt5fNYD1X76-d2hdxvoqlzwM9qzg4X4G0-l5vFxFYMcLaYyACvFyrj5JxJunhnPfk4XAKK2WWKDDUBvyiGycQ-GD_AJgdw4uIyGO-b8bNm1Rpt1LQI9QJbOiaPYIhyL67XZXgskMu-SrpdG_TQbRAOxuN03nrO-jgPhaYN87VAr9iABdcGZ_W5Z9nco4DJJYZoa37zoYkx9ce2CNzgDaVlQ0aU0S8JsbBfWqQdsoIp8-2AZgv0PdKkFHXEt_zyjJwODWS1BHnUaF; __Secure-next-auth.session-token.1=D2rDhHCFCy3BsUgtc8oWm5wyoKstOY98bHNLvcI0OoNnQZFtyXBkLsgW4hIqyF4N5dzkCpbbM7bwU42gsBP0QXwLZScX52z8pHvjfzVN6HNTo-oXOf1Gb_ZTy9bLXKovEucDoYdc0ifTDKXIbl5bZPrOZpW1x9XW4t3sSbEVWE8UEujdd9i-t_8l2X09ibnsIgB2a-y_SSvxmYbiV88lZy4DovXRJoudk9pvDZY_WbQzPWshCormL5xGwc1AvBSZ4y8QR15yiKf370pW7B9O41m3ZzP2bwR88H5GI59wBZUSxNVFiSakQ6eSlch3WYKJYCAZCJeDjtkohKzJSwsoLW1Hw6zAfuGx_XpuW6ehOZ3Fpghy7AIducbyYcAjkqccuxwWgVBG0zZOohG8LIv1L38P2-GnGOr36oEulG7Q-c4KAxsMSf2MtqsXyWo1yBxbM-ypmfKaYMer-9tDyxF5U2nrJZbdAPiwuUf0e58bdmkUXE75og0eaXomLtJk-3E2BcW6CirUMQ2rtIKW0-jSHSzUZplmk-qcMoOCqTA2xJ6dc7Tg7hriMyL60CBjN8CUidlPWt2D-uqWIj4OYd61vQValq-OQVMyJxf1oerSRYREuxEQAXQzWu_O8B2ZxQJ8cqcBtYKnfXzyqGjjnhpSQJU826s6amrMQzo4Ve-gLeWPa0QXgLnNk2G5S3_xcmYcrZptsZsU5aGDqtttEYSLV_lj1jD0E9DMKO8KRk2WclzviefretVP1TchVpkEhgPoSiUfpRR6YJgTylwAQK0JJ2L9MzSrqR1mhGKassVUX0gkWMyHfQsQlL7YW8CPyKLQfeNdGNYdxj2mjo_nuhhkvRh-l9zFPM_vuo_34zUUElDhgDBUwoyonlz4pNLaJkLycP8xNHWRousilvlgBeDFWRRVD__ScfWd-PSA_PbfA0AnRfD8GFycB_FDe9lMWEF5BIpluwpu0xgmMUXumBG2jp5fyxuTV6KOQWEPMGvYnxpyV0_nc1raRps3SV5tLkiZvLpGbkWvIgMibcyx8IYj3dfFQcgW8PjW3JieRxwfntroqWBi8634wAO33W-3zZ9OPPzlcdMzCmQ-u_jhoEfPyIUL_DamykzvJSQ.td5-DvH1yqKKCDPtUXnaDw'

ua = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'
]
admin = "6083636150"

uri = "mongodb+srv://suryanshmalhotra57:feRt0l4tVNyQ987e@cluster0.u6ky6ak.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
database = client['Leonardo-image-generation-bot']


def generate_user(header, sub):
    url = "https://api.leonardo.ai/v1/graphql"
    payload = json.dumps({
        "operationName":
        "GetUserDetails",
        "variables": {
            "userSub": sub
        },
        "query":
        "query GetUserDetails($userSub: String) {\n  users(where: {user_details: {cognitoId: {_eq: $userSub}}}) {\n    id\n    username\n    blocked\n    createdAt\n    user_details {\n      apiConcurrencySlots\n      apiCredit\n      apiPaidTokens\n      apiPlan\n      apiPlanAutoTopUpTriggerBalance\n      apiPlanSubscribeDate\n      apiPlanSubscribeFrequency\n      apiPlanSubscriptionSource\n      apiPlanTokenRenewalDate\n      apiPlanTopUpAmount\n      apiSubscriptionTokens\n      auth0Email\n      interests\n      interestsRoles\n      interestsRolesOther\n      isChangelogVisible\n      lastSeenChangelogId\n      paddleId\n      paidTokens\n      plan\n      planSubscribeFrequency\n      showNsfw\n      subscriptionGptTokens\n      subscriptionModelTokens\n      subscriptionSource\n      subscriptionTokens\n      tokenRenewalDate\n      __typename\n    }\n    team_memberships {\n      team {\n        akUUID\n        id\n        modifiedAt\n        paidTokens\n        paymentPlatformId\n        plan\n        planCustomTokenRenewalAmount\n        planSeats\n        planSubscribeDate\n        planSubscribeFrequency\n        planSubscriptionSource\n        planTokenRenewalDate\n        subscriptionTokens\n        teamLogoUrl\n        teamName\n        createdAt\n        creatorUserId\n        __typename\n      }\n      role\n      __typename\n    }\n    __typename\n  }\n}"
    })

    response = requests.post(url, headers=header, data=payload)
    print("Status code in getting user id:", response.status_code)
    data = response.json()
    user_id = data["data"]["users"][0]["id"]
    print(user_id)
    return user_id


user_last_message_time = {}


async def rate_limiter(message: types.Message):
    current_time = time.time()
    user_id = message.from_user.id
    if str(user_id) == admin:
        print("Admin")
        return True
    # If user_id is not in the dictionary, add it
    if user_id not in user_last_message_time:
        user_last_message_time[user_id] = current_time
        return True

    last_message_time = user_last_message_time[user_id]
    if current_time - last_message_time < 30:
        remaining_time = math.ceil(30 - (current_time - last_message_time))
        await message.reply(
            f"⚠️ **Alert!**\n\n In the Bot rate limit of 30 seconds is applied \n So, pls send message again after {remaining_time} seconds.",
            parse_mode=ParseMode.MARKDOWN)
        return False

    # Update the last message time
    user_last_message_time[user_id] = current_time
    return True


class CheggAccount:

    def switch(self):
        collection = database["accounts"]
        document = collection.find_one({"_id": 11})

        if document:
            if 'accounts' in document:
                cookiesList = document['accounts']

                global SUScookies
                SUScookies = cookiesList[0]
                global NXTcookies
                try:
                    NXTcookies = cookiesList[1]
                except:
                    NXTcookies = cookiesList[0]
                changeIndex = cookiesList.pop(0)
                cookiesList.append(SUScookies)
                collection.update_one({"_id": 11},
                                      {"$set": {
                                          "accounts": cookiesList
                                      }})
            else:
                collection.update_one({"_id": 11}, {
                    "$set": {
                        "accounts": [
                            'account_4', 'account_5', 'account_2', 'account_1',
                            'account_6', 'account_7', 'account_3'
                        ]
                    }
                })
        else:
            collection.insert_one({
                "_id":
                11,
                "accounts": [
                    'account_4', 'account_5', 'account_2', 'account_1',
                    'account_6', 'account_7', 'account_3'
                ]
            })


Account = CheggAccount()


def get_cookies():
    collection = database["accounts"]
    document = collection.find_one({"_id": 11})

    if document:
        if 'accounts' in document:
            cookiesList = document['accounts']

            account = cookiesList[0]

            if 'cookies' in document:
                cookies = document['cookies']

                COOKIE = cookies.get(account)
            else:
                pass
            return COOKIE
    else:
        print("No account present in accounts")


async def delete_message_after_delay(message: types.Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")


async def check_tokens(callback_query: types.CallbackQuery, user_id: int,
                       quantity: int):
    database_main = client['main-user-detail']
    colllection_main = database_main[str(user_id)]
    find_detail = colllection_main.find_one({"_id": user_id})
    if find_detail:
        if find_detail["Subscription"] == "Premium":
            token_collection = database[str(user_id)]
            token_detail = token_collection.find_one(
                {"_id": int(f"{user_id}11")})
            if token_detail:
                tokens = token_detail["tokens"]
                if tokens >= quantity:
                    msg = await callback_query.message.edit_text(
                        "generating images ")
                    collection = database[str(user_id)]
                    user_detail_id = int(f"{user_id}13")
                    document = collection.find_one({"_id": user_detail_id})
                    if document:
                        # Document exists, append the prompt to the 'prompts' field
                        collection.update_one({"_id": user_detail_id},
                                              {"$set": {
                                                  "quantity": quantity
                                              }})
                    print("processing 1 ")

                    p = multiprocessing.Process(target=generate_images,
                                                args=(callback_query, tokens,
                                                      user_id))
                    p.start()
                else:
                    await callback_query.message.edit_text(
                        "You don't have enough tokens to generate image/images \n \n Remaining token : "
                        + str(tokens))
            else:
                print("Else")
                insert_token_detail = token_collection.insert_one({
                    "_id":
                    int(f"{user_id}11"),
                    "tokens":
                    100
                })
                check_tokens(callback_query, user_id, quantity)
        else:
            print(find_detail)
            await callback_query.message.edit_text(
                "You don't have access to generate images ")

    else:
        find_detail = colllection_main.insert_one({
            "_id": user_id,
            "Subscription": "Free"
        })


@dp.callback_query(lambda c: c.data.isdigit())
async def button_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    print(user_id)

    await callback_query.answer()
    quantity = int(callback_query.data)
    print(quantity)

    # Proceed with image generation
    await callback_query.answer()
    await check_tokens(callback_query, user_id, quantity)


def generate_image_switch(callback_query: types.CallbackQuery, prompt,
                          quantity):
    global authorize, cookie_account, access_token
    switch_account()
    url = "https://api.leonardo.ai/v1/graphql"
    headers = {
        'cookie': cookie_account,
    }

    response = requests.get('https://app.leonardo.ai/api/auth/session',
                            headers=headers)
    print("Status code in getting access token", response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)
        access_token = data["accessToken"]
        sub = data["user"]["sub"]

    authorize = "Bearer " + access_token

    user_agent = random.choice(ua)

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "hi,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": authorize,
        "content-type": "app/json",
        "origin": "https://app.leonardo.ai",
        "referer": "https://app.leonardo.ai/",
        "sec-ch-ua":
        '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": user_agent
    }
    payload = json.dumps({
        "operationName":
        "CreateSDGenerationJob",
        "variables": {
            "arg1": {
                "prompt": prompt,
                "negative_prompt": "",
                "nsfw": True,
                "num_images": quantity,
                "width": 1024,
                "height": 1024,
                "image_size": 7,
                "num_inference_steps": 10,
                "contrast": 3.5,
                "guidance_scale": 7,
                "sd_version": "SDXL_0_9",
                "modelId": "2067ae52-33fd-4a82-bb92-c2c55e7d2786",
                "presetStyle": "LEONARDO",
                "scheduler": "LEONARDO",
                "public": True,
                "tiling": False,
                "leonardoMagic": False,
                "poseToImage": False,
                "poseToImageType": "POSE",
                "weighting": 0.75,
                "highContrast": False,
                "elements": [],
                "controlnets": [],
                "photoReal": False,
                "transparency": "disabled",
                "styleUUID": "703d6fe5-7f1c-4a9e-8da0-5331f214d5cf",
                "collectionIds": []
            }
        },
        "query":
        "mutation CreateSDGenerationJob($arg1: SDGenerationInput!) {\n  sdGenerationJob(arg1: $arg1) {\n    generationId\n    __typename\n  }\n}"
    })
    response = requests.post(url=url, headers=headers, data=payload)
    print("Status code in start generating : ", response.status_code)
    data = response.json()
    print(response.text)
    url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"
    user_id = generate_user(headers, sub)

    try:
        if data["errors"][0][
                "message"] == "Free users are subject to stricter filtering. As such your prompt has been blocked as it may result in inappropriate content. You may modify your prompt and try again or upgrade to a paid account." or data[
                    "errors"][0][
                        "message"] == "Our filter indicates that your prompt may include inappropriate references to children or younger persons, and has been blocked." or data[
                            "errors"][0][
                                "message"] == "content moderation filter":
            payload = {
                'chat_id':
                chat_id,
                "text":
                "Our system detected that your prompt contain restricted word/content! \n Send something that not restricted \n If you send it repeteadly ,you will be blocked"
            }
            response = requests.post(url_send, json=payload)
            return None
        if data["errors"][0][
                "message"] == f"not enough tokens userId: {user_id}":
            print("function executed")
            user_id = generate_image_switch(callback_query, prompt, quantity)
            if user_id == None:
                return None
        if data["errors"][0][
                "message"] == f"Invalid prompt, maximum length of 1000 characters exceeded.":
            payload = {
                'chat_id': chat_id,
                "text": "Your prompt is too long send something shortner "
            }
            response = requests.post(url_send, json=payload)
            return None

    except Exception as e:
        print(e)
    return user_id


def generate_images(callback_query: types.CallbackQuery, tokens, user_id_tg):
    print("generation functon")
    global authorize, cookie_account, access_token
    url = "https://api.leonardo.ai/v1/graphql"
    headers = {
        'cookie': cookie_account,
    }
    chat_id = callback_query.message.chat.id
    response = requests.get('https://app.leonardo.ai/api/auth/session',
                            headers=headers)
    print("Status code in getting access token", response.status_code)
    if response.status_code == 200:
        data = response.json()
        access_token = data["accessToken"]
        sub = data["user"]["sub"]

    authorize = "Bearer " + access_token
    url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Leonardo-image-generation-bot']
    collection = database[str(user_id_tg)]
    document = collection.find_one({"_id": int(f"{user_id_tg}13")})
    print(document)
    prompt = document["prompt"]
    quantity = document["quantity"]
    msg_id = document["msg_id"]
    user_agent = random.choice(ua)

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "hi,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": authorize,
        "content-type": "app/json",
        "origin": "https://app.leonardo.ai",
        "referer": "https://app.leonardo.ai/",
        "sec-ch-ua":
        '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": user_agent
    }
    payload = json.dumps({
        "operationName":
        "CreateSDGenerationJob",
        "variables": {
            "arg1": {
                "prompt": prompt,
                "negative_prompt": "",
                "nsfw": True,
                "num_images": quantity,
                "width": 1024,
                "height": 1024,
                "image_size": 7,
                "num_inference_steps": 10,
                "contrast": 3.5,
                "guidance_scale": 7,
                "sd_version": "SDXL_0_9",
                "modelId": "2067ae52-33fd-4a82-bb92-c2c55e7d2786",
                "presetStyle": "LEONARDO",
                "scheduler": "LEONARDO",
                "public": True,
                "tiling": False,
                "leonardoMagic": False,
                "poseToImage": False,
                "poseToImageType": "POSE",
                "weighting": 0.75,
                "highContrast": False,
                "elements": [],
                "controlnets": [],
                "photoReal": False,
                "transparency": "disabled",
                "styleUUID": "703d6fe5-7f1c-4a9e-8da0-5331f214d5cf",
                "collectionIds": []
            }
        },
        "query":
        "mutation CreateSDGenerationJob($arg1: SDGenerationInput!) {\n  sdGenerationJob(arg1: $arg1) {\n    generationId\n    __typename\n  }\n}"
    })
    response = requests.post(url=url, headers=headers, data=payload)
    print("Status code in start generating : ", response.status_code)
    data = response.json()
    print(response.text)

    user_id = generate_user(headers, sub)

    try:
        if data["errors"][0][
                "message"] == "Free users are subject to stricter filtering. As such your prompt has been blocked as it may result in inappropriate content. You may modify your prompt and try again or upgrade to a paid account." or data[
                    "errors"][0][
                        "message"] == "Our filter indicates that your prompt may include inappropriate references to children or younger persons, and has been blocked." or data[
                            "errors"][0][
                                "message"] == "content moderation filter":
            payload = {
                'chat_id':
                chat_id,
                "text":
                "Our system detected that your prompt contain restricted word/content! \n Send something that not restricted \n If you send it repeteadly ,you will be blocked"
            }
            response = requests.post(url_send, json=payload)
            return None
        if data["errors"][0][
                "message"] == f"not enough tokens userId: {user_id}":
            print("function executed")
            user_id = generate_image_switch(callback_query, prompt, quantity)
            if user_id == None:
                return None
        if data["errors"][0][
                "message"] == f"Invalid prompt, maximum length of 1000 characters exceeded.":
            payload = {
                'chat_id': chat_id,
                "text": "Your prompt is too long send something shortner "
            }
            response = requests.post(url_send, json=payload)
            return None

    except Exception as e:
        print(e)

    global trycount
    trycount = 0

    image_genration = False
    while image_genration == False:
        global image_count
        image_count = 0
        headers = {
            'authority': 'api.leonardo.ai',
            'accept': '*/*',
            "accept-encoding": "gzip, deflate, br",
            'accept-language': 'hi,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            "authorization": authorize,
            'content-type': 'app/json',
            'origin': 'https://app.leonardo.ai',
            'referer': 'https://app.leonardo.ai/',
            'sec-ch-ua':
            '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
        }

        if trycount < 10:

            payload = json.dumps({
                "operationName":
                "GetAIGenerationFeed",
                "variables": {
                    "where": {
                        "userId": {
                            "_eq": user_id
                        },
                        "teamId": {
                            "_is_null": True
                        },
                        "canvasRequest": {
                            "_eq": False
                        },
                        "universalUpscaler": {
                            "_is_null": True
                        },
                        "isStoryboard": {
                            "_eq": False
                        }
                    },
                    "offset": 0,
                    "limit": 10
                },
                "query":
                "query GetAIGenerationFeed($where: generations_bool_exp = {}, $userId: uuid, $limit: Int, $offset: Int = 0) {\n  generations(\n    limit: $limit\n    offset: $offset\n    order_by: [{createdAt: desc}]\n    where: $where\n  ) {\n    alchemy\n    contrastRatio\n    highResolution\n    guidanceScale\n    inferenceSteps\n    modelId\n    scheduler\n    coreModel\n    sdVersion\n    prompt\n    negativePrompt\n    id\n    status\n    quantity\n    createdAt\n    imageHeight\n    imageWidth\n    presetStyle\n    styleUUID\n    public\n    seed\n    tiling\n    transparency\n    initStrength\n    imageToImage\n    highContrast\n    promptMagic\n    promptMagicVersion\n    promptMagicStrength\n    imagePromptStrength\n    expandedDomain\n    motion\n    photoReal\n    photoRealStrength\n    photoRealVersion\n    nsfw\n    user {\n      username\n      id\n      __typename\n    }\n    custom_model {\n      id\n      userId\n      name\n      modelHeight\n      modelWidth\n      __typename\n    }\n    init_image {\n      id\n      url\n      __typename\n    }\n    generated_images(order_by: [{url: desc}]) {\n      id\n      url\n      motionGIFURL\n      motionMP4URL\n      likeCount\n      nsfw\n      generated_image_variation_generics(order_by: [{createdAt: desc}]) {\n        url\n        status\n        createdAt\n        id\n        transformType\n        upscale_details {\n          alchemyRefinerCreative\n          alchemyRefinerStrength\n          creativityStrength\n          oneClicktype\n          isOneClick\n          id\n          variationId\n          upscaleMultiplier\n          width\n          height\n          optional_metadata(path: \"upscalerStyle\")\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    generation_elements {\n      id\n      lora {\n        akUUID\n        name\n        description\n        urlImage\n        baseModel\n        weightDefault\n        weightMin\n        weightMax\n        __typename\n      }\n      weightApplied\n      __typename\n    }\n    generation_controlnets(order_by: {controlnetOrder: asc}) {\n      id\n      weightApplied\n      imageGuidanceStrengthType\n      controlnet_definition {\n        akUUID\n        displayName\n        displayDescription\n        controlnetType\n        __typename\n      }\n      controlnet_preprocessor_matrix {\n        id\n        preprocessorName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
            })
            response = requests.post('https://api.leonardo.ai/v1/graphql',
                                     headers=headers,
                                     data=payload)
            print("Status code in AI generation feed : ", response.status_code)
            if response.status_code == 200:
                trycount += 1
                data = json.loads(response.text)

                for generation in data["data"]["generations"]:
                    if prompt == generation["prompt"]:
                        if generation["status"] == "COMPLETE":
                            try:
                                dele = callback_query.message.delete()
                            except Exception as e:
                                print(e)

                            image_genration = True
                            for image in (generation["generated_images"]):
                                try:

                                    image_count += 1
                                    if image_count <= quantity:
                                        url = image["url"]
                                        response = requests.get(url=url)
                                        print("imagesend ")
                                        # Send the image to the user
                                        url_send_photo = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendPhoto"
                                        payload = {
                                            "chat_id": chat_id,
                                            "photo": url
                                        }
                                        response = requests.post(
                                            url_send_photo, json=payload)
                                        print(response)
                                        print(image_count, quantity)
                                    else:
                                        break
                                except:
                                    print("Error")
                            images_generated = generation["generated_images"]
                            document = collection.find_one(
                                {"_id": int(f"{user_id_tg}12")})
                            data = {
                                "prompt": prompt,
                                "generated_images": images_generated
                            }
                            if document:
                                if 'data' in document:
                                    collection.update_one(
                                        {"_id": int(f"{user_id_tg}12")},
                                        {"$push": {
                                            "data": data
                                        }})

                                else:
                                    collection.update_one(
                                        {"_id": int(f"{user_id_tg}12")},
                                        {"$set": {
                                            "data": [data]
                                        }})
                                print("document updated")
                            else:
                                collection.insert_one({
                                    "_id":
                                    int(f"{user_id_tg}12"),
                                    "data": [data]
                                })
                            new_token = int(tokens) - int(quantity)
                            print(new_token)
                            collection = database[str(user_id_tg)]
                            u = collection.update_one(
                                {"_id": int(f"{user_id_tg}11")},
                                {'$set': {
                                    'tokens': new_token
                                }},
                                upsert=True)

                            image_genration = True
                            print("Succesfuly generated")
                        else:
                            time.sleep(4)

        else:
            break


@dp.error()
async def error_handler(event: ErrorEvent):
    # logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    try:
        if "query is too old" in str(event.exception):
            pass
        else:
            await bot.send_message(
                chat_id=admin,
                text=f"{str(event.exception)} in aiogram error handling")
    except Exception as e:
        await bot.send_message(chat_id=admin, text=str(e))
    # do something with error


@dp.message(Command('send_message'))
async def send_message(message: types.Message):
    try:
        user_id = message.from_user.id
        if str(user_id) != admin:
            await message.reply(
                "You are not authorized to send msg to every users.",
                reply=True)
            return

        args = message.text.split(' ',
                                  1)  # Extract arguments from message text
        print(args)
        if len(args) != 2:
            h_1p = await message.reply("Usage: /send_message [message]",
                                       reply=True)
            await delete_message_after_delay(h_1p, 280)
            return

        msg = args[1]
        builder = InlineKeyboardBuilder()
        builder.button(text="Both", callback_data=f"send_both {msg}")
        builder.button(text="Free", callback_data=f"send_free {msg}")
        await message.reply("Choose the audience msg to be sent ",
                            reply_markup=builder.as_markup())
    except:
        pass


@dp.callback_query(lambda c: c.data.startswith("send_"))
async def send_message(callback_query: types.CallbackQuery):
    _, msg = callback_query.data.split(' ', 1)
    print(_, msg)
    edit_text = await callback_query.message.edit_text("sending msg  ")
    send_count = 0
    if _ == "send_free":
        collection = database['details of bot']
        record = collection.find_one({"_id": 1})
        if record:
            if 'chat_ids' in record:
                users = record['chat_ids']
                print(users)
                for user_id in users:
                    database_main = client['main-user-detail']
                    colllection_main = database_main[str(user_id)]
                    find_detail = colllection_main.find_one({"_id": user_id})
                    if find_detail:
                        if find_detail["Subscription"] == "Premium":
                            pass
                        else:
                            url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"

                            payload = {'text': msg, 'chat_id': user}
                            response = requests.post(url_send, json=payload)

                            send_count += 1

                    else:

                        find_detail = colllection_main.insert_one({
                            "_id":
                            user_id,
                            "Subscription":
                            "Free"
                        })
    else:
        collection = database['details of bot']
        record = collection.find_one({"_id": 1})
        if record:
            if 'chat_ids' in record:
                users = record['chat_ids']
                print(users)
                for user in users:
                    url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"

                    payload = {'text': msg, 'chat_id': user}
                    response = requests.post(url_send, json=payload)
                    send_count += 1
    await callback_query.message.edit_text(
        f"Message sent to {send_count} users")


def split_file(file_path,
               chunk_size=2 * 1024 * 1024 * 980):  # 50MB chunks as an example
    file_parts = []
    with open(file_path, 'rb') as f:
        part_num = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_file_name = f'images_part{part_num}.zip'
            with open(part_file_name, 'wb') as part_file:
                part_file.write(chunk)
            file_parts.append(part_file_name)
            part_num += 1
    return file_parts


def long_running_func(user_id, chat_id, msg_id):
    print(user_id, chat_id)
    url_delete = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/deleteMessage"
    uri = "mongodb+srv://suryanshmalhotra57:feRt0l4tVNyQ987e@cluster0.u6ky6ak.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['Leonardo-image-generation-bot']

    if str(user_id) != admin:
        database_main = client['main-user-detail']
        colllection_main = database_main[str(user_id)]
        find_detail = colllection_main.find_one({"_id": int(user_id)})
        print(find_detail)
        if find_detail:
            if find_detail["Subscription"] == "Premium":
                collection = database[str(user_id)]
                document = collection.find_one({"_id": int(f"{user_id}12")})
                url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"
                print(msg_id)
                payload = {'message_id': msg_id, 'chat_id': chat_id}
                response = requests.post(url_delete, json=payload)
                print(response.text)
                if document:
                    if 'data' in document:
                        pass
                    else:
                        payload = {
                            "chat_id": chat_id,
                            "text":
                            "You have not generated any images till now "
                        }

                        response = requests.post(url=url_send, json=payload)
                        return None
                else:
                    payload = {
                        "chat_id": chat_id,
                        "text": "You have not generated any images till now "
                    }
                    response = requests.post(url=url_send, json=payload)
                    return None
                payload = {
                    'chat_id':
                    chat_id,
                    "text":
                    "We are loading all the images generated by you pls wait!"
                }
                response = requests.post(url=url_send, json=payload)
                data = response.json()
                msg_id = data['result']['message_id']
                print(msg_id)
                print(response.text)

                list = document["data"]
                for data in list:
                    prompt = data['prompt']
                    for index, image in enumerate(data["generated_images"]):
                        url = image["url"]
                        image_response = requests.get(url=url)
                        if image_response.status_code == 200:
                            prompt = prompt.replace('/', ' ')
                            image_path = f'images_user/{user_id}/{str(prompt)}_{index}.jpg'

                            try:
                                os.makedirs(f'images_user/{user_id}')
                            except FileExistsError as e:
                                pass
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image_response.content)

                all_images_loaded = True
                zip_filename = 'images_library.zip'

                #Command to convert directory to zip file
                with zipfile.ZipFile(zip_filename, "w",
                                     zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(f'images_user/{user_id}'):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Construct the relative path within the ZIP file
                            relative_path = os.path.relpath(
                                file_path, f'images_user/{user_id}')
                            # Add the parent folder in the ZIP path
                            zip_path = os.path.join('Images', relative_path)
                            # Write the file to the ZIP archive
                            zipf.write(file_path, zip_path)

                url = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendDocument"
                print("before sending")
                if os.path.getsize(zip_filename) > 2 * 1024 * 1024 * 1000:
                    file_parts = split_file(zip_filename)

                    for part_file in file_parts:
                        with open(part_file, 'rb') as f:
                            files = {'document': f}
                            data = {'chat_id': chat_id}
                            response = requests.post(url,
                                                     data=data,
                                                     files=files)
                            print(response.status_code)
                            print(response.text)

                        os.remove(part_file
                                  )  # Optionally delete the part after sending

                else:
                    with open(zip_filename, 'rb') as zip_file:
                        files = {'document': zip_file}
                        data = {'chat_id': chat_id}
                        response = requests.post(url, data=data, files=files)
                        print(response.status_code)
                        print(response.text)
                        data = response.json()
                    payload = {'message_id': msg_id, 'chat_id': chat_id}
                response = requests.post(url=url_delete, json=payload)

                # Clean up
                os.remove(zip_filename)

                for file in os.listdir(f'images_user/{user_id}'):
                    os.remove(os.path.join(f'images_user/{user_id}', file))

                return "Success"

            else:
                print(find_detail)
                url_send = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": "You have not access to these function "
                }
                response = requests.post(url=url_send, json=payload)
                print(response.status_code)

        else:
            find_detail = colllection_main.insert_one({
                "_id": user_id,
                "Subscription": "Free"
            })
        return None

    all_images_loaded = False
    user_agent = random.choice(ua)

    image_count = 0

    while not all_images_loaded:
        collection = database["accounts"]
        document = collection.find_one({"_id": 11})

        if document:
            if 'accounts' in document:
                lines = document['accounts']
            else:
                payload = {
                    "chat_id": chat_id,
                    "text":"NO account available in database "
                }

                response = requests.get(url_send,json=payload)
                break
            if 'cookies' in document:
                cookieDict = document['cookies']
            else:
                payload = {
                    "chat_id": chat_id,
                    "text":"NO cookies available in database "
                }

                response = requests.get(url_send,json=payload)
                break
        for account_user in lines:
            cookie_account = cookieDict[account_user]
            url = "https://api.leonardo.ai/v1/graphql"
            headers = {
                'cookie': cookie_account,
            }

            data = requests.get(url='https://app.leonardo.ai/api/auth/session',
                                headers=headers)
            data = data.json()
            # print("Status code in getting access token",
            #       response.status_code)

            access_token = data["accessToken"]
            sub = data["user"]["sub"]
            authorize = "Bearer " + access_token

            headers.update({
                'authority': 'api.leonardo.ai',
                'accept': '*/*',
                "accept-encoding": "gzip, deflate, br",
                'accept-language': 'hi,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                "authorization": authorize,
                'content-type': 'app/json',
                'origin': 'https://app.leonardo.ai',
                'referer': 'https://app.leonardo.ai/',
                'sec-ch-ua':
                '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': user_agent,
            })

            user_id = generate_user(headers, sub)

            payload = {
                "operationName":
                "GetAIGenerationFeed",
                "variables": {
                    "where": {
                        "userId": {
                            "_eq": user_id
                        },
                        "teamId": {
                            "_is_null": True
                        },
                        "canvasRequest": {
                            "_eq": False
                        },
                        "universalUpscaler": {
                            "_is_null": True
                        },
                        "isStoryboard": {
                            "_eq": False
                        }
                    },
                    "offset": 0,
                    "limit": 1500
                },
                "query":
                "query GetAIGenerationFeed($where: generations_bool_exp = {}, $userId: uuid, $limit: Int, $offset: Int = 0) {\n  generations(\n    limit: $limit\n    offset: $offset\n    order_by: [{createdAt: desc}]\n    where: $where\n  ) {\n    alchemy\n    contrastRatio\n    highResolution\n    guidanceScale\n    inferenceSteps\n    modelId\n    scheduler\n    coreModel\n    sdVersion\n    prompt\n    negativePrompt\n    id\n    status\n    quantity\n    createdAt\n    imageHeight\n    imageWidth\n    presetStyle\n    styleUUID\n    public\n    seed\n    tiling\n    transparency\n    initStrength\n    imageToImage\n    highContrast\n    promptMagic\n    promptMagicVersion\n    promptMagicStrength\n    imagePromptStrength\n    expandedDomain\n    motion\n    photoReal\n    photoRealStrength\n    photoRealVersion\n    nsfw\n    user {\n      username\n      id\n      __typename\n    }\n    custom_model {\n      id\n      userId\n      name\n      modelHeight\n      modelWidth\n      __typename\n    }\n    init_image {\n      id\n      url\n      __typename\n    }\n    generated_images(order_by: [{url: desc}]) {\n      id\n      url\n      motionGIFURL\n      motionMP4URL\n      likeCount\n      nsfw\n      generated_image_variation_generics(order_by: [{createdAt: desc}]) {\n        url\n        status\n        createdAt\n        id\n        transformType\n        upscale_details {\n          alchemyRefinerCreative\n          alchemyRefinerStrength\n          creativityStrength\n          oneClicktype\n          isOneClick\n          id\n          variationId\n          upscaleMultiplier\n          width\n          height\n          optional_metadata(path: \"upscalerStyle\")\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    generation_elements {\n      id\n      lora {\n        akUUID\n        name\n        description\n        urlImage\n        baseModel\n        weightDefault\n        weightMin\n        weightMax\n        __typename\n      }\n      weightApplied\n      __typename\n    }\n    generation_controlnets(order_by: {controlnetOrder: asc}) {\n      id\n      weightApplied\n      imageGuidanceStrengthType\n      controlnet_definition {\n        akUUID\n        displayName\n        displayDescription\n        controlnetType\n        __typename\n      }\n      controlnet_preprocessor_matrix {\n        id\n        preprocessorName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
            }
            resp = requests.post('https://api.leonardo.ai/v1/graphql',
                                 json=payload,
                                 headers=headers)
            data = resp.json()

            for generation in data["data"]["generations"]:
                if generation["status"] == "COMPLETE":
                    for image in (generation["generated_images"]):
                        url = image["url"]

                        image_response = requests.get(url=url)
                        if image_response.status_code == 200:
                            image_count += 1
                            image_path = f'images/image_{image_count}.jpg'
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image_response.content)
            print("One account  completed")

        all_images_loaded = True
        zip_filename = 'images_library.zip'

        #Command to convert directory to zip file
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('images'):
                for file in files:
                    zipf.write(os.path.join(root, file))

        # Send the ZIP file to the user
        url = "http://0.0.0.0:8081/bot6910871811:AAH8VG4lyB8zi0EOAyL2FFbtb6DvB2ZzKw4/sendDocument"
        print("before sending")
        if os.path.getsize(zip_filename) > 2 * 1024 * 1024 * 1000:
            file_parts = split_file(zip_filename)

            for part_file in file_parts:
                with open(part_file, 'rb') as f:
                    files = {'document': f}
                    data = {'chat_id': chat_id}
                    response = requests.post(url, data=data, files=files)
                    print(response.status_code)
                    print(response.text)

                os.remove(
                    part_file)  # Optionally delete the part after sending
        else:
            with open(zip_filename, 'rb') as zip_file:
                files = {'document': zip_file}
                data = {'chat_id': chat_id}
                response = requests.post(url, data=data, files=files)
                print(response.status_code)
                print(response.text)
        payload = {'message_id': msg_id, 'chat_id': chat_id}
        response = requests.post(url_delete, json=payload)
        # Clean up
        try:os.remove(zip_filename)
        except:pass

        try:
            for file in os.listdir('images'):

                os.remove(os.path.join('images', file))
        except:pass
        return "Success"


def start_long_running_task(user_id, chat_id, msg_id):
    run_s = f'python s.py {user_id} {chat_id} {msg_id}'
    # os.system(run_s)
    long_running_func(user_id, chat_id, msg_id)


@dp.message(Command('load_all_image'))
async def load_all_image(message: types.Message):
    if not await rate_limiter(message):
        return None
    user_id = message.from_user.id
    chat_id = message.chat.id
    if str(user_id) == admin:
        msg = await message.reply(
            "We are loading all the images available in our data-base.It will take too much time so , pls be patient"
        )
        msg_id = msg.message_id
    else:
        msg = await bot.send_message(chat_id, text="Loading...")
        msg_id = msg.message_id
    p = multiprocessing.Process(target=start_long_running_task,
                                args=(user_id, chat_id, msg_id))
    p.start()


def switch_account():
    Account.switch()
    global cookie_account
    cookie_account = get_cookies()


@dp.message(Command('premium'))
async def premium_adder(message: types.Message):
    user_id = message.from_user.id
    msg_id = message.message_id
    print(user_id, admin)
    if str(user_id) != admin:
        await message.reply("You are not authorized to make a user premium .",
                            reply=True)
        return

    args = message.text.split()  # Extract arguments from message text
    print(args)
    if len(args) != 2:
        h_1p = await message.reply("Usage: /premium [user_id/username]",
                                   reply=True)
        await delete_message_after_delay(h_1p, 100)
        return

    user_id = args[1]
    print(user_id)
    try:
        if user_id.startswith('@'):
            collection = database['details of bot']
            # user_id =
            # Query to find the document with _id 1
            query = {"_id": 1}
            projection = {"all_users": {"$elemMatch": {"username": user_id}}}

            # Find the document with the specific username
            record = collection.find_one(query, projection)

            if record and 'all_users' in record and record['all_users']:
                user_id = int(record['all_users'][0]['user_id'])
            else:
                await message.reply("User not found in the database.",
                                    reply=True)
                return None

        print(user_id)
        user_id = int(user_id)
        database_main = client['main-user-detail']
        colllection_main = database_main[str(user_id)]
        find_detail = colllection_main.find_one({"_id": user_id})
        print(find_detail)
        if find_detail:
            print("Entered if ")
            if find_detail["Subscription"] == "Premium":
                print("entered if if ")
                await message.reply(
                    "The user already has the premium subscription ")
                print("message sent ")
            else:
                print("Entered if else ")
                premium_set = {"$set": {"Subscription": "Premium"}}
                query = {"_id": user_id}
                colllection_main.update_one(query, premium_set)
                await message.reply(
                    "The user has been added to the premium subscription")
                await bot.send_message(
                    chat_id=user_id, text="The admin gifted premium to you !")

        else:
            print("Entered else")
            find_detail = colllection_main.insert_one({
                "_id": user_id,
                "Subscription": "Premium"
            })
    except Exception as e:
        print(e)
        await message.reply("Error adding premium subscription")
        return


@dp.message(CommandStart())
async def start(message: types.Message):

    user_id = message.from_user.id
    first_name = message.from_user.full_name
    chat_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "None"
    reply_message = f"👋 Welcome {first_name} to our Leonardo image generation bot💚 "
    builder = InlineKeyboardBuilder()
    builder.button(text='Contact Here 💚', url='t.me/mkb_769')

    sp = await message.reply(reply_message, reply_markup=builder.as_markup())

    # Start a thread to delete the message after a delay

    database_main = client['main-user-detail']
    colllection_main = database_main[str(user_id)]
    find_detail = colllection_main.find_one({"_id": user_id})
    if find_detail:
        pass
    else:

        find_detail = colllection_main.insert_one({
            "_id": user_id,
            "Subscription": "Free"
        })
    collection = database['details of bot']
    record = collection.find_one({"_id": 1})
    username = '@' + username
    data = {"username": username, "user_id": user_id}
    query = {"_id": 1}

    if record:
        if 'count' in record:
            # Use the $inc operator to increment the 'count' field by 1
            update = {'$inc': {'count': 1}}
        else:
            # Initialize the 'count' field to 1 if it doesn't exist
            update = {'$set': {'count': 1}}
        chat = True
        if 'chat_ids' in record:
            if any(user == chat_id for user in record['chat_ids']):
                print("Chat_id is already present ")
                chat = False
            update2 = {'$push': {'chat_ids': chat_id}}

        else:
            update2 = {'$set': {'chat_ids': [chat_id]}}
        if 'all_users' in record:

            if any(user['username'] == username
                   for user in record['all_users']):
                pass
            else:
                # Add the new user to the all_users array
                value = {"$push": {"all_users": data}}
                if chat: collection.update_one(query, update2)
                collection.update_one(query, value)
                collection.update_one(query, update)

        else:

            value = {"$set": {"all_users": [data]}}
            collection.update_one(query, value)
            collection.update_one(query, update)
            if chat: collection.update_one(query, update2)

    else:
        collection.insert_one({
            "_id": 1,
            "all_users": [data],
            "count": 1,
            "chat_ids": [chat_id]
        })

    await delete_message_after_delay(sp, 28)


def reset_token():

    collections = database.list_collection_names()
    query = {"tokens": {"$exists": True}}
    new_values = {"$set": {"tokens": 100}}
    for collection_name in collections:
        collection = database[collection_name]
        result = collection.update_many(query, new_values)
        print(
            f"Updated {result.modified_count} in collection : {collection_name}"
        )
    print("Token reseted ")


async def on_startup():
    # Create scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_token, 'interval', hours=24)
    scheduler.start()


@dp.message(Command('token'))
async def token(message: types.Message):
    if not await rate_limiter(message):
        return None
    try:
        user_id = message.from_user.id
    except:
        user_id = message.callback_query.message.from_user.id
    print(user_id)

    database_main = client['main-user-detail']
    colllection_main = database_main[str(user_id)]
    find_detail = colllection_main.find_one({"_id": user_id})
    if find_detail:
        if find_detail["Subscription"] == "Premium":
            token_collection = database[str(user_id)]
            user_token_id = f"{user_id}11"
            token_detail = token_collection.find_one(
                {"_id": int(user_token_id)})
            if token_detail:
                tokens = token_detail["tokens"]

                reply = await message.reply(f"You have {tokens} tokens left")

            else:
                print("Else")
                user_token_id = f"{user_id}11"
                insert_token_detail = token_collection.insert_one({
                    "_id":
                    int(user_token_id),
                    "tokens":
                    100
                })
                await token(message)
        else:
            print(find_detail)
            return message.reply("You are not authorized to do this ")

    else:
        find_detail = colllection_main.insert_one({
            "_id": user_id,
            "Subscription": "Free"
        })
        return "hii"


@dp.message(~F.text.startswith('/'))
async def generate_image(message: types.Message):
    if not await rate_limiter(message):
        return None
    try:
        prompt = message.text
        msg_id = message.chat.id
        user_id = message.from_user.id
        collection = database[str(user_id)]
        user_detail_id = int(f"{user_id}13")

        database_main = client['main-user-detail']
        colllection_main = database_main[str(user_id)]
        find_detail = colllection_main.find_one({"_id": user_id})
        if find_detail:
            if find_detail["Subscription"] == "Premium":

                # Check if the document with the given ID exists
                document = collection.find_one({"_id": user_detail_id})

                if document:
                    # Document exists, append the prompt to the 'prompts' field
                    collection.update_one(
                        {"_id": user_detail_id},
                        {"$set": {
                            "prompt": prompt,
                            "msg_id": msg_id
                        }})
                    print(
                        f"Appended prompt to existing document with ID {user_detail_id}"
                    )

                else:
                    # Document does not exist, create it with the 'prompts' field
                    new_document = {
                        "_id": user_detail_id,
                        "prompt": prompt,
                        "msg_id": msg_id
                    }
                    collection.insert_one(new_document)
                    print(f"Created new document with ID {user_detail_id}")

                builder = InlineKeyboardBuilder()
                builder.button(text="1", callback_data="1")
                builder.button(text="2", callback_data="2")
                builder.button(text="3", callback_data="3")
                builder.button(text="4", callback_data="4")
                builder.adjust(1, 4)
                reply_message = await message.reply(
                    "How many images do you want to generate?",
                    reply_markup=builder.as_markup())

                # Delete the message after 2 minutes if no response
                try:
                    await delete_message_after_delay(reply_message, 360)
                except:
                    print("Error")

            else:
                await message.reply("You have not access to generate images ")
        else:
            find_detail = colllection_main.insert_one({
                "_id": user_id,
                "Subscription": "Free"
            })
    except TelegramBadRequest as e:
        print("Same error : {e}")
    except Exception as e:
        print(f" error occurs : {e}")


async def main():
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':

    print("Starting")
    print("polling")
    asyncio.run(main())

# $ cd telegram-bot-api
# $ telegram-bot-api --api-id=29482431 --api-hash=f6d3d53a435d6ac1ba2388508f7bdb38
