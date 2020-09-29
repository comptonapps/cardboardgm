from models import User, Card, TradeRequest, RequestCard, db
from app import app

db.drop_all()
db.create_all()

jcom = User.register(username="jcompton", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
klew = User.register(username="klew", password="qqqqqqqq", first_name="Kyle", last_name="Lewis", email="k@l.com")
mgon = User.register(username="mgonzales", password="qqqqqqqq", first_name="Marco", last_name="Gonzales", email="m@g.com")
u4 = User.register(username="kseager", password="qqqqqqqq", first_name="Kyle", last_name="Seager", email="k@s.com")
u5 = User.register(username="tfrance", password="qqqqqqqq", first_name="Ty", last_name="France", email="t@f.com")
u6 = User.register(username="slong", password="qqqqqqqq", first_name="Shed", last_name="Long", email="s@l.com")
u7 = User.register(username="jcrawford", password="qqqqqqqq", first_name="J.P.", last_name="Crawford", email="jp@c.com")
u8 = User.register(username="dmoore", password="qqqqqqqq", first_name="Dylan", last_name="Moore", email="d@m.com")
u9 = User.register(username="pervin", password="qqqqqqqq", first_name="Phil", last_name="Ervin", email="p@e.com")
u10 = User.register(username="jsheffield", password="qqqqqqqq", first_name="Justus", last_name="Sheffield", email="j@s.com")
u11 = User.register(username="jdunn", password="qqqqqqqq", first_name="Justin", last_name="Dunn", email="j@d.com")
u12 = User.register(username="ykikuchi", password="qqqqqqqq", first_name="Yusei", last_name="Kikuchi", email="y@k.com")
u13 = User.register(username="kgraveman", password="qqqqqqqq", first_name="Kendall", last_name="Graveman", email="k@g.com")
u14 = User.register(username="jodom", password="qqqqqqqq", first_name="Joe", last_name="Odom", email="j@o.com")
u15 = User.register(username="ltorrens", password="qqqqqqqq", first_name="Luis", last_name="Torrens", email="l@t.com")
u16 = User.register(username="jmarmo", password="qqqqqqqq", first_name="Jose", last_name="Marmolejos", email="j@m.com")
u17 = User.register(username="ttrammell", password="qqqqqqqq", first_name="Taylor", last_name="Trammell", email="t@t.com")
u18 = User.register(username="jkelenic", password="qqqqqqqq", first_name="Jarred", last_name="Kelenic", email="j@k.com")
u19 = User.register(username="jgerber", password="qqqqqqqq", first_name="Joey", last_name="Gerber", email="j@g.com")
u20 = User.register(username="ewhite", password="qqqqqqqq", first_name="Evan", last_name="White", email="e@w.com")
u21 = User.register(username="yhirano", password="qqqqqqqq", first_name="Yosahiso", last_name="Hirano", email="y@h.com")
u22 = User.register(username="twalker", password="qqqqqqqq", first_name="Taijuan", last_name="Walker", email="t@w.com")
u23 = User.register(username="anola", password="qqqqqqqq", first_name="Austin", last_name="Nola", email="a@n.com")
u24 = User.register(username="dgordon", password="qqqqqqqq", first_name="Dee", last_name="Gordon", email="d@g.com")
u25 = User.register(username="nmargevicius", password="qqqqqqqq", first_name="Nick", last_name="Margevicius", email="n@g.com")

db.session.add_all([jcom, klew, mgon, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22, u23, u24, u25])
db.session.commit()

acuna = Card.create(owner_id=jcom.id, player="Ronald Acuna Jr", year="2018", set_name="Topps Series 2", number="698", desc="PSA 10")
tatis = Card.create(owner_id=jcom.id, player="Fernando Tatis Jr", year="2019", set_name="Topps Seris 2", number="410", desc="PSA 10")

griffeyUD = Card.create(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Upper Deck", number="1", desc="PSA 9")
griffeyDon = Card.create(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Donruss", number="33", desc="PSA 10")

mantle56 = Card.create(owner_id=mgon.id, player="Mickey Mantle", year="1956", set_name="Topps", number="135", desc="PSA 5.5")
mantle52 = Card.create(owner_id=mgon.id, player="Mickey Mantle", year="1952", set_name="Topps", number="311", desc="Authentic")

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
