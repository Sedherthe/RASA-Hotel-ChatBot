# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import math
import datetime

class ActionSetRoomPreference(Action):

    def name(self) -> Text:
        return "action_set_room_preference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker)
        dispatcher.utter_message(template="utter_confirm_booking")

        return []

class ActionSetNumRooms(Action):

    def name(self) -> Text:
        return "action_set_num_rooms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num_rooms = tracker.get_slot("num_rooms")
        num_persons = tracker.get_slot("num_people")
        print(f'num rooms is {num_rooms}')

        # If unable to extract num persons then ask again, else update num rooms
        if num_rooms is None:
            if num_persons is None:
                num_rooms = "1"
            else:
                num_rooms = str(math.ceil(int(num_persons)/2)) # Assumption: 2 persons per room
        else:
            num_rooms = num_rooms
        return [SlotSet("num_rooms", num_rooms)] 


class ActionScheduleCleaning(Action):

    def name(self) -> Text:
        return "action_schedule_cleaning"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dur = tracker.get_slot("duration")
        unit = tracker.get_slot("time_unit")

        if dur is None:
            dispatcher.utter_message(text='Sure, I will send someone to your room right away')
            return []

        if unit is None:
            dispatcher.utter_message(text='sure, Sending a cleaner to your room')
            return []

        if unit == "sec":
            dur = int(dur)
            dur = math.ceil(dur/60)
            if dur < 1:
                dispatcher.utter_message(text=f'Sure, Sending cleaner to your room in a minute')
            else:
                dispatcher.utter_message(text=f'Sure, Sending cleaner to your room in {dur} minutes')
            return []

        time_tuple = datetime.datetime.now().timetuple()
        h = time_tuple[3]
        m = time_tuple[4]

        if unit == "min":
            m += int(dur)
            if m > 60:
                h += int(m/60)
                m = m % 60

        elif unit == "hour":
            h += int(dur)

        h = h % 24
        if h > 12:
            h = h - 12
            suff = 'PM'
        else:
            suff = 'AM'
        m = "%02d" % m
        dispatcher.utter_message(text=f'Sure, I have scheduled a cleaning for {h}:{m} {suff} today')        
        return []