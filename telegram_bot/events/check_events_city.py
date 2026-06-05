from datetime import datetime 


def check_event_city(events,city: str):

    if len(events) <= 1:
        return events[0]

    for i,event in enumerate(events):
        if city == 'coruna':
            if 'admin' in event["name"]["text"].strip().lower():
                return check_repeated_event(event,events[i+1])
        elif city == 'vigo':
            if 'olivarmy' in event["name"]["text"].strip().lower():
                return check_repeated_event(event,events[i+1])
        i+=1

        return "No event"



def check_repeated_event(current_event, next_event):
    current_event_name = current_event["name"]["text"].strip().lower()
    next_event_name = next_event["name"]["text"].strip().lower()
    current_event_month = datetime.fromisoformat(current_event["start"]["local"]).month
    next_event_month = datetime.fromisoformat(next_event["start"]["local"]).month


    if current_event_name != next_event_name:
        return current_event
    
    if current_event_month == next_event_month:
        return next_event
    else:
        return current_event