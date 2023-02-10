from typing import Any, Text, Dict, List
from urllib import response
from . import db_functions, debug_host
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
# from pythonping import ping
from . import ssh_connect
import requests

# import our cards
from actions.cards import TeamsCards

cards = TeamsCards()
# import asyncio, asyncssh, sys
# import platform    # For getting the operating system name
# import subprocess  # For executing a shell command

class Actionsshcommand(Action):

    def name(self) -> Text:
        return "action_ask_ssh_command_option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        input_channel = tracker.get_latest_input_channel

        if input_channel() == 'slack' or input_channel() == 'telegram':
            buttons = []
            buttons.append({"title": "hostname", "payload": f"hostname"})
            buttons.append({"title": "ss -ltn", "payload": f"ss -ltn"})
            buttons.append({"title": "cat /proc/meminfo", "payload": f"cat /proc/meminfo"})
            buttons.append({"title": "df", "payload": f"df"})
            dispatcher.utter_message(text="Are you sure to proceed with these details?", buttons=buttons)

            #print("Recent message:", str(tracker.latest_message['text']) )
            return []

        card = cards.card("Which command do you want to execute?") 
        card["attachments"][0]["content"]["actions"] = [cards.button("hostname", "hostname"),
            cards.button("ss -ltn", "ss -ltn"),cards.button("cat /proc/meminfo", "cat /proc/meminfo"),cards.button("df", "df")]

        # teasers = db_functions.show_brain_teaser()
        #dispatcher.utter_message(text="Write Host name?")
        dispatcher.utter_message(json_message=card)
        return []

class ActionsshcommandYesNo(Action):

    def name(self) -> Text:
        return "action_ask_debug_host_proceed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        input_channel = tracker.get_latest_input_channel

        if input_channel() == 'slack' or input_channel() == 'telegram':
            buttons = []
            buttons.append({"title": "Yes", "payload": f"Yes"})
            buttons.append({"title": "No", "payload": f"No"})
            dispatcher.utter_message(text="Are you sure to proceed with these details?", buttons=buttons)

            #print("Recent message:", str(tracker.latest_message['text']) )
            return []

        card = cards.card("Are you sure to proceed with these details?")
        card["attachments"][0]["content"]["actions"] = [cards.button("Yes", "Yes"),
            cards.button("No", "No")]

        # teasers = db_functions.show_brain_teaser()
        #dispatcher.utter_message(text="Write Host name?")
        dispatcher.utter_message(json_message=card)
        return []
        
               
class ActionDebug(Action):

    def name(self) -> Text:
        return "debug_new"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #card = cards.card("Select any one option?") 
        #card["attachments"][0]["content"]["actions"] = [cards.button("star", "st"),
            #cards.button("chr", "ch")]

        # teasers = db_functions.show_brain_teaser()
        dispatcher.utter_message(text="Write startree question?")
        #dispatcher.utter_message(json_message=card)
        #return []
        return [SlotSet("chromeos_question", None), FollowupAction('chromeos_qna_form')]


class ActionNew(Action):

    def name(self) -> Text:
        return "action_new"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        input_channel = tracker.get_latest_input_channel
        #print("Input channel:",input_channel())
        if input_channel() == 'slack' or input_channel() == 'telegram':
            buttons = []
            buttons.append({"title": "ChromeOS bot", "payload": f"/chromeos_knowledge_base"})
            #buttons.append({"title": "StarTree bot", "payload": f"/startree_knowledge_base"})
            buttons.append({"title": "Debug", "payload": f"/debug_help_servers"})
            dispatcher.utter_message(text="Alright, here are the funtions you can perform:", buttons=buttons)

            #print("Recent message:", str(tracker.latest_message['text']) )
            return []

        card = cards.card("Alright, here are the funtions you can perform:") 
        card["attachments"][0]["content"]["actions"] = [cards.button("Startree Bot", "Startree Bot"),
            cards.button("Debug", "Debug")]

        # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(teasers))
        dispatcher.utter_message(json_message=card)
        return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_custom_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # result = db_functions.show_brain_teaser()
        # question = result["question"]
        # question_id = result["q_id"]
        # input_channel = tracker.get_latest_input_channel
        # print("tracker.latest_message['text']",tracker.latest_message['text'])

        # ans = ['time', 'distance', 'light', 'intensity of light', 'Delhi', 'Pune', 'Mumbai', 'Bangalore', 'fermi']
        # for i in ans:
        #     if i == tracker.latest_message['text']:
        #         print("True")
        #         return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", tracker.latest_message['text'])]
        dispatcher.utter_message(text="Thank you111")
        # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(teasers))

        return []


class ActionChromeOSQNA(Action):

    def name(self) -> Text:
        return "action_chromeos_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # =====================================
        # Exit the loop when below words are found.

        # =======================
        stop_bot=['stop','stop flow','back','exit','stop','Stop','Exit']
        if tracker.get_slot('chromeos_question') in stop_bot:
            dispatcher.utter_message(text="Thanks for using our service")
            dispatcher.utter_message(text="If need more assistance type 'help' ")

            return [SlotSet("chromeos_question", None)]

        question = tracker.get_slot('chromeos_question')
        data = {
            "client": "chromeos",
            "input_text": question
        }
        r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        result = r.json()
        lines = str(result).splitlines()
        last_line = lines[-1]
        result = result[:result.rfind('\n')]
        # teasers = db_functions.show_brain_teaser()
        # html_text = result.replace("\n", "<br>")
        # url_link = '<a href="' + last_line + '" target="_blank">' + last_line + '</a>'

        dispatcher.utter_message(text=result)
        dispatcher.utter_message(text=last_line)

        # dispatcher.utter_message(text=html_text)
        # dispatcher.utter_message(text=url_link)
        return [SlotSet("chromeos_question", None), FollowupAction('chromeos_qna_form')]


class ActionChromeOSQNAIntentTrigger(Action):
    print("Hello")
    def name(self) -> Text:
        return "action_chromeos_qna_intent_trigger"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # question = tracker.get_slot('chromeos_question')
        # data = {
        #     "client": "chromeos",
        #     "input_text": question
        # }
        # r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        # result = r.json()
        # lines = str(result).splitlines()
        # last_line = lines[-1]
        # # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(result))
        # dispatcher.utter_message(text=last_line)
        # return [UserUttered("/chromeos_knowledge_base", intent={'name': 'chromeos_knowledge_base', 'confidence': 1.0})]
        return []


class ActionStarTreeQNA(Action):

    def name(self) -> Text:
        return "action_startree_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # =====================================
        # Exit the loop when below words are found.

        # =======================
        stop_bot=['stop','stop flow','back','exit','Stop','Exit']
        if tracker.get_slot('startree_question') in stop_bot:
            dispatcher.utter_message(text="Thanks for using our service")
            dispatcher.utter_message(text="If need more assistance type 'help' ")

            return [SlotSet("startree_question", None)]



        question = tracker.get_slot('startree_question')
        data = {
            "client": "startree",
            "input_text": question
        }
        r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        result = r.json()
        lines = str(result).splitlines()
        last_line = lines[-1]
        result = result[:result.rfind('\n')]
        # teasers = db_functions.show_brain_teaser()

        # html_text = result.replace("\n", "<br>")
        # url_link = '<a href="' + last_line + '" target="_blank">' + last_line + '</a>'

        dispatcher.utter_message(text=result)
        dispatcher.utter_message(text=last_line)

        # dispatcher.utter_message(text=html_text)
        # dispatcher.utter_message(text=url_link)
        return [SlotSet("startree_question", None), FollowupAction('startree_qna_form')]


class ActionStarTreeQNAIntentTrigger(Action):
    print("Hello")
    def name(self) -> Text:
        return "action_startree_qna_intent_trigger"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="please wait for a while")

        # question = tracker.get_slot('startree_question')
        # data = {
        #     "client": "startree",
        #     "input_text": question
        # }
        # r = requests.post('http://qna-api.jiva.live/qna-engine/', json=data)
        # result = r.json()
        # lines = str(result).splitlines()
        # last_line = lines[-1]
        # # teasers = db_functions.show_brain_teaser()
        # dispatcher.utter_message(text=str(result))
        # dispatcher.utter_message(text=last_line)

        # return [UserUttered("/startree_knowledge_base", intent={'name': 'startree_knowledge_base', 'confidence': 1.0})]
        return []


class ShowBrainTeaser(Action):

    def name(self) -> Text:
        return "action_show_brain_teaser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        result = db_functions.show_brain_teaser()
        print("Result is:",result)
        question = result["question"]
        question_id = result["q_id"]
        # dispatcher.utter_message(text=question)
        input_channel = tracker.get_latest_input_channel
        # print("Input channel:",input_channel())
        # card = cards.card("Do you want to continue?")

        print("Recent message:", str(tracker.latest_message['text']) )
        
        # ans = ['time', 'distance', 'light', 'intensity of light', 'Delhi', 'Pune', 'Mumbai', 'Bangalore', 'fermi']
        # for i in ans:
        #     if i == tracker.latest_message['text']:
        #         print("True")
        #         return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", tracker.latest_message['text'])]
        # return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", tracker.latest_message['text'])]
        ###########################################
        buttons1 = []

        # card = cards.card(question)
        #######################################

        # for d in result["options"]:
        #     print("I for options:",d)
        #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
        #     buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
            # buttons1.append(d)
            # card["attachments"][0]["content"]["actions"] = [cards.button(d,d)]
        if input_channel() == 'slack' or input_channel() == 'telegram':
            buttons = []
            for d in result["options"]:
                fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
                buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
            dispatcher.utter_message(text=question, buttons=buttons)

            print("Recent message:", str(tracker.latest_message['text']) )
            return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
        

        # for d in result["options"]:
        #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
        #     buttons1.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
        # dispatcher.utter_message(text=question, buttons=buttons1)
        # return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
            
        # buttons1 = []
        # card = cards.card(question)
        # for d in result["options"]:
        #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
        #     card["attachments"][0]["content"]["actions"] = [cards.button(d, d)]
            # print("I for options:",d)
            # buttons1.append(d)
        # print("Buttons:",buttons1)
        # card["attachments"][0]["content"]["actions"] = [cards.button(buttons1[0], buttons1[0]),
        #     cards.button(buttons1[1], buttons1[1]),cards.button(buttons1[2], buttons1[2]),cards.button(buttons1[3], buttons1[3])]

        else:
            buttons1 = []
            card = cards.card(question)
            for d in result["options"]:
                fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
                # card["attachments"][0]["content"]["actions"] = [cards.button(d,f"/intent_brain_teaser_answer {fill_slot}")]
                print("I for options:",d)
                buttons1.append([d, f"/intent_brain_teaser_answer {fill_slot}"])
            # print("Buttons:",buttons1)
            
            card["attachments"][0]["content"]["actions"] = [cards.button(buttons1[0][0], buttons1[0][1]),
                cards.button(buttons1[1][0], buttons1[1][1]),cards.button(buttons1[2][0], buttons1[2][1]),cards.button(buttons1[3][0], buttons1[3][1])]

            # for i in range(len(buttons1)):
            #     print(buttons1[i],i)
            #     card["attachments"][0]["content"]["actions"] = [cards.button(buttons1[0], buttons1[0]),
            #     cards.button(buttons1[1], buttons1[1]),cards.button(buttons1[2], buttons1[2]),cards.button(buttons1[3], buttons1[3])]
                # card["attachments"][1]["content"]["actions"] = [cards.button(buttons1[1], buttons1[1])]
                # card["attachments"][2]["content"]["actions"] = [cards.button(buttons1[2], buttons1[2])]
                # card["attachments"][3]["content"]["actions"] = [cards.button(buttons1[3], buttons1[3])]
                # fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
                # card["attachments"][0]["content"]["actions"] = [cards.button(d, d)]
                # # buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
            dispatcher.utter_message(json_message=card)
            return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
            # print("Recent message:", tracker.latest_message['text'] )
            # return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
            # return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]

            # for d in result["options"]:
            #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
            #     card["attachments"][0]["content"]["actions"] = [cards.button(d, d)]
            #     # buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})

            #     dispatcher.utter_message(json_message=card)

            #     return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
        
        

        # nm = {
        #     "attachments": [{
        #         "contentType": "application/vnd.microsoft.card.adaptive",
        #         "content": {
        #             "type": "AdaptiveCard",
        #             "version": "1.0",
        #             "body": [{
        #                 "type": "TextBlock",
        #                 "text": question
        #             }],
        #             "actions": [{
        #                     "type": "Action.Submit",
        #                     "title": "Button1",
        #                     "data": {
        #                         "msteams": {
        #                             "type": "imBack",
        #                             "value": "light"
        #                         }
        #                     }
        #                 },
        #             ]
        #         }
        #     }]
        # }
        # nm = {
        #     "attachments": [{
        #         "contentType": "application/vnd.microsoft.card.adaptive",
        #         "content": {
        #             "type": "AdaptiveCard",
        #             "version": "1.0",
        #             "body": [{
        #                 "type": "TextBlock",
        #                 "text": question
        #             }],
        #             "actions": [{
        #                     "type": "Action.Submit",
        #                     "title": "Button1",
        #                     "data": {
        #                         "msteams": {
        #                             "type": "imBack",
        #                             "value": "Hello11"
        #                         }
        #                     }
        #                 },
        #                 {
        #                     "type": "Action.Submit",
        #                     "title": "Button2",
        #                     "value": "Hello11"
        #                 }
        #             ]
        #         }
        #     }]
        # }
        

        # nm = { 
        #     "type": "Action.Submit", 
        #     "title": "Button", 
        #     "data": {
        #         "msteams": { 
        #             "type": "imBack",
        #             "value": "/intent_brain_teaser_answer"
        #         } 
        #     }, 
        #     "style": "positive" 
        # }
        # nm = {
        #     "type": "Action.Submit",
        #     "title": "My MessageBack button",
        #     "data": {
        #         "msteams": {
        #             "type": "messageBack",
        #             "displayText": "I clicked this button",
        #             "value": "light"
        #         }
        #     }
        # }

        # dispatcher.utter_message(text=question, buttons=buttons1)
        # return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]
        # dispatcher.utter_message(json_message=nm)

        return [SlotSet("question_id", question_id), SlotSet("brain_teaser_answer", None)]


class ValidateBrainTeaserAnswer(Action):
    print("Validate Brain")
    def name(self) -> Text:
        return "action_validate_brain_teaser_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brain_teaser_answer = tracker.get_slot('brain_teaser_answer')
        question_id = tracker.get_slot('question_id')

        if db_functions.brain_teaser_answer_check(q_id=question_id, answer=brain_teaser_answer):
            dispatcher.utter_message(text="Great Job! Let's move forward.")
        else:
            dispatcher.utter_message(text="Sorry, that was incorrect. Let's move forward.")

        return [SlotSet("brain_teaser_answer", None), SlotSet("question_id", None)]


class ActionDebugHostValidate(Action):

    def name(self) -> Text:
        return "action_debug_host_validate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_value = tracker.get_slot("debug_host_proceed")
        if slot_value == 'No':
            dispatcher.utter_message(text=f"Operation canceled.")
        elif slot_value == 'Yes':
            # result = ''
            # dispatcher.utter_message(text= f"fetching results.. please wait..")
            # Option for the number of packets as a function of

            host_value = tracker.get_slot("debug_host_name")
            username_value = tracker.get_slot("debug_host_username")
            password_value = tracker.get_slot("debug_host_password")
            ssh_command_value = tracker.get_slot("ssh_command_option")

            # buttons =[]
            # for d in result["options"]:
            #     fill_slot = '{"brain_teaser_answer" : "' + d + '"}'
            #     buttons.append({"title": d, "payload": f"/intent_brain_teaser_answer {fill_slot}"})
            result = ssh_connect.ssh_exec_command(host=host_value, username=username_value, password=password_value,
                                                  command=ssh_command_value)
            # print(("*"*100) + "\n" + str(result))
            dispatcher.utter_message(text=result)
        else:
            dispatcher.utter_message(text="Didn't expect that input, please try again.")
            # if ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command='hostname'):
            #     # try:
            #     #     command = 'ss -ltn'
            #     #     # result = asyncio.get_event_loop().run_until_complete(ssh_connect.run_client(host=host_value, username=username_value, password=password_value, command=command))
            #     #     result = ssh_connect.ssh_exec_command(host=host_value, username=username_value, password=password_value, command=command)
            #     #     # result = ' '.join([str(elem)+'\n' for elem in result_list])
            #     # # except (OSError, asyncssh.Error) as exc:
            #     # except Exception as exc:
            #     #     result = 'SSH connection failed: ' + str(exc)
            #         # sys.exit()
            #     dispatcher.utter_message(text= 'Connection Successful. Executing command..')
            #     # command_list = ['hostname', 'ss -ltn', 'cat /proc/meminfo', 'df']
            #     # buttons =[]
            #     # for d in command_list:
            #     #     fill_slot = "{'ssh_command_option' : '" + d + "'}"
            #     #     buttons.append({"title": d, "payload": f"/intent_ssh_command_option {fill_slot}"})
            #     # dispatcher.utter_message(text="", buttons=buttons)
            #     result = ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command=ssh_command_value)
            #     dispatcher.utter_message(text= result)
            # else:
            #     dispatcher.utter_message(text= "SSH Connection failed")
        return [SlotSet("debug_host_name", None), SlotSet("debug_host_username", None),
                SlotSet("debug_host_password", None), SlotSet("debug_host_proceed", None),
                SlotSet("ssh_command_option", None)]

# class ActionDebugHostExecuteCommand(Action):

#     def name(self) -> Text:
#         return "action_debug_host_execute_command"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         host_value = tracker.get_slot("debug_host_name")
#         username_value = tracker.get_slot("debug_host_username")
#         password_value = tracker.get_slot("debug_host_password")
#         ssh_command_value = tracker.get_slot("ssh_command_option")

#         result = ssh_connect.ssh_conn_check(host=host_value, username=username_value, password=password_value, command=ssh_command_value)
#         dispatcher.utter_message(text= result)
#         return [SlotSet("debug_host_name", None), SlotSet("debug_host_username", None), SlotSet("debug_host_password", None), SlotSet("debug_host_proceed", None), SlotSet("ssh_command_option", None)]
