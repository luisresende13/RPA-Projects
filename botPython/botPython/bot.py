from time import sleep
import requests, json
from botcity.core import DesktopBot
from botcity.maestro import *   # Using the Maestro SDK

# WhatsApp credentials
# keys = json.loads(open('./credentials', 'r'))
keys = {
    "token": "EAAIyEfhhDxQBAE6LKa8dZB5QZBJ4iCbaQck1vJB7Aotwz9tMZBjannxW8fkkAveDJqxtpjboFKKh8FMZBKSxOirXB15kLccDHjRvE6iIEZCOnXMeZBTOIEtiR9VmZCiy7FglmruDaqQyBpNcZAGm8BxBeneD7eUXNYtEbLmVoqXjzctd0HKIQZCUnZAhxAjDk4t59iUS2Q52uHJZCm7JR8H8LL0P9CTgF7WZBOkZD",
    "number_id": "101349609340848"
}
token = keys['token']
number_id = keys['number_id']

# Contact & message options
translate_msg =  True
contact_list = {
    'Dayvisson Daniel': '5521981759814',
    'Luis Resende Silva': '5531984258358',
    'Hanna Soares Viana': '5521983445550',
}

# WhatsApp Cloud API BotCity Plugin Settings
# from botcity.plugins.whatsapp import BotWhatsappPlugin
# whatsapp = BotWhatsappPlugin(access_token=token, whatsapp_number_id=number_id) # instantiate plugin
# msg_template = "*{}*\n\n- {} ({})\n\nBio do autor: {}\n\nTags: {}"

# WhatsApp Cloud API Request Settings
WhatsAppCloudAPIUrl = 'https://graph.facebook.com/v13.0'
msg_url = WhatsAppCloudAPIUrl + f'/{number_id}/messages'; msg_url # messages endpoint
headers = {'Authorization': f'Bearer {token}'}
message_payload = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": None, # dinamic
  "type": "template",
  "template": {
     # "namespace": credentials['template_namespace'], # template namespace id
    "name": "citacao_famosa", # template name id
    "language": {
      "code": "pt_BR"
    },
    "components": [
      {
        "type": "body",
        "parameters": None # static
      }
    ]
  }
}

# Setting up quotable api request
api_url = r'https://api.quotable.io'

quote_params = {
    'minLenght': 1,
    'maxLenght': 5000,
    # 'tags': 'famous-quotes|wisdom|friendship|inspirational|success|life|business|motivational|history|politics|hapiness|humor|freedom|science|philosophy|truth|spirituality|self|faith',
}

def random_quote():
    response = requests.request("GET", api_url+'/random', params=quote_params)
    if response.status_code==200:
        return json.loads(response.text)
    else: return None

def search_author(slug):
    response = requests.request("GET", api_url+'/authors', params={'slug': slug, 'limit': 1, 'page': 1})
    if response.status_code==200:
        return json.loads(response.text)['results'][0]
    else: return None
    
# Extra: Translate api response
import translators as ts

def translate(query):
    if type(query)==str:
        return ts.google(query_text=query.replace('-', ' '), from_language='en', to_language='pt')
    elif type(query)==list:
        return list(map(translate, query))

def translate_object(obj, fields):
    obj_copy = obj.copy()
    for field in fields:
        obj_copy[field] = translate(obj_copy[field])
    return obj_copy

# Extra: Capitalize single string or list
def capitalize(query):
    if type(query)==str:
        return query.capitalize()
    elif type(query)==list:
        return list(map(capitalize, query))

# Extra: transform text list into text object list
as_text_obj = lambda text: {'type': 'text', 'text': text}

def as_text_object_list(text_list):
    return list(map(as_text_obj, text_list))

class Bot(DesktopBot):
    def action(self, execution=None):

        print('Desktop bot task started.')
        try:
            task = self.maestro.get_task(execution.task_id) # Fetch the Activity ID from the task
            activity_id = task.activity_id
            mode = 'remote'
        except:
            mode = 'on-premise'

        quote = random_quote() # Fetch random quote
        author = search_author(slug=quote['authorSlug'])
        if quote is None or author is None:
            status = 'Aborted. Random quote or search author request failed.'
        else:
            print("Random quote and author info requests successful. Working on translation...")
            if translate_msg:
                try:
                    quote = translate_object(quote, ['content', 'tags'])
                    author = translate_object(author, ['description'])
                except Exception as err:
                    print('Translation failed. Proceeding anyway...')
            template_params = [
                quote['content'],
                quote['author'],
                author['description'],
                author['link'],
                ', '.join(capitalize(quote['tags'])) + '.'
            ]
            message_payload['template']['components'][0]['parameters'] = as_text_object_list(template_params)
            message_payload['template'] = json.dumps(message_payload['template'])
            unsent = {}; responses = {}
            for i, (name, phone) in enumerate(contact_list.items()): # send quote as whatsapp text message for each in contact list
                try:
                    message_payload['to'] = phone
                    message_response = requests.request("POST", msg_url, headers=headers, data=message_payload) # Send message via whatsapp api
                    responses[name] = json.loads(message_response.text)
                    # whatsapp.send_text_message(phone, text_msg, preview_url=True) # use BotCity WhatsApp plugin
                except requests.HTTPError as err:
                    unsent[name] = type(err).__name__ + ' (Number probably not registered to allowed contacts of WhatsApp Business account)'
                except BaseException as err:
                    unsent[name] = type(err).__name__

            print('Sending text messages finished!')
            n_failed = len([resp for resp in responses.values() if 'error' in list(resp.keys())])
            status = f'Attempted messages: {len(contact_list)}\nUnsent messages: {len(unsent)}.\nFailed sent messages: {n_failed}\n{unsent if len(unsent) else ""}'

        print('Printing task finish status...')
        print(status)

        # Logging task status
        if mode=='on-premise':
            self.maestro.login(server='https://developers.botcity.dev/', login='c8dba406-cfc4-428e-9e42-38b17cfd8d8a', key='C8D_AHUZJZS5R3VA9QIMD875')
        
        # Uncomment if log table is not created (first time logging for activity)        
        # columns = [
        #     Column(name="Quote task status", label="status", width=300),
        # ]
        
        # self.maestro.new_log(
        #     "atvd-02",
        #     columns
        # )

        print('Logging task status to maestro...')
        self.maestro.new_log_entry(
            activity_label="atvd-02",
            values = {
                "status": status,
            }
        )

        print('DONE! Desktop bot task about to end.')
        if mode=='remote':
            self.maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Desktop task Finished OK."
            )
        # print('Desktop bot task ended.')

    def not_found(self, label):
        print(f"Element not found: {label}")

if __name__ == '__main__':
    Bot.main()

