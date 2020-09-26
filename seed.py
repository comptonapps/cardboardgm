from models import User, Card, TradeRequest, RequestCard, db
from app import app

db.drop_all()
db.create_all()

jcom = User.register(username="jcompton", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
klew = User.register(username="klew", password="qqqqqqqq", first_name="Kyle", last_name="Lewis", email="k@l.com")
mgon = User.register(username="mgonzales", password="qqqqqqqq", first_name="Marco", last_name="Gonzales", email="m@g.com")

db.session.add_all([jcom, klew, mgon])
db.session.commit()

acuna = Card(owner_id=jcom.id, player="Ronald Acuna Jr", year="2018", set_name="Topps Series 2", number="698", desc="PSA 10")
tatis = Card(owner_id=jcom.id, player="Fernando Tatis Jr", year="2019", set_name="Topps Seris 2", number="410", desc="PSA 10")

griffeyUD = Card(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Upper Deck", number="1", desc="PSA 9")
griffeyDon = Card(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Donruss", number="33", desc="PSA 10")

mantle56 = Card(owner_id=mgon.id, player="Mickey Mantle", year="1956", set_name="Topps", number="135", desc="PSA 5.5")
mantle52 = Card(owner_id=mgon.id, player="Mickey Mantle", year="1952", set_name="Topps", number="311", desc="Authentic")

db.session.add_all([acuna, tatis, griffeyDon, griffeyUD, mantle52, mantle56])
db.session.commit()

req1 = TradeRequest(from_id=1, to_id=2)
req2 = TradeRequest(from_id=2, to_id=1)
req3 = TradeRequest(from_id=2, to_id=3)
req4 = TradeRequest(from_id=2, to_id=3)
req5 = TradeRequest(from_id=3, to_id=1)
req6 = TradeRequest(from_id=3, to_id=2)

db.session.add_all([req1, req2, req3, req4, req5, req6])
db.session.commit()

rc1 = RequestCard(request_id=1, card_id=2, requested=False)
rc2 = RequestCard(request_id=1, card_id=3, requested=True)
rc3 = RequestCard(request_id=2, card_id=3, requested=False)
rc4 = RequestCard(request_id=2, card_id=4, requested=False)
rc5 = RequestCard(request_id=2, card_id=1, requested=True)
rc6 = RequestCard(request_id=3, card_id=3, requested=False)
rc7 = RequestCard(request_id=3, card_id=4, requested=False)
rc8 = RequestCard(request_id=3, card_id=5, requested=True)
rc9 = RequestCard(request_id=4, card_id=4, requested=False)
rc10 = RequestCard(request_id=4, card_id=6, requested=True)
rc11 = RequestCard(request_id=5, card_id=5, requested=False)
rc12 = RequestCard(request_id=5, card_id=1, requested=True)
rc13 = RequestCard(request_id=6, card_id=5, requested=False)
rc14 = RequestCard(request_id=6, card_id=3, requested=True)
rc15 = RequestCard(request_id=6, card_id=4, requested=True)

db.session.add_all([rc1, rc2, rc3, rc4, rc5, rc6, rc7, rc8, rc9, rc10, rc11, rc12, rc13, rc14, rc15])
db.session.commit()
