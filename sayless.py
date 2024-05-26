

import CalAgent
import GoogleCalendar


def main():
  calendar = GoogleCalendar.GoogleCalendar()
  calendar.get_events()
  calAgent = CalAgent.CalAgent(calendar)
  #calAgent.get_events()
  calAgent.test()

#  cal = GoogleCalendar()
#  cal.get_events()


if __name__ == "__main__":
  main()