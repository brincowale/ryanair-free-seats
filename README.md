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
Each time the script finish two images will be stored. First is __seats_page.png__ that contains a full screenshot and __seats_(date).png__ with only aircraft with seats.

    from check_seats import Ryanair  
    # Ryanair('confirmation number', 'mail@gmail.com', 'origin airport', 'destination airport')  
    Ryanair('123ABC', 'Mail@gmail.com', 'BRU', 'SXF')

