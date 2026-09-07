"""Curated public-source snapshot. No live-operation or exhaustive-coverage claim."""
import json, collections, pathlib, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE='2026-09-07'
places=[]
# Fields: map id | branch name | district | category | source address | lat,lng | business phone | dishes mentioned in source | platform score | dated review (NOT visit/verification date)
raw='''
B0FFLAQI13|串王阿三烧烤(高沙商业街店)|钱塘区|中式烧烤|学林街1131号一楼、二楼|30.315543,120.337597|18069773723;18358148107|烤茄子、扇贝、奶黄包|4.5|2020-08-26
B0HUOZDVVM|肉本家·炭烤肉(杭州浙大总店)|西湖区|韩式烤肉|紫荆花北路宝港生活广场1楼188号|30.306813,120.092541|0571-81111130;0571-81111160|雪花牛肉、厚切五花|4.9|2025-09-29
B0JURM6891|烤大仙·烤鲈鱼·东北烧烤(华中南路店)|上城区|东北烧烤|华中南路120号|30.321498,120.201108|17328876535;18067932777|乳酸菌牛肉、剖开串烤鸡爪||2023-07-23
B0K6BRJ30G|牛小新烧肉·和牛放题(龙湖杭州金沙天街店)|钱塘区|日式烧肉|金沙大道560号龙湖杭州金沙天街L3|30.310315,120.326214|0571-86938285|||
B0K3M7O3SX|牛小新烧肉·和牛放题(萧山万象汇店)|萧山区|日式烧肉|金城路927号万象汇3楼L329|30.181893,120.268979|18072988738|芝士肥牛、谷饲横膈膜、海鲜拼盘||2024-11-19
B0JAGSARXL|京永盛·老北京铜锅涮肉·烤串(紫金港店)|西湖区|复合烤肉|古墩路705号新时代紫金家具商城A座一楼A118|30.309206,120.093891|19357318577|||
B0K6C72LQD|柒房里·鸡汤火锅·云南烤肉(滨江店)|滨江区|复合烤肉|西兴街道襄七房225号5幢|30.177972,120.203832|17367130617|||2024
B0IUTS4JWH|牛小新烧肉屋(滨江银泰店)|滨江区|日式烧肉|西兴街道银泰百货B区4层407室|30.202028,120.221717|0571-87801978||1.7|2022
B0I2THX2A3|齐齐哈尔烤肉鹤之乡(环翼城店)|上城区|齐市烤肉|鸿泰路128号4幢1层101室-16|30.293192,120.222441|19157880452|传统烤牛肉||2022
B0FFJV1W68|御牛道日式烤肉料理(杭州万象城店)|上城区|日式烧肉|富春路701号杭州万象城B2层287号(Ole超市对面)|30.251246,120.215268|0571-85291818;15372038252||4.8|
B0GKY1LDQS|小屋烤肉|拱墅区|中式烤肉|沈塘桥路56号|30.281465,120.151547|18069877988|||2022
B0J1FZ4USK|朴太院·烤肉万岁·创意料理(大悦城店)|拱墅区|韩式烤肉|大悦城悦街B栋3楼313室|30.300905,120.129902|18072936766|||
B0H65SKZR5|趣东北齐齐哈尔家庭烤肉|拱墅区|齐市烤肉|信义坊商街28号|30.294186,120.144959|0571-86906515;4000678333|大盆牛肉、酸菜||2022
B0FFIK12DE|御牛道日式烤肉料理(永旺梦乐城店)|余杭区|日式烧肉|古墩路1888号永旺梦乐城2层262号|30.360667,120.057686|0571-85291618;17357152570||4.8|2018
B0IDDA75PD|芝小官毛肚火锅烤肉自助(龙湖杭州吾角天街店)|钱塘区|自助烤肉|金沙大道30号吾角天街4F-01|30.310193,120.335941|0571-88880177|||
B0FFIPNDJB|AJIYA味屋日式烤肉(开元路店)|上城区|日式烧肉|开元路75号|30.247600,120.162311|0571-88078207;19957139428||4.7|2018
B0LRYKV40L|姜胖胖韩式自助烤肉(庆春银泰店)|上城区|自助烤肉|景昙路18-26号银泰百货6层|30.260025,120.204868|18157138062|厚切五花、部队锅、韩式风干肠、羊排|4.6|2025-11-30
B0FFK7E29G|韩宫宴炭火烤肉(西湖银泰店)|上城区|韩式烤肉|延安路98号西湖银泰五楼506|30.244518,120.165099|0571-87002727|牛肉、芝士年糕||2022
B0L335AFVE|喜牛吉烤肉·和牛放题(501城市广场店)|上城区|日式烧肉|景昙路9号西子国际中心一层101-10|30.259442,120.203649|19012830180|||
B0GD0A8K79|椒炉·鲜切自助烤肉(临安店)|临安区|自助烤肉|城中街300号钱王财富中心F2|30.231209,119.722160||||2022
B0JBYBR8IT|山海盟海鲜烤肉自助餐厅(中大银泰店)|拱墅区|自助烤肉|石祥路138号中大银泰城F2 L216/L216b|30.327127,120.175367|0571-85175628|鲍鱼、甜虾、鲜榨果汁||2023
B0KA7M5L8N|熊福烤肉无限放题(湖滨88店)|上城区|自助烤肉|湖滨88负一楼|||||
B0H37XEM01|西塔老太太泥炉烤肉(杭州首店)|上城区|泥炉烤肉|长生路25、26号／延安路302、302-1号103、104室|30.257179,120.164409|18172739071|||
B0FFJD46CB|韩宫宴炭火烤肉(临平银泰城店)|临平区|韩式烤肉|世纪大道西1号临平银泰城4楼404|30.404795,120.302612|0571-86155083|||
B0H095KYGE|肉本家·炭烤肉(下沙宝龙店)|钱塘区|韩式烤肉|25号大街与学林街交叉口南30米路东，宝龙广场2期31幢106|30.313562,120.382001|0571-81111190|拌饭、小菜||2022
B0I67CR9SQ|本逸·篹·和牛烧肉(黄龙店)|西湖区|日式烧肉|杭大路2号黄龙饭店西门一楼|30.267073,120.142170|19357257298|||2022
B0L0L5A37I|牛小新烧肉·和牛放题(西溪天街店)|西湖区|日式烧肉|余杭塘路1001号龙湖杭州西溪天街6层|30.293396,120.069116|0571-88235502|||
B0I0NR6N5M|东京烧肉Itimaru(屏风街店)|拱墅区|日式烧肉|屏风街29号九鼎·名仕顿商务楼F2|30.266982,120.169150|0571-86808926|蒜香黄油横膈膜|4.82|2025
B0FFMEP2N1|牛一族泥炉碳火烤肉(浙大紫金港店)|西湖区|泥炉烤肉|紫荆花北路浙港国际2号楼130号|30.309001,120.092070|18857133266||4.2|2022
B0K23A0W1A|韩宫宴烤肉(杭州萧山银泰店)|萧山区|韩式烤肉|通惠南路667号银泰百货F5 523M|30.144475,120.286375|0571-82122293|南瓜粥||2022
B0L6RKOORY|夜肆·和牛烧肉料理(奥体店)|萧山区|日式烧肉|嘉润公馆7幢2单元1层104号|30.236619,120.234869|18857861679|眼肉心、板腱||2025-02-26
B0FFGH7O98|蒙城羊肉汤·烧烤(闲林西路店)|余杭区|中式烧烤|闲林西路加油站对面15-8号|30.227210,119.980650|18758276130|||
B0GK1CYH6J|新疆和田美味羊肉烧烤(怡丰城店)|临平区|新疆烧烤|迎宾路怡丰城|30.367046,120.296240|18194956128|||
B0H10UWDH1|夜航烧烤|临平区|中式烧烤|藕花洲大街西段580号|30.393689,120.253072|13611889919|脆皮卤鸽||2021-09-05
B0LGJNHXES|肉士家自助烤肉(义桥星天地店)|萧山区|自助烤肉|义桥星天地南门旁|30.069299,120.202834|18906525699|||
B0H391WSLV|芝小官毛肚火锅烤肉自助(加州阳光·开元广场店)|萧山区|自助烤肉|金城路333号加州阳光·开元广场F3 3034|30.182776,120.252754|0571-83389889;17328865118|||
B0JG3M0UWI|大渔农特色烤鱼·烧烤·小龙虾(崇贤佳源名城店)|临平区|复合烤肉|崇贤街道佳源名城10-60|30.380690,120.174191|15158179135|||
B0K33A04HL|东北老徐烧烤(永宁路店)|临平区|东北烧烤|运河街道永宁路28号|30.467252,120.309423|13867142089|||
B0FFFA7Z3U|明洞世家韩国料理烤肉(萧山工人路店)|萧山区|韩式烤肉|工人路938号|30.180363,120.260943|0571-83507200||4.6|2018
B0JDU5MU6U|金玉东北烧烤·东北菜|余杭区|东北烧烤|宝橙广场22幢-11号|30.283495,120.030407|15765314888|烤蚬子||2023
B0FFMEMGBB|我们家私房烧烤东北菜(未来科技城店)|余杭区|东北烧烤|龙潭路1326号利尔达物联网科技园5幢102室|30.276170,119.991048|13093709775|||
B0LKV54Y55|虹姐正宗东北烧烤|临平区|东北烧烤|振兴西路126-42号(万达广场金街)|30.432762,120.283649|15067121073|||
B0IR2S31HD|西塔老太太泥炉烤肉(萧山万象汇店)|萧山区|泥炉烤肉|金城路927号万象汇|30.182052,120.268521|0571-82706588|||2022
B0HRFX3F67|小胡子音乐餐吧·炒菜·烧烤|余杭区|复合烤肉|良渚街道逸盛路123号1层|30.378665,120.110806||||2022
B0LRUODMW4|串哥东北特色烧烤|临平区|东北烧烤|顺风路196号|30.442587,120.271101|15657125517|||
B0IUU1BUC4|137烧烤龙虾烤鱼·新疆羊肉串(南大街店)|临平区|中式烧烤|南大街137号|30.411624,120.306919|13588702980||4.3|
B0I23U12TP|新疆和田烧烤(塘塍街店)|临安区|新疆烧烤|青山湖街道星悦城2幢111|30.264073,119.821882|13063332444|玉米串、牛肚串||2024
B0J2LHZ9OG|炭火匠人烧烤+龙虾+江湖菜|临安区|中式烧烤|沙树路21幢3号103-104门面|30.229919,119.712367|15355052529|烤年糕、土豆片、郡肝||2024-10
B0KKXS4STM|炭鲜家东北烧烤|临安区|东北烧烤|湍口镇新大街51号|30.042764,119.164516||||
B0FFG976J0|阿碳烧烤(桐庐高铁站格林豪泰商务酒店店)|桐庐县|中式烧烤|下杭路与瑶琳路交叉口东80米|29.801786,119.697971|15888850771||4.7|2021
B0FFIB9P5V|姚记烧烤|桐庐县|中式烧烤|江南镇集市路215号|29.865516,119.769166|18905896027|糖醋里脊、酱爆螺蛳、酱爆茄子||2024
B0M6TR6BIP|新疆兄弟烤羊肉烧烤店|桐庐县|新疆烧烤|大阜山居西南门西南100米|29.808975,119.734975|13649948501|||
B0FFKT9OY4|东北朝鲜族烧烤|临安区|东北烧烤|西林街与农林大路交叉口西60米|30.246886,119.727840|13685743361|辣白菜炒饭、肥牛拌饭||2024
B0JG9P2ANU|串哥烧烤(富阳东桥路点)|富阳区|中式烧烤|东桥路与二号路交叉口西南260米|30.066946,120.068708|13136153328|||2024
B0IR0CS92O|小杨炭烤烧烤海鲜火锅炒菜|富阳区|复合烤肉|银湖街道九龙大道美食街187号|30.145173,119.970997|15267464289|辣炒花甲、螺蛳||2024-11-18
B0J2MDX1HW|刘老根·东北烧烤酒场(闻涛观潮店)|滨江区|东北烧烤|闻涛路1852号-2-3商铺|30.209503,120.198435|19033987899|||2023
B0FFHBHJDK|鲁拉拉烧烤(桥南店)|建德市|中式烧烤|法院路22-1号附近|29.461407,119.285592|13868125830;17757104086|千页豆腐、骨肉相连、蛋炒饭||2024-10-21
B0LU97D0UJ|双人徐平价大排档·炒菜·烧烤·龙虾(新安江店)|建德市|复合烤肉|新安江街道广兴北路21号|29.483383,119.290097|15925636263|||
B0HAVA9Q62|汉巴味德(杭州大悦城店)|拱墅区|巴西烤肉|隐秀路1号大悦城购物中心L6-07B|30.301514,120.130959|0571-86937676|牛舌、铁板虾|4.74|2025
B0H0BUY6WX|木屋烧烤(拱墅胜利河店)|拱墅区|中式烧烤|霞湾巷71号1层108室|30.297011,120.152370|0571-85356959||4.4|2022
B0IA15UZB2|新疆阿布来提羊肉烧烤店|富阳区|新疆烧烤|松溪村182号|29.999512,119.752582|15858818110;18606671111|羊肉串、烤大鱿鱼||2024-10-30
B0K02DYK2H|东北烧烤大油边银湖店|富阳区|东北烧烤|九龙大道163号|30.144990,119.972782|15504370721|||
B0L3JHDE4T|好久不见烧烤·民谣酒馆(富阳店)|富阳区|中式烧烤|富春街道秦望商业中心S3-1006|30.039037,119.940484||||
B0LKBUTG6O|小邵东北烧烤家常菜|富阳区|东北烧烤|恩波大道1166号|||||
B0FFI1AC4B|三哥烧烤炒菜(大桥南路店)|富阳区|中式烧烤|大桥南路190-17-18号|30.025756,119.978580|18758858079|||2021-01-11
B0IDVAT8DR|过江烤鱼·农家菜·烧烤小海鲜(东望大厦店)|富阳区|复合烤肉|恩波大道888号金门东望大厦F1|30.067947,119.947159|18758565100|||2023-10-01
B0FFJLU9JE|牛表妹烤肉(杭州旗舰店)|钱塘区|中式烤肉|下沙街道学林街1253号|30.315273,120.334545|13325913432|||2020-08-09
B0HB3G7ZHC|鸟易·炭火烧鸟(杭州滨江店)|滨江区|日式烧鸟|西兴街道闻涛路华联·星光大道二期302室|30.212425,120.205675|15384080314|||2022-12-07
B0LDGMAIDW|久旦鲜串烧鸟(杭州大悦城店)|拱墅区|日式烧鸟|悦街E幢162号|30.300034,120.129734|13758212870;15658805560|||
B0KAOC3VSZ|三个蒙古大叔烤羊肉串(杭州临平inPARK店)|临平区|中式烧烤|南苑街道汀兰街232号3幢A区L1层L1007室|30.388987,120.294265|19106519890|||2024-05-31
B0M63U94FS|四季三食东北烧烤|上城区|东北烧烤|红普路与格畈家园七号路交叉口西160米|||||
B0FFKFVGKY|李记烧烤龙虾万州烤鱼|萧山区|复合烤肉|新街街道盛中村10组50号|||||
'''

def add(name,district,cat,address,source,*,id=None,coords=None,phone='',dishes='',score=None,date='',confidence='地图定位',history=False,price=None,hours='',note='',kind='门店',src_title='高德地图·公开地点页',extra=None):
    pid=id or 'hz-'+hashlib.sha1((name+address).encode()).hexdigest()[:10]
    rank='待评'
    if score is not None:
        rank='夯' if score>=4.8 else '顶级' if score>=4.6 else '人上人' if score>=4.4 else 'NPC' if score>=4 else '待评'
    desc=note or (('资料里提到'+dishes+'。菜品与供应以到店为准。') if dishes else '公开资料确认店名与位置；未查到足够的招牌菜资料，不凭同类店补写菜单。')
    if not note and cat=='日式烧肉' and '放题' in name:
        desc='店名标示和牛放题路线；套餐档位、肉品等级与限时规则须向该分店确认。'+(('资料提到'+dishes+'。') if dishes else '')
    sources=[{'title':src_title,'url':source,'date':date or '页面未注明资料更新时间','type':confidence,'fields':['店名','地址']+(['坐标'] if coords else []) + (['电话'] if phone else [])+(['菜品线索'] if dishes else []),'retrievedAt':DATE}]
    if extra: sources+=extra
    places.append(dict(id=pid,name=name,district=district,category=cat,address=address,coordinates=coords,phone=phone,dishes=[d.strip() for d in dishes.split('、') if d.strip()],description=desc,score=score,scoreSource='高德公开页' if score is not None else None,scoreNote='样本量与评分更新时间未完整披露，不能等同实吃结论。' if score is not None else '',tier=rank,rankReason=(f'可见高德分数 {score:g}/5，按本页公开阈值初筛。不是官方全城名次。' if score is not None and score>=4 else '缺少可比较的公开口碑证据，暂不强行定档。'),price=price,priceNote='来源参考人均；资料未注明价格采集日期，非当前报价。' if price is not None else '未核实人均，不推测价格。',hours=hours,hoursNote='来源营业时段，非实时营业状态。' if hours else '未核实营业时段。',confidence=confidence,history=history,evidenceDate=date,kind=kind,status='营业未核实',sources=sources,checkedAt=DATE,street=False,featureTag=cat))

for line in raw.strip().splitlines():
    cols=line.split('|'); assert len(cols)==10,(len(cols),line)
    pid,name,district,cat,address,coord,phone,dishes,score,date=cols
    latlng=list(map(float,coord.split(','))) if coord else None
    add(name,district,cat,address,'https://www.amap.com/place/'+pid,id=pid,coords=latlng,phone=phone,dishes=dishes,score=float(score) if score else None,date=date)
# Secondary directory records. Prices/hours intentionally preserved as historical reference only.
secondary='''
1644503|ASANSHAOKAO阿三烧烤(万塘汇店)|西湖区|中式烧烤|万塘路262号6幢南楼1层1006|17767063663|鸡大长腿、小里脊、掌中宝、小鱿鱼、牛油、蒜蓉茄子|周一至周四15:00–次日02:00；周五至周日15:00–次日03:00
1604173|AJIYA味屋日式烧肉(滨江天街店)|滨江区|日式烧肉|江南大道龙湖杭州滨江天街6楼|0571-87153567;17757197025|横膈膜、特选牛小排、厚切牛舌、葱鸡蛋饭|工作日11:00–15:00、17:00–22:00；周末11:00–14:30、17:00–22:00
1590025|九田家黑牛烤肉料理(西溪银泰城店)|西湖区|日式烧肉|崇仁路西溪银泰B馆4楼|0571-87613127;13136101962|黑牛肋条、牡蛎肉、调味猪五花、锡盟羊排、冷面|11:00–14:30、16:30–21:30
1209841|御牛道日式料理炭火烤肉(滨江宝龙店)|滨江区|日式烧肉|滨盛路3867号宝龙城市广场5F-012|0571-85291178;17357152959|雪花中落小排、厚切牛舌、和牛四点拼盘、安格斯横膈膜|11:00–13:30、16:30–21:30
1670551|闻老头·菊花炭烤肉(文一路店)|西湖区|中式烤肉|文一路300号|18072896675;0571-86703095|鲜切瘦牛、炭黑牛五花、厚切五花、秘制猪排、冻梨菊花酒酿|工作日11:00–14:00、16:00–24:00；周末11:00–24:00
1649118|木浦喜肉堂·韩式烤肉(滨江天街店)|滨江区|韩式烤肉|天街铂金岛二楼1-218|0571-86800127|熟成黑猪五花、梅花肉、猪颈肉、鱼饼芝士炒年糕|11:30–14:30、16:30–21:30
1354584|御牛道日式料理炭火烤肉(黄龙恒励大厦店)|西湖区|日式烧肉|黄龙路5号黄龙恒励大厦一层A2座|0571-85333033;18969022910|特上牛小排、雪花中落小排、玫瑰牛舌、牛尾汤|11:00–13:30、16:30–21:30
'''
for row in secondary.strip().splitlines():
    sid,name,dist,cat,addr,tel,dishes,hours=row.split('|')
    add(name,dist,cat,addr,'https://www.zaoseo.com/place/'+sid,phone=tel,dishes=dishes,hours=hours,confidence='名录资料',src_title='找查网·餐厅目录')

add('阿三烧烤(胜利河店)','拱墅区','中式烧烤','胜利河霞湾巷216号','https://hz.bendibao.com/wangdian/dian/3965339.shtm',hours='16:00–次日03:00',confidence='名录资料',src_title='杭州本地宝·网点目录')
add('东京烧肉(滨江天街店)','滨江区','日式烧肉','江汉路1515号龙湖杭州滨江天街1F-27a至1F-28b','https://maps.apple.com/place?auid=1118897824019327&lsp=57879',price=183,hours='11:30–14:00、17:00–次日00:30',src_title='Apple Maps·商户信息',note='资料标示滨江天街一层外围店。与屏风街Itimaru分别建档，不把分店口碑混算。')
add('客串烧烤(千岛湖镇核心区域店)','淳安县','中式烧烤','千岛湖镇22里村农居点水上客栈91号（原地址转写，需二次核对）','https://maps.apple.com/place?auid=1118551951244503&lsp=57879',phone='15224079077',hours='16:00–23:30',src_title='Apple Maps·商户信息',note='千岛湖镇的烧烤门店线索。来源地址为英文转写，出发前请电话核对准确门牌。')
add('一二3鲜货烧烤铺(千岛湖店)','淳安县','中式烧烤','杜鹃路25-2号','https://maps.apple.com/place?auid=1118807644981902&lsp=57879',phone='13616534143',price=19,hours='17:00–次日03:00',src_title='Apple Maps·商户信息',note='地图页标示烧烤、户外座位与宠物友好。页面人均19元口径不详，仅作参考；座位和携宠规则请先问店家。')
add('六丁火烤肉(杭州首店)','萧山区','中式烤肉','钱江世纪公园A区14幢13单元','https://hk.trip.com/moments/poi-city-149809465/',dishes='九宫格烤肉、牛肋条、战斧羊排',hours='15:00–次日01:00',confidence='游记线索',src_title='Trip.com·用户游记',note='游记提到九宫格选肉与樱花主题布置。定位为主题烤肉线索，不以拍照氛围推断食材品质。')
add('破路边烧烤工厂(临平inPARK店)','临平区','中式烧烤','临平银泰inPARK（汀兰街与望梅路交叉口西北一带，具体门牌待核）','https://fashion.hangzhou.com.cn/content/2025-05/09/content_8991067.htm',date='2025-05-09',confidence='报道线索',src_title='杭州网·临平银泰inPARK周年报道',note='2025年报道确认引入该店。是街区里的烧烤餐饮品牌，并非因为名字里有“路边”就被算成流动摊。')

# Legacy street-food directories. Deliberately not treated as 2026 real-time listings.
legacy='''
https://www.cityhui.com/shop/19071.html|撸一手(皇后公园店)|拱墅区|中式烧烤|武林路277号皇后公园二楼|100|0571-88098003|17:00–次日04:00|
https://www.cnpp100.com/shop/19073.html|串哥烧烤(武林巷店)|拱墅区|中式烧烤|武林巷503号(近莫干山路易盛大厦)|86|15356683383|18:30–次日02:00|五花肉
https://www.cnpp100.com/shop/19074.html|我们家私房纸包鱼&烧烤(佑昌巷店)|拱墅区|复合烤肉|莫干山路949号佳源银座佑昌巷46号|61|15258878066;15258836647|17:00–次日02:00|纸包鱼
https://www.cnpp100.com/shop/19075.html|大陈海鲜烧烤|拱墅区|中式烧烤|武林路163号西湖D11食尚城1层|60|15372425287;15372023747|11:00–次日03:00|羊肉串、海鲜烧烤
https://www.cityhui.com/shop/19076.html|清雅斋清真饭庄|上城区|新疆烧烤|凯旋路39号(采荷二小附近)|92|18072713520|09:00–次日02:00|羊肉串
https://www.cityhui.com/shop/19079.html|新凯旋郑燕烧烤(上塘路店)|拱墅区|中式烧烤|上塘路308号(浙工大西门)|68|0571-81805536|16:00–次日03:30|羊肉串
https://www.cnpp100.com/shop/19080.html|西北人家·羊坝头特色烧烤|上城区|新疆烧烤|中山中路257号|58|18072812233|09:30–24:00|羊肉串
https://www.cityhui.com/shop/19081.html|王记金图门串烤|拱墅区|中式烧烤|百井坊巷101号|79|13857195063|17:00–次日02:00|自动旋转串烤
https://www.cityhui.com/shop/19082.html|威武羊肉烧烤|西湖区|中式烧烤|文二路334号富丽科技大厦A座1楼|91|0571-88862635|15:00–次日03:00|羊肉烧烤
'''
for row in legacy.strip().splitlines():
    url,name,dist,cat,addr,price,tel,hours,dishes=row.split('|')
    add(name,dist,cat,addr,url,price=int(price),phone=tel,hours=hours,dishes=dishes,confidence='历史线索',history=True,src_title='城市惠／CNPP100·历史餐饮目录',note=('目录提到'+dishes+'。' if dishes else '武林片区的烧烤旧店线索。')+'页面内容存在历史地址与旧价格，尚未确认该地址继续营业。')

# Compact facts from the same dated local press report; no copied review prose.
press_url='https://news.qq.com/rain/a/20200826A0AKQ000'
old='''
李不管把把烧|拱墅区|中式烧烤|百井坊巷24号|猪鼻筋、把把烧
木屋烧烤(武林路店)|拱墅区|中式烧烤|武林路9号|生蚝、羔羊串
老杨小黄鱼|余杭区|中式烧烤|向往街368号乐时城一楼|烤小黄鱼
深夜好食堂|西湖区|中式烧烤|文三路星光城B座一层|羊排、鸡胗
洪涛烤肉|拱墅区|齐市烤肉|上塘路1035号|牛肉、酸菜
新疆兄弟(德胜路点)|拱墅区|新疆烧烤|德胜路3号|羊肉串、架子肉
三肥两瘦(滨江宝龙点)|滨江区|中式烧烤|江南大道宝龙广场外围一层|厚切五花
蛮串(闻涛路点)|滨江区|中式烧烤|科技馆街1058号天瑀蒙马街一层110|羊肉串、牛奶鸡蛋醪糟
新凯旋烧烤(东站西子国际点)|上城区|中式烧烤|和兴路东站西子国际大厦1幢|羊肉串、羊骨汤
'''
for row in old.strip().splitlines():
    name,dist,cat,addr,dishes=row.split('|')
    add(name,dist,cat,addr,press_url,dishes=dishes,date='2020-08-26',confidence='历史线索',history=True,src_title='钱江晚报／潮新闻·2020烧烤报道',note='2020年当地报道收录；保留旧址与品类线索，不表示当前仍在原址营业。')

ranking='https://ranks.amap.com/ranking/烧烤店/杭州市/白领'
rank_add='''
木屋烧烤(江干天虹店)|上城区|中式烧烤|凤起东路205号|4.8
鹤之乡·齐齐哈尔烤肉(秋涛路店)|上城区|齐市烤肉|秋涛路秋涛发展大厦B座1层248-1|4.7
头牌鹤岗小串(天虹店)|上城区|东北烧烤|新塘路108号天虹购物广场B座负一层|4.5
忽然之间·露营烧烤·日咖夜酒·音乐驻唱|滨江区|中式烧烤|奥体中心莲荷里A区20|4.5
凯旋烧烤(凯旋路)|上城区|中式烧烤|凯旋路69号|4.5
台客熊烧鸟(庆谐路店)|上城区|日式烧鸟|庆谐路26号底商|4.4
木可记烤肉火锅(双菱路总店)|上城区|复合烤肉|双菱路137号|4.0
'''
for row in rank_add.strip().splitlines():
    name,dist,cat,addr,score=row.split('|')
    add(name,dist,cat,addr,ranking,score=float(score),src_title='高德地图·烧烤店白领推荐榜',note='高德垂类榜提供了这家分店的地址与评分。该榜仅为其特定人群推荐，不是杭州全城穷尽榜单。')

add('平炼路共富市集·东北烧烤摊（报道未披露招牌）','拱墅区','东北烧烤','康桥街道平炼路中央景观大道共富市集，具体摊位号未披露','https://hznews.hangzhou.com.cn/chengshi/content/2025-06/22/content_9022405.htm',date='2025-06-22',confidence='报道线索',kind='摊位',src_title='都市快报／杭州网·平炼路共富市集',note='报道明确记载一处东北烧烤摊，但没有披露招牌、摊位号、电话或出摊时段。这里使用描述性名称，不虚构店名；当前是否继续出摊未知。')

# Extra evidence and careful corrections.
byid={p['id']:p for p in places}
def patch(pid,**kw): byid[pid].update(kw)
def extra(pid,title,url,date,fields): byid[pid]['sources'].append(dict(title=title,url=url,date=date,type='交叉资料',fields=fields,retrievedAt=DATE))
extra('B0HUOZDVVM','杭州网·2025高德国庆TOP100报道','https://ori.hangzhou.com.cn/ornews/content/2025-09/29/content_9094308.htm','2025-09-29',['2025榜单表现'])
extra('B0HUOZDVVM','高德·杭州2025榜单','https://www.amap.com/ranking/hangzhou','2025',['特色菜线索','榜单'])
patch('B0HUOZDVVM',description='公开榜单与地方媒体均指向这家浙大总店。榜单提到雪花牛肉、厚切五花与代烤；不把品牌热度外推到所有分店。',rankReason='高德公开分数4.9；另有2025年杭州网榜单报道交叉支持。仅是资料优先级，不是实吃保证。',featureTag='多源交叉 · 韩式炭火')
extra('B0I0NR6N5M','高德·拱墅区2025必吃美食','https://www.amap.com/ranking/hangzhou/food/330105','2025',['全年综合分4.82','蒜香黄油横膈膜','代烤线索'])
patch('B0I0NR6N5M',scoreSource='高德2025榜单综合分',description='屏风街二楼的日式烧肉。2025高德榜单提到蒜香黄油横膈膜与代烤；门店定位已用独立POI交叉核对。',featureTag='横膈膜 · 日式烧肉')
extra('B0HAVA9Q62','高德·拱墅区2025必吃美食','https://www.amap.com/ranking/hangzhou/food/330105','2025',['全年综合分4.74','巴西烤肉自助'])
patch('B0HAVA9Q62',scoreSource='高德2025榜单综合分',description='巴西烤肉自助路线，区别于桌上自己烤的韩式与日式店。榜单提到现场切肉；价格与当日出品请咨询该分店。')
extra('B0FFLAQI13','钱江晚报／潮新闻·2020烧烤报道',press_url,'2020-08-26',['分店地址','菜品线索'])
patch('B0FFLAQI13',description='高沙商业街的具体分店，地图与2020本地报道地址相符。报道提到烤茄子、扇贝、奶黄包，当前供应须确认。',featureTag='高沙夜宵 · 中式串烤')
patch('B0IUTS4JWH',description='页面汇总分与所示单条评价存在明显差异，无法确认样本与口径。保留地址，不以这个分数直接判“拉”。',rankReason='汇总分1.7与页面展示评价不一致；样本不明，暂停定档。',tier='待评')
patch('B0FFFA7Z3U',tier='待评',rankReason='地点页的分类与餐厅名称存在不一致，先核对门店，不按单个分数定档。',description='地图中能查到工人路938号，但地点分类与餐厅名称有出入。建议先致电确认店名与营业情况。')
patch('B0K02DYK2H',status='来源标注暂停营业',tier='待评',description='地点页名称包含“暂停营业”。保留档案用于避免按旧地址白跑；未电话复核，也不将停业状态当作口味评价。',rankReason='来源标注暂停营业，不进入默认推荐候选。')
patch('B0I67CR9SQ',description='黄龙饭店西门一层的和牛烧肉线索。2022年食客记录提到暗调空间与庆生布置；本次没有核实当前套餐与肉品等级。',featureTag='黄龙 · 约会场景线索')
patch('B0L6RKOORY',description='奥体片区的日式烧肉门店。2025年食客记录提到眼肉心、板腱与大阪居酒屋式布置，适合作为风格鲜明的候选。',featureTag='眼肉心 · 奥体片区')
patch('B0GKY1LDQS',description='沈塘桥路上的小型烤肉门店。2022年记录提到东北背景与小店氛围；尚无足够样本支持当前口碑定档。')
patch('B0J2MDX1HW',description='闻涛路的东北烧烤酒场。2023年食客记录提到现场音乐；演出、包场与噪声环境请先问店家。')
patch('B0KAOC3VSZ',description='临平inPARK内的烤羊肉串门店。所见评论存在跨分店描述，不据此确认本店肉源与烤制方式。')
patch('B0HRFX3F67',description='店名显示音乐餐吧、炒菜与烧烤并行。现场演出、菜品与价位未获得足够资料，暂作位置候选。')
patch('B0JAGSARXL',description='铜锅涮肉与烤串的复合型门店，不属于纯烤肉店；在筛选中可单独排除复合餐饮。')
patch('B0K6C72LQD',description='店名标示鸡汤火锅与云南烤肉两条路线；记录也提到空间氛围。暂未核实烤肉套餐，属于复合餐饮。')
# Name collisions are never auto-merged or assumed to be a chain.
for p in places:
    if p['id'] in ('B0JG9P2ANU','B0LRUODMW4'):
        p['description']='与武林巷“串哥烧烤”分开建档；同名不代表同一老板或连锁。当前仅有位置线索，招牌菜与口碑待核实。'
    if p['name'].startswith('串哥烧烤(武林巷'):
        p['description']='旧目录记载由路边摊发展而来，特色指向五花肉。武林巷地址与参考价均待复核；不同区的同名店不混作分店。'
        p['featureTag']='摊起家 · 五花肉线索'
    if p['name']=='老杨小黄鱼':
        p['sources'].append(dict(title='什么值得买·2019年个人探店',url='https://post.smzdm.com/p/adwlnpkz/',date='2019-06-26',type='历史游记',fields=['烤小黄鱼','历史迁址'],retrievedAt=DATE))
        p['description']='两份旧资料均指向乐时城地址，核心线索是烤小黄鱼。存在多次迁址历史，不能把旧地址当成当下营业确认。'
        p['featureTag']='烤小黄鱼 · 历史名店'
    if p['category'] in ['中式烧烤','东北烧烤','新疆烧烤','齐市烤肉','中式烤肉'] and not any(x in p['address'] for x in ['广场','天街','银泰','大悦城','万象','公园','inPARK','购物中心']):
        p['street']=True
    if p['kind']=='摊位': p['street']=True
    if p['history']: p['tier']='待评';p['rankReason']='历史地址/旧价尚未复核，不以历史知名度直接评级。'
    p['addressPrecision']='摊位号未披露' if p['kind']=='摊位' else ('门牌/楼层待核' if any(x in p['address'] for x in ['一带','附近','一幢','原地址转写']) else '来源地址')
    p['scene'] = '自助聚餐' if ('自助' in p['category'] or '放题' in p['name'] or p['category']=='巴西烤肉') else '烧肉聚会' if p['category'] in ['日式烧肉','韩式烤肉','泥炉烤肉'] else '夜宵串场' if p['street'] else '风味探索'

# Area leads have their own count. They are NOT counted as restaurants.
areas=[
 {'name':'平炼路共富市集','district':'拱墅区','address':'康桥街道平炼路中央景观大道','note':'2025年本地报道记录有东北烧烤摊；未得到完整摊商清单，不虚构每个摊位。','source':'https://hznews.hangzhou.com.cn/chengshi/content/2025-06/22/content_9022405.htm','date':'2025-06-22'},
 {'name':'富阳文教路夜宵街','district':'富阳区','address':'文教路沿线','note':'2023年资料记录夜宵与烧烤业态。这里只是扫街起点，不代表整条街当前商户已经收齐。','source':'https://zhejiang.chinatax.gov.cn/art/2023/8/31/art_13230_597596.html','date':'2023-08-31'},
 {'name':'高沙商业街','district':'钱塘区','address':'学林街高沙商业街一带','note':'已收录阿三高沙店、牛表妹等具体门店；流动摊位的当日位置不在本次可核实范围。','source':'https://www.amap.com/place/B0FFLAQI13','date':'来源未注明'},
 {'name':'胜利河美食街','district':'拱墅区','address':'霞湾巷沿线','note':'木屋与阿三分别建档；沿街其他烧烤店仍有采集缺口。','source':'https://www.amap.com/place/B0H0BUY6WX','date':'来源未注明'}
]
meta={
 'title':'炙·杭州｜全城烤肉图鉴','version':'1.0-public-research','researchedAt':DATE,
 'scope':'杭州市13个区县市的公开资料采集；不是完整商户注册库，不保证无遗漏。',
 'liveOperationsVerified':False,'tastedByAuthor':False,'sourceMethod':'公开网页与搜索索引检索、分店级整理、按地点标识和地址去重；未绕过登录、验证码或平台限制。',
 'tierMethod':'公开口碑初筛：高德可见分数≥4.8为夯，≥4.6为顶级，≥4.4为人上人，≥4.0为NPC；不同高德页面口径也可能不同。缺样本、历史资料、分数矛盾或状态异常列待评。本次无充分证据分配拉；我的实吃榜可由用户自评。',
 'coordinatesMethod':'只使用已见公开POI坐标，不给地址不详店编坐标；图谱为经纬度散点示意，不作底图或导航。',
 'limitations':['未获得大众点评、美团及地图平台的杭州全量商户库。','部分来源与菜品评价较旧；抓取日期不等于营业确认日期。','没有电话核验、实地吃访、实时排队或实时价格。','街边小店标签按地址与报道作候选归类，不等于已实地确认门面布局或出摊形式。','摊位招牌/编号未公开的，用明确描述性名称，不冒充正式店名。','未核实肉品产地与等级，不沿用营销页的无证认证。'],
 'districts':['上城区','西湖区','拱墅区','滨江区','萧山区','余杭区','临平区','钱塘区','富阳区','临安区','桐庐县','淳安县','建德市']}
ids=[p['id'] for p in places]; assert len(ids)==len(set(ids))
assert all(p['sources'] and p['address'] and p['name'] for p in places)
meta['counts']={'places':len(places),'shops':sum(p['kind']=='门店' for p in places),'stalls':sum(p['kind']=='摊位' for p in places),'coordinatePoints':sum(bool(p['coordinates']) for p in places),'districts':len(set(p['district'] for p in places)),'sourceURLs':len({s['url'] for p in places for s in p['sources']}),'historical':sum(p['history'] for p in places),'referencePrices':sum(p['price'] is not None for p in places),'menuClues':sum(bool(p['dishes']) for p in places),'areaLeads':len(areas),'suspended':sum(p['status']!='营业未核实' for p in places)}
bundle={'meta':meta,'places':places,'areas':areas}
(ROOT/'data'/'places.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data'/'sources.json').write_text(json.dumps([{'placeId':p['id'],'name':p['name'],'sources':p['sources']} for p in places],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta['counts'],ensure_ascii=False));print(collections.Counter(p['tier'] for p in places));print(collections.Counter(p['district'] for p in places))
