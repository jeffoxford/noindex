from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import streamlit as st
import pandas as pd

st.title('NoIndexing')

urls=st.text_area(label='Enter Urls',placeholder='Enter URLs (1 per line)').strip()

urls=urls.split('\n')

uploaded_file=st.file_uploader(label='Upload Credential File',type='json')

button=st.button('Click Me')
empty=[]
deleted_url=[]
type=[]
notifyTime=[]
if uploaded_file is not None and button:
    filename=uploaded_file.name

    JSON_KEY_FILE = filename

    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    # Authorize credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    # for checking purpuse i add 2
    if len(urls) > 200:
        st.error('more than 200 urls are not allowed')
    else:
        for url in urls:
            try:
                if not url.endswith('.com/'):
                    content = {}
                    content['url'] = url
                    content['type'] = "URL_DELETED"
                    json_content = json.dumps(content)
                    response, content = http.request(ENDPOINT, method="POST", body=json_content)
                    result = json.loads(content.decode())
                    empty.append(result)
                    st.write(result)
                    st.success('Success')
                else:
                    st.error('Urls Should Not End With .com/')
            except Exception as e:
                st.error('UnsuccessFul')

for value in empty:
    try:
        deleted_url.append(value['urlNotificationMetadata']['latestRemove']['url'])
        type.append(value['urlNotificationMetadata']['latestRemove']['type'])
        notifyTime.append(value['urlNotificationMetadata']['latestRemove']['notifyTime'])
    except Exception as e:
        st.error('Error')

df=pd.DataFrame(data={'url':deleted_url,'type':type,'notifyTime':notifyTime})

@st.cache
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.download_button(
    label="Get Deleted URLS",
    data=csv,
    file_name='response.csv',
    mime='text/csv')


# urls = ['https://e-gunparts.com/homepage/','https://e-gunparts.com/homepage/','https://e-gunparts.com/category/rifle/']

# Build the request body
