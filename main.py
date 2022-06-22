from io import StringIO

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import streamlit as st
import pandas as pd
import tldextract

st.title('Bulk URL Removal Tool')

urls=st.text_area(label='Enter URLs (max 200)',placeholder='Enter URLs (1 per line)').strip()

urls=urls.split('\n')

uploaded_file=st.file_uploader(label='Upload Credential File',type='json')

button=st.button('Start Noindexing URLs')
empty=[]
deleted_url=[]
type=[]
notifyTime=[]
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
            try:
                result=tldextract.extract(url)
                suffix = result.suffix + '/'
                if not url.endswith(suffix):
                    content = {}
                    content['url'] = url
                    content['type'] = "URL_DELETED"
                    json_content = json.dumps(content)
                    response, content = http.request(ENDPOINT, method="POST", body=json_content)
                    result = json.loads(content.decode())
                    empty.append(result)
            except Exception as e:
                st.error('UnsuccessFul')
    st.success('Sucess')


for value in empty:
    try:
        deleted_url.append(value['urlNotificationMetadata']['latestRemove']['url'])
        type.append(value['urlNotificationMetadata']['latestRemove']['type'])
        notifyTime.append(value['urlNotificationMetadata']['latestRemove']['notifyTime'])
    except Exception as e:
        print('Error')

df=pd.DataFrame(data={'url':deleted_url,'type':type,'notifyTime':notifyTime})

@st.cache
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.download_button(
    label="Export API Responses",
    data=csv,
    file_name='response.csv',
    mime='text/csv')


# urls = ['https://e-gunparts.com/homepage/','https://e-gunparts.com/homepage/','https://e-gunparts.com/category/rifle/']

# Build the request body
