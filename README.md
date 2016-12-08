# Kibana-Protector
A simple python proxy for securing Kibana instances that face the outside world from settings changes while allowing public viewing

## Features
Provides a landing page for users to complete a capcha (currently google capcha) and then proceed to Kibana
the proxy also blocks settings changes to Kibana, although this isn't tested well yet. The idea is a look don't touch
feature set.

I really wouldn't be that difficult to expand this to provide a basic user system for Kibana but that's not the goal right now.
