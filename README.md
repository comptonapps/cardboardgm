# cardboard_gm
### Online Baseball Card Collection

This app is for sharing your baseball card collection with other collection 'Managers'.  You can view collections and propose trades for cards from other managers' collections.
Managers can view current eBay listings of cards to gauge card value in evaluating trades.  API docs here: https://developer.ebay.com/DevZone/finding/Concepts/FindingAPIGuide.html

The database uses SQLAlchemy to track Users(managers), Cards, TradeRequests, and RequestCards.  Schema outline:  
![This is a alt text.](https://cardboardgmpics.s3-us-west-2.amazonaws.com/schema-design/cbgmschema.jpg)
