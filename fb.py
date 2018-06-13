from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import  FacebookAdsApi
from facebook_business.adobjects.adreportrun import AdReportRun
import time
import datetime
import json

api = FacebookAdsApi.init(access_token='xxxxx')
account = AdAccount('xxxxx')
today = datetime.date.today()
startDate=str(today - datetime.timedelta(days=3))
endDate=str(today - datetime.timedelta(days=3))
fileName="facebook_api_"+startDate+".json"
data = []

params = {
    'level': AdsInsights.Level.ad,
        'time_range': {
        'since': startDate,
        'until': endDate,
    },
    'fields': [
        AdsInsights.Field.ad_id,
        AdsInsights.Field.ad_name,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.reach,
        AdsInsights.Field.spend,
        AdsInsights.Field.unique_clicks,
        AdsInsights.Field.clicks,
        AdsInsights.Field.impressions,
        AdsInsights.Field.cpc,
        AdsInsights.Field.cpm,
        AdsInsights.Field.actions
    ],
    'breakdowns':['age','gender'],
    'export_format': 'json',
    'limit': 1000
}

async_job = account.get_insights(params=params,async=True)
async_job.remote_read()

while async_job[AdReportRun.Field.async_percent_completion] < 100:
    async_job.remote_read()
    time.sleep(1)

result = async_job.get_result()

for AdsInsights in result:
    data.append(AdsInsights.export_all_data())

with open(fileName, 'w') as outfile:
    json.dump(data, outfile, sort_keys = True, ensure_ascii=True, indent=0, separators=(',',':'))
