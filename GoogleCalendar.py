import datetime
import os.path
import CalAgent 


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# TODO: create a while loop that keeps the model ready to recieve prompt
# TODO: create two different function one for viewing list of events in the calendar and
# another for adding events to the calendar
# TODO: create a tool that uses these functions provide it to the model with each prompt.

# If modifying these scopes, delete the file token.json.#
#SCOPES = ["https://www.googleapis.com/auth/calendar"] # this might be too much privilage try using the below instead
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly","https://www.googleapis.com/auth/calendar.events"]


class GoogleCalendar:
  def __init__(self, calendar_id="primary"):
    self.creds = None
    self.service = None
    self.get_service()
    self.calendar_info = self.service.calendars().get(calendarId=calendar_id).execute()
    print(self.calendar_info)
    print(self.calendar_info.get('timeZone'))


  def get_creds(self):
    if self.creds:
      return self.creds
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())
      
    self.creds = creds
    return self.creds

  def get_service(self):
    if self.service:
      return self.service

    if not self.creds:
      self.get_creds()
    # try:
    self.service = build("calendar", "v3", credentials=self.creds)
    # except Exception as error:
    #   print(f"An error occurred while getting the calendar service: {error}")
    # return None
    
    return self.service
  
  def create_event(self, event_details):
    if not self.service:
      self.get_service()

    
    time_zone_name = self.calendar_info.get('timeZone')
    print("current time zone: ", time_zone_name)

    event = {
    'summary': event_details.event_name,
    'location': event_details.location,
    # 'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
      'dateTime': event_details.start_time,
      'timeZone': self.calendar_info.get('timeZone'),
    },
    'end': {
      'dateTime': event_details.end_time,
      'timeZone': self.calendar_info.get('timeZone'),
    },
    # 'recurrence': [
    #   'RRULE:FREQ=DAILY;COUNT=2'
    # ],
    # 'attendees': [
    #   {'email': 'lpage@example.com'},
    #   {'email': 'sbrin@example.com'},
    # ],
    # 'reminders': {
    #   'useDefault': False,
    #   'overrides': [
    #     {'method': 'email', 'minutes': 24 * 60},
    #     {'method': 'popup', 'minutes': 10},
    #   ],
    #},
  }

    event = self.service.events().insert(calendarId='primary', body=event).execute()
    print("Event created successfully")
    print( 'Event created: %s' % (event.get('htmlLink')))

    return event
  
  def get_events(self, num_events=10):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
  
    if not self.service:
      self.get_service()

    try:
      # Call the Calendar API
      now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
      print("Getting the upcoming 10 events")
      events_result = (
          self.service.events()
          .list(
              calendarId="primary",
              timeMin=now,
              maxResults=num_events,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )

      # for k, v in events_result.items():
      #   print(k, v)

      events = events_result.get("items", [])

      if not events:
        print("No upcoming events found.")
        return

      # Prints the start and name of the next 10 events
      # TODO: remove this print statement since it's just a test.
      # for event in events:
      #   start = event["start"].get("dateTime", event["start"].get("date"))
      #   print(start, event["summary"])

      return events

    except HttpError as error:
      print(f"An error occurred: {error}")



