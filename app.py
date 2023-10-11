import json

from extractors.action import ActionExtractor
from extractors.adidas import AdidasExtractor
from extractors.arhelan import ArhelanExtractor
from extractors.auchan import AuchanExtractor
from extractors.biedronka import BiedronkaExtractor
from extractors.breakandwash import BreakAndWashExtractor
from extractors.carrefour import CarrefourExtractor
from extractors.castorama import CastoramaExtractor
from extractors.chorten import ChortenExtractor
from extractors.costacoffee import CostaCoffeeExtractor
from extractors.cukierniasowa import CukierniaSowaExtractor
from extractors.dealz import DealzExtractor
from extractors.delikatesycentrum import DelikatesyCentrumExtractor
from extractors.dino import DinoExtractor
from extractors.empik import EmpikExtractor
from extractors.eobuwie import EObuwieExtractor
from extractors.epaka import EpakaExtractor
from extractors.eurosklep import EuroSklepExtractor
from extractors.gant import GantExtractor
from extractors.glovo import GlovoExtractor
from extractors.gromulski import GromulskiExtractor
from extractors.groszek import GroszekExtractor
from extractors.hebe import HebeExtractor
from extractors.hm import HMExtractor
from extractors.hotel import HotelExtractor
from extractors.intermarche import IntermarcheExtractor
from extractors.kaufland import KauflandExtractor
from extractors.kfc import KFCExtractor
from extractors.komfort import KomfortExtractor
from extractors.lagardere import LagardereExtractor
from extractors.leroymerlin import LeroyMerlinExtractor
from extractors.levis import LevisExtractor
from extractors.lewiatan import LewiatanExtractor
from extractors.lidl import LidlExtractor
from extractors.livio import LivioExtractor
from extractors.lubaszka import LubaszkaExtractor
from extractors.mcdonalds import McDonaldsExtractor
from extractors.mediaexpert import MediaExpertExtractor
from extractors.naszsklep import NaszSklepExtractor
from extractors.netto import NettoExtractor
# from extractors.ochnik import OchnikExtractor
from extractors.obi import ObiExtractor
from extractors.odido import OdidoExtractor
from extractors.oskroba import OskrobaExtractor
from extractors.pasibus import PasibusExtractor
from extractors.pepco import PepcoExtractor
from extractors.pizzahut import PizzaHutExtractor
from extractors.play import PlayExtractor
from extractors.polomarket import PoloMarketExtractor
from extractors.pyszne import PyszneExtractor
from extractors.retailmap import RetailMapExtractor
from extractors.rossmann import RossmannExtractor
from extractors.shop4f import Shop4FExtractor
from extractors.smyk import SmykExtractor
from extractors.spar import SparExtractor
from extractors.spc import SPCExtractor
from extractors.subway import SubwayExtractor
from extractors.tchibo import TchiboExtractor
from extractors.timberland import TimberlandExtractor
from extractors.tkmaxx import TKMaxxExtractor
from extractors.tmobile import TMobileExtractor
from extractors.topaz import TopazExtractor
from extractors.topmarket import TopMarketExtractor
from extractors.visionexpress import VisionExpressExtractor
from extractors.wittchen import WittchenExtractor
from extractors.wojas import WojasExtractor
from extractors.zabka import ZabkaExtractor
from extractors.zahir import ZahirExtractor
from extractors.ziaja import ZiajaExtractor
from extractors.pekaosa import PekaoSAExtractor
from temputils import draw_pois

completed = [
    # ActionExtractor,
    # AdidasExtractor,
    # ArhelanExtractor,
    # AuchanExtractor,
    # BiedronkaExtractor,
    # BreakAndWashExtractor,
    # CarrefourExtractor,
    # CastoramaExtractor,
    # ChortenExtractor,
    # CostaCoffeeExtractor,
    # CukierniaSowaExtractor,
    # DealzExtractor,
    # DelikatesyCentrumExtractor,
    # DinoExtractor,
    # EmpikExtractor,
    # EObuwieExtractor,
    # EpakaExtractor,
    # EuroSklepExtractor,
    # GantExtractor,
    # GlovoExtractor, # time intensive
    GromulskiExtractor,
    GroszekExtractor,
    HebeExtractor,
    HMExtractor,
    HotelExtractor,
    IntermarcheExtractor,
    KauflandExtractor,
    KFCExtractor,
    KomfortExtractor,
    LagardereExtractor,
    LeroyMerlinExtractor,
    LevisExtractor,
    LewiatanExtractor,
    LidlExtractor,
    LivioExtractor,
    LubaszkaExtractor,
    McDonaldsExtractor,
    MediaExpertExtractor,
    NaszSklepExtractor,
    NettoExtractor,
    # OchnikExtractor,
    ObiExtractor,
    OdidoExtractor,
    OskrobaExtractor,
    PasibusExtractor,
    PepcoExtractor,
    PizzaHutExtractor,
    PlayExtractor,
    PoloMarketExtractor,
    # PyszneExtractor, # time intensive
    RetailMapExtractor,
    RossmannExtractor,
    Shop4FExtractor,
    SmykExtractor,
    SparExtractor,
    SPCExtractor,
    SubwayExtractor,
    TchiboExtractor,
    TimberlandExtractor,
    TKMaxxExtractor,
    TMobileExtractor,
    TopazExtractor,
    TopMarketExtractor,
    VisionExpressExtractor,
    WittchenExtractor,
    WojasExtractor,
    ZabkaExtractor,
    ZahirExtractor,
    ZiajaExtractor,
    PekaoSAExtractor
]

draw_pois(completed)


tests = [
    # 'Pon. - Sob: 06:00 - 22:00, Ndz. handlowe: 09:00 - 20:00',
    # 'Pon- Pt: 7:00 - 22:00 , Sobota: 7:00 - 21:00 Niedziela : 8:00 - 20:00',
    # 'Zamknięte',
    # 'Pn. - So. 10:00-21:00',
    # 'pon.-sob. 09:00 - 21:00      niedz. 10:00 - 20:00',
    # 'pon.-pt. 11:00 - 21:00      sob. 10:00 - 21:00 niedz. 10:00 - 19:00',
    # 'pon.-sob. 10:00-22:00</br>nd. 10:00-21:00</br>',
    # 'pn-pt: 09:00 - 21:00<br> sb: 09:00 - 21:00<br> nd: 10:00 - 20:00',
    # 'pon, śr, czw 10:00 - 18:00 <br>wt. pt  09:00 - 17:00 <br> sb: 09:00 - 13:00<br> nd: nieczynne',
    # 'poniedzialek xddddd 1.00    9:00 wt 12:12 --- 15:11',
    'czynne poniedziałek – sobota + niedziele handlowe od 8 do 22'
]
#
# for test in tests:
#     print(utils.opening_dates.create_from_freetext(test))
