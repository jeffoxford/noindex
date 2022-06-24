from io import StringIO

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import streamlit as st
import pandas as pd
import tldextract

st.title('Bulk URL Removal Tool')

urls=st.text_area(label='Enter URLs (max 200)',placeholder='Enter URLs (1 per line)').strip('')


urls=urls.split('\n')


uploaded_file=st.file_uploader(label='Upload Credential File',type='json')

button=st.button('Start Noindexing URLs')



code=[]
empty=[]
deleted_url=[]
type=[]
notifyTime=[]
message=[]
status=[]
type_error=[]
reason=[]
domain=[]
quota_limit_value=[]
quota_limit=[]
service=[]
quota_metric=[]
consumer=[]
quota_location=[]
type_error2=[]
description=[]
url_error=[]



if uploaded_file is not None and button:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    JSON_KEY_FILE = json.loads(string_data)

    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    # Authorize credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    # for checking purpuse i add 2
    if len(urls) > 200:
        st.error('more than 200 urls are not allowed')
    else:
        for url in urls:
            deleted_url.append(url)
            try:
                # url=url+'/'
                result=tldextract.extract(url)
                suffix = result.suffix + '/'
                print(suffix)
                if not url.endswith(suffix):
                    content = {}
                    content['url'] = url
                    content['type'] = "URL_DELETED"
                    json_content = json.dumps(content)
                    response, content = http.request(ENDPOINT, method="POST", body=json_content)
                    result = json.loads(content.decode())
                    print(result)
                    empty.append(result)
            except Exception as e:
                print('??')

for value in empty:
    if 'urlNotificationMetadata' in value:
        type.append(value['urlNotificationMetadata']['latestRemove']['type'])
        notifyTime.append(value['urlNotificationMetadata']['latestRemove']['notifyTime'])
        code.append(None)
        message.append(None)
        status.append(None)
        type_error.append(None)
        reason.append(None)
        domain.append(None)
        quota_limit_value.append(None)
        quota_limit.append(None)
        service.append(None)
        quota_metric.append(None)
        consumer.append(None)
        quota_location.append(None)
        type_error2.append(None)
        description.append(None)
        url_error.append(None)
    # if 'error' in value:
    #     deleted_url.append(None)
    #     type.append(None)
    #     notifyTime.append(None)
    #     code.append(value['error']['code'])
    #     message.append(value['error']['message'])
    #     status.append(value['error']['status'])
    #     type_error.append(value['error']['details'][0]['@type'])
    #     reason.append(value['error']['details'][0]['reason'])
    #     domain.append(value['error']['details'][0]['domain'])
    #     quota_limit_value.append(value['error']['details'][0]['metadata']['quota_limit_value'])
    #     quota_limit.append(value['error']['details'][0]['metadata']['quota_limit'])
    #     service.append(value['error']['details'][0]['metadata']['service'])
    #     quota_metric.append(value['error']['details'][0]['metadata']['quota_metric'])
    #     consumer.append(value['error']['details'][0]['metadata']['consumer'])
    #     quota_location.append(value['error']['details'][0]['metadata']['quota_location'])
    #     type_error2.append(value['error']['details'][1]['@type'])
    #     description.append(value['error']['details'][1]['links'][0]['description'])
    #     url_error.append(value['error']['details'][1]['links'][0]['url'])

    if 'error' in value:
        if value['error']['code']==403:
            type.append(None)
            notifyTime.append(None)
            code.append(value['error']['code'])
            message.append(value['error']['message'])
            status.append(value['error']['status'])
            type_error.append(None)
            reason.append(None)
            domain.append(None)
            quota_limit_value.append(None)
            quota_limit.append(None)
            service.append(None)
            quota_metric.append(None)
            consumer.append(None)
            quota_location.append(None)
            type_error2.append(None)
            description.append(None)
            url_error.append(None)
        if value['error']['code']==400:
            type.append(None)
            notifyTime.append(None)
            code.append(value['error']['code'])
            message.append(value['error']['message'])
            status.append(value['error']['status'])
            type_error.append(None)
            reason.append(None)
            domain.append(None)
            quota_limit_value.append(None)
            quota_limit.append(None)
            service.append(None)
            quota_metric.append(None)
            consumer.append(None)
            quota_location.append(None)
            type_error2.append(None)
            description.append(None)
            url_error.append(None)
        if value['error']['code']==429:
            type.append(None)
            notifyTime.append(None)
            code.append(value['error']['code'])
            message.append(value['error']['message'])
            status.append(value['error']['status'])
            type_error.append(value['error']['details'][0]['@type'])
            reason.append(value['error']['details'][0]['reason'])
            domain.append(value['error']['details'][0]['domain'])
            quota_limit_value.append(value['error']['details'][0]['metadata']['quota_limit_value'])
            quota_limit.append(value['error']['details'][0]['metadata']['quota_limit'])
            service.append(value['error']['details'][0]['metadata']['service'])
            quota_metric.append(value['error']['details'][0]['metadata']['quota_metric'])
            consumer.append(value['error']['details'][0]['metadata']['consumer'])
            quota_location.append(value['error']['details'][0]['metadata']['quota_location'])
            type_error2.append(value['error']['details'][1]['@type'])
            description.append(value['error']['details'][1]['links'][0]['description'])
            url_error.append(value['error']['details'][1]['links'][0]['url'])

@st.cache
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')


try:
    df=pd.DataFrame(data={'url':deleted_url,'type':type,'notifyTime':notifyTime,'code':code,
                      'message':message,'status':status,'type_error':type_error,'reason':reason,'domain':domain,
                      'quota_limit_value':quota_limit_value,'quota_limit':quota_limit,'service':service,
                      'quota_metric':quota_metric,'consumer':consumer,'quota_location':quota_location,
                      'type_error2':type_error2,'description':description,'url_error':url_error})

    csv = convert_df(df)
    st.download_button(
        label="Export API Responses",
        data=csv,
        file_name='response.csv',
        mime='text/csv')
    if button:
        response_df=pd.DataFrame({'error_403':[len(df[df['code']==403])],'error_400':[len(df[df['code'] == 400])],
                              'error_429':[len(df[df['code'] == 429])],
                              'success_response':[len(df[df['type']=='URL_DELETED'])]})
        st.dataframe(response_df)
except:
    st.error('HomePage URLs Detected Remove And Refresh')

    # if len(df[df['code']==403])>0:
    #     st.error("Total Number of 403 Error Response "+ str(len(df[df['code']==403])))
    # if len(df[df['code'] == 400])>0:
    #     st.error("Total Number of 400 Error Response " + str(len(df[df['code'] == 400])))
    # if len(df[df['code'] == 429])>0:
    #     st.error("Total Number of 429 Error Response " + str(len(df[df['code'] == 429])))
    # if len(df[df['type']=='URL_DELETED'])>0:
    #     st.success("Total Number of Success Response "+ str(len(df[df['type']=='URL_DELETED'])))






# urls = ['https://e-gunparts.com/homepage/','https://e-gunparts.com/homepage/','https://e-gunparts.com/category/rifle/']

# Build the request body
