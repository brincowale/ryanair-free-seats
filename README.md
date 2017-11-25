# Ryanair free seats
Ryanair has the option to choose a seat if you pay a fee or a random seat for free. Luckily there's a way to get the seat of your choise for free. Ryanair asignation isn't random so you will know when seats will get booked. You can find all information about this process at [flights-blog](http://flights-blog.lowcostroutes.com/2014/04/how-to-get-a-free-seat-on-ryanair/).

This script allows you get an screenshot of the aircraft with her seats. In my example I wanted the seat 1A because has more space for legs. I had to wait until 8 hours before of flight and then checkin. This is only a test, you have to know about cons. I created a gif file with all screenshots until all row 2 was booked, so 1A was the next.

![alt text](http://i.imgur.com/Q7t4Skw.gif "Ryanair free seats")

This method uses legacy website of Ryanair because the new website doesn't see which seats are booked. In the nearly future this script will stop working if Ryanair not recover this feature.

# Requirements
* Selenium
* Python 2.7
* PhantomJS
* PIL / Pillow

# Usage

```
usage: check_seats.py [-h] -r RESERVATION -e EMAIL [-t POLL_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -r RESERVATION, --reservation RESERVATION
                        Flight reservation number
  -e EMAIL, --email EMAIL
                        Email address used for reservation
  -t POLL_INTERVAL, --poll-interval POLL_INTERVAL
                        Time in seconds between checks
```

Each time the script a few images will be stored. First is __seats_page.png__ that contains a full screenshot and __seats_(date).png__ with only aircraft with seats. Besides those, a few more debugging images are saved (`checked/filled/homepage/manage_page/seat_map.png`).

`python check_seats.py -r RESERVATION_ID -e EMAIL_USED_FOR_RESERVATION`
