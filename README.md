# cardboard_gm
### Online Baseball Card Collection

This app is for sharing your baseball card collection with other collection 'Managers'.  You can view collections and propose trades for cards from other managers' collections.
Managers can view current eBay listings of cards to gauge card value in evaluating trades.  API docs here: https://developer.ebay.com/DevZone/finding/Concepts/FindingAPIGuide.html

The database uses SQLAlchemy to track Users(managers), Cards, TradeRequests, and RequestCards.  Schema outline:  
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/cbgmschema.jpg)

The app can be found at https://cardboardgm.herokuapp.com

## App Flow

Upon registering an account, authenticated managers can view all of the cards in the database, either by searching through all cards, or searching
through a collection on a specific manager's page.  Clicking on a card cell from the Cards page or from a Managers collection will take you to a 
card detail page, in which you can view a larger, detailed image, view active trade requests that other managers have requested, or you can also propose 
a trade request from cards in your own collection.

#### Managers 
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/managers.png)

#### Cards
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/cards.png)

#### Card Page
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/card.png)

### Trade Requests

If a trade is requested, a trade request screen will be displayed in which you can choose cards from your own collection to offer for the requested card.
You can find cards from scrolling through your entire collection or using the search bar to enter any combination of query info (year, set name, player, number, description).

#### Viewing Your Trade Requests
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/request.png)

#### Creating a request for another manager's card
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/create-request.png)

## EBAY API

Initially, the app used the findCompletedItems API from eBay so managers could evaluate card pricing based on previous eBay sales.  That API was made private
on 10/15/2020, so now the app finds any fixed price items currently for sale on eBay.

## APP TECHNOLOGIES

This app was created using Flask and Python on the server side and uses jinja templates for page presentation.  In addition to HTML and CSS, vanilla js is used for client side coding.  I decided not to use bootstrap or jQuery in this project so I could get a better grasp on app development from the ground up.  
