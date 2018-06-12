from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adreportrun import AdReportRun
import time
import facebook_business
import datetime
import json

api = facebook_business.api.FacebookAdsApi.init(access_token='xxx')
account_id = 'act_xxx'

account = AdAccount(account_id)

today = datetime.date.today()
startDate=str(today - datetime.timedelta(days=3))
endDate=str(today - datetime.timedelta(days=3))

fileName="facebook_api_"+startDate+".json"

row = 1

params = {
    'level': AdsInsights.Level.ad,
        'time_range': {
        'since': startDate,
        'until': endDate,
    },
    'fields': [
        AdsInsights.Field.ad_name,
        AdsInsights.Field.ad_id,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.spend,
        AdsInsights.Field.reach,
        AdsInsights.Field.unique_clicks,
        AdsInsights.Field.impressions,
        AdsInsights.Field.cpc,
        AdsInsights.Field.cpm,
        AdsInsights.Field.actions
    ],
    'breakdowns':['age','gender'],
    # 'export_format': 'json',
    'limit': 4000
}

async_job = account.get_insights(params=params,async=True)

async_job.remote_read()

data = []

while async_job[AdReportRun.Field.async_percent_completion] < 100:
    async_job.remote_read()
    time.sleep(1)

result = async_job.get_result()

with open(fileName, 'w') as outfile:
    for AdsInsights in result:
        json.dump(AdsInsights.export_all_data(), outfile)

# json_output = json.dumps(async_job.get_result())

# print(async_job.get_result())
# print(async_job.export_all_data())
# print(type(async_job.get_result()))
# print(data)
# with open(fileName, 'w') as outfile:
#     json.dump(async_job.get_result(), outfile)