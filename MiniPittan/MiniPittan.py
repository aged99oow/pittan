#
# MiniPittan.py 2022/9/15
#
import copy
import random
import csv
import pyxel
import mkfont

BOARD_X, BOARD_Y = 17, 23
BOARD_WIDTH, BOARD_HEIGHT = 13, 11
MSG_X, MSG_Y = 2, 2
STAND_X, STAND_Y = 2, 23
STARTBTN_X, STARTBTN_Y = 2, 143
STATUS_TITLE       = 110
STATUS_START       = 120
STATUS_SELECT_DROP = 210
STATUS_TOBOARD     = 220
STATUS_JUDGE       = 230
STATUS_TOSTAND     = 240
STATUS_MATCH       = 250
STATUS_HOP         = 260
STATUS_NEW_INHAND  = 270
STATUS_CLEAR_CHECK = 310
STATUS_CLEAR_MSG   = 320
STATUS_CLEAR       = 330
STATUS_CLEAR_HOP   = 340
GRADE1 = '一右雨円王音下火花貝学気九休玉金空月犬見五口校左三山子四糸字耳七車手十出女小上森'+\
         '人水正生青夕石赤千川先早草足村大男竹中虫町天田土二日入年白八百文木本名目立力林六'  # 80字
GRADE2 = '引羽雲園遠何科夏家歌画回会海絵外角楽活間丸岩顔汽記帰弓牛魚京強教近兄形計元言原戸'+\
         '古午後語工公広交光考行高黄合谷国黒今才細作算止市矢姉思紙寺自時室社弱首秋週春書少'+\
         '場色食心新親図数西声星晴切雪船線前組走多太体台地池知茶昼長鳥朝直通弟店点電刀冬当'+\
         '東答頭同道読内南肉馬売買麦半番父風分聞米歩母方北毎妹万明鳴毛門夜野友用曜来里理話'  # 160字
GRADE3 = '悪安暗医委意育員院飲運泳駅央横屋温化荷界開階寒感漢館岸起期客究急級宮球去橋業曲局'+\
         '銀区苦具君係軽血決研県庫湖向幸港号根祭皿仕死使始指歯詩次事持式実写者主守取酒受州'+\
         '拾終習集住重宿所暑助昭消商章勝乗植申身神真深進世整昔全相送想息速族他打対待代第題'+\
         '炭短談着注柱丁帳調追定庭笛鉄転都度投豆島湯登等動童農波配倍箱畑発反坂板皮悲美鼻筆'+\
         '氷表秒病品負部服福物平返勉放味命面問役薬由油有遊予羊洋葉陽様落流旅両緑礼列練路和'  # 200字
GRADE4 = '愛案以衣位囲胃印英栄塩億加果貨課芽改械害街各覚完官管関観願希季紀喜旗器機議求泣救'+\
         '給挙漁共協鏡競極訓軍郡径型景芸欠結建健験固功好候航康告差菜最材昨札刷殺察参産散残'+\
         '士氏史司試児治辞失借種周祝順初松笑唱焼象照賞臣信成省清静席積折節説浅戦選然争倉巣'+\
         '束側続卒孫帯隊達単置仲貯兆腸低底停的典伝徒努灯堂働特得毒熱念敗梅博飯飛費必票標不'+\
         '夫付府副粉兵別辺変便包法望牧末満未脈民無約勇要養浴利陸良料量輪類令冷例歴連老労録'  # 200字
GRADE5 = '圧移因永営衛易益液演応往桜恩可仮価河過賀快解格確額刊幹慣眼基寄規技義逆久旧居許境'+\
         '均禁句群経潔件券険検限現減故個護効厚耕鉱構興講混査再災妻採際在財罪雑酸賛支志枝師'+\
         '資飼示似識質舎謝授修述術準序招承証条状常情織職制性政勢精製税責績接設舌絶銭祖素総'+\
         '造像増則測属率損退貸態団断築張提程適敵統銅導徳独任燃能破犯判版比肥非備俵評貧布婦'+\
         '富武復複仏編弁保墓報豊防貿暴務夢迷綿輸余預容略留領'  # 185字
GRADE6 = '異遺域宇映延沿我灰拡革閣割株干巻看簡危机揮貴疑吸供胸郷勤筋系敬警劇激穴絹権憲源厳'+\
         '己呼誤后孝皇紅降鋼刻穀骨困砂座済裁策冊蚕至私姿視詞誌磁射捨尺若樹収宗就衆従縦縮熟'+\
         '純処署諸除将傷障城蒸針仁垂推寸盛聖誠宣専泉洗染善奏窓創装層操蔵臓存尊宅担探誕段暖'+\
         '値宙忠著庁頂潮賃痛展討党糖届難乳認納脳派拝背肺俳班晩否批秘腹奮並陛閉片補暮宝訪亡'+\
         '忘棒枚幕密盟模訳郵優幼欲翌乱卵覧裏律臨朗論'  # 181字
CHARGROUP = (('数', '一二三四五六七八九十百千'),
             ('人', '口耳手女人足男目王子'),
             ('生物', '貝犬草竹虫林花森'),
             ('自然', '雨空山石川天田夕村町気音月火水木金土日'),
             ('もの', '円玉糸字車文本名校年力白赤青'),
             ('動作', '右下学休見左出小上正生先早大中入立'))
BEGINNER = '春風車内外国立場所長男女王時雨足元気分身体重大声色紙和牛肉親交流出番地面会心配強火事実名前世代理科目役物'
ADBANCED = '集合格言文明日本音楽器用意写真空白夜行進入手記年力作命中間食後半月給水先発見学新年数人生徒歩道草花園芸術'
MIXED    = '車立男女王雨足大出火名目文日本音空白入手年力中月水先見学年人生草花'

SPC = '-'
BOARD_LARGE =  [[ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '']]
BOARD_MID   =  [[ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '',SPC,SPC, '',SPC,SPC,SPC, '',SPC,SPC, '', ''],
                [ '',SPC,SPC,SPC, '',SPC,SPC,SPC, '',SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '',SPC,SPC,SPC, '', '', '',SPC,SPC,SPC, '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', '']]
BOARD_SMALL =  [[ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC, '', '', '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '',SPC,SPC, '',SPC,SPC, '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '', '', '',SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', '']]
BOARD_TINY =   [[ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '',SPC, '',SPC, '',SPC, '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '', '',SPC, '',SPC, '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '', '', '', '', '', '', '', '', '', '', '']]
BOARD_MOUSE =  [[ '', '', '',SPC,SPC, '', '', '',SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC, '', ''],
                [ '',SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC, '',SPC, '',SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC, '', '',SPC, '', '',SPC,SPC, '', ''],
                [ '', '',SPC,SPC, '',SPC,SPC, '',SPC,SPC,SPC, '', ''],
                [ '', '',SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '',SPC,SPC,SPC, '',SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', '']]
BOARD_CROSS =  [[ '', '', '', '', '', '',SPC, '', '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '', '',SPC, '', '', '', '', '', '']]
BOARD_HEART =  [[ '', '', '', '', '', '', '', '', '', '', '', '', ''],
                [ '', '', '',SPC,SPC, '', '', '',SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC, '', ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '', '',SPC, '', '', '', '', '', '']]
BOARD_STAR =   [[ '', '', '', '', '', '',SPC, '', '', '', '', '', ''],
                [ '', '', '', '', '', '',SPC, '', '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '', '',SPC,SPC,SPC,SPC,SPC, '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC, '',SPC,SPC,SPC, '', '', ''],
                [ '', '', '',SPC,SPC, '', '', '',SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC, '', '', '', '', '',SPC,SPC, '', '']]
BOARD_CIRCLE = [[ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '',SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC, '', '', '',SPC,SPC,SPC,SPC, ''],
                [ '',SPC,SPC,SPC,SPC,SPC, '',SPC,SPC,SPC,SPC,SPC, ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', ''],
                [ '', '', '',SPC,SPC,SPC,SPC,SPC,SPC,SPC, '', '', ''],
                [ '', '', '', '', '',SPC,SPC,SPC, '', '', '', '', '']]

class App:
    def restart(self):
        self.bgcol    = random.choice((6,11,14,15))
        self.msgbgcol = random.choice((2,3,4,5))
        self.bdbgcol  = random.choice((2,3,4,5))
        randcol       = random.sample(range(7), 3)
        self.blkcol   = randcol[1]
        self.btncol   = randcol[2]
        self.board = copy.deepcopy(random.choice((BOARD_LARGE, BOARD_MID, BOARD_SMALL, BOARD_TINY, \
                BOARD_MOUSE, BOARD_CROSS, BOARD_HEART, BOARD_STAR, BOARD_CIRCLE)))
        #self.board = copy.deepcopy(BOARD_CROSS)
        self.board_color =  [[self.blkcol for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
        groupset = ''
        self.charset = ''
        for i in random.sample(range(len(CHARGROUP)), random.randint(1,len(CHARGROUP))):
            groupset += CHARGROUP[i][0]+' '
            self.charset += CHARGROUP[i][1]
        self.msg1 = ''
        self.msg2 = ''
        self.msgscrl = 0
        self.in_message('文字セット:'+groupset)
        fixblkptn = random.randrange(3)
        if fixblkptn == 0:  # 縞
            for i in range(0, BOARD_HEIGHT, 2):
                for j in range(0, BOARD_WIDTH, 2):
                    if self.board[i][j] == SPC:
                        self.board[i][j] = random.choice(self.charset)
                        self.board_color[i][j] = randcol[0]
            for i in range(1, BOARD_HEIGHT, 2):
                for j in range(1, BOARD_WIDTH, 2):
                    if self.board[i][j] == SPC:
                        self.board[i][j] = random.choice(self.charset)
                        self.board_color[i][j] = randcol[0]
        elif fixblkptn == 1:  # 縁
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    if self.board[i][j] == SPC:
                        if i == 0 or i == BOARD_HEIGHT-1 or j == 0 or j == BOARD_WIDTH-1:
                            self.board[i][j] = random.choice(self.charset)
                            self.board_color[i][j] = randcol[0]
                        elif self.board[i-1][j] == '' or self.board[i+1][j] == '' or self.board[i][j-1] == '' or self.board[i][j+1] == '':
                            self.board[i][j] = random.choice(self.charset)
                            self.board_color[i][j] = randcol[0]
        else:  # ランダム
            spc_num = 0
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    if self.board[i][j] == SPC:
                        spc_num += 1
            blk_num = spc_num//3
            while blk_num > 0:
                x, y = random.randrange(BOARD_WIDTH), random.randrange(BOARD_HEIGHT)
                if self.board[y][x] == SPC:
                    self.board[y][x] = random.choice(self.charset)
                    self.board_color[y][x] = randcol[0]
                    blk_num -= 1
        self.inhand = []
        for _ in range(8):
                self.inhand.append(random.choice(self.charset))
        self.newinhand = []
        self.newinhand_y = 0
        self.allcandrop = []
        self.select_pos = 0
        self.drop_x, self.drop_y = -1, -1

    def __init__(self):
        pyxel.init(176, 158, title='MiniPittan')
        pyxel.load('assets/MiniPittan.pyxres')
        pyxel.mouse(True)
        with open('jukugo.csv', encoding='utf8', newline='') as f:
            reader = csv.reader(f)
            self.jukugo = {row[0]:row[1] for row in reader}
        self.restart()
        self.status = STATUS_TITLE
        pyxel.run(self.update, self.draw)

    def in_message(self, newmsg, keep=False):
        if keep or self.msg1 == '':
            self.msg1 = newmsg
        elif newmsg:
            self.msgscrl = 7
            self.msg2 = self.msg1
            self.msg1 = newmsg

    def candrop(self):
        ret = []
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.board[i][j] == SPC:
                    if (i > 0 and self.board[i-1][j] and self.board[i-1][j] != SPC) or \
                            (i < BOARD_HEIGHT-1 and self.board[i+1][j] and self.board[i+1][j] != SPC) or \
                            (j > 0 and self.board[i][j-1] and self.board[i][j-1] != SPC) or \
                            (j < BOARD_WIDTH-1 and self.board[i][j+1] and self.board[i][j+1] != SPC):
                        ret.append([j, i])
        return ret

    def judge_jukugo(self, str, start, pos, end):
        pos_msg = []
        for i in range(start, pos+1):
            for j in range(pos, end):
                if i != j:
                    k = ''.join(str[i:j+1])
                    v = self.jukugo.get(k)
                    if v:
                        pos_msg.append([i, j+1, k+':'+v])
        return pos_msg

    def isjudge(self, block):
        row = self.board[self.drop_y][:]
        row[self.drop_x] = block
        for i in range(self.drop_x-1, -1, -1):
            if not row[i] and row[i] != SPC:
                start = i+1
                break
        else:
            start = 0
        for i in range(self.drop_x+1, BOARD_WIDTH):
            if not row[i] and row[i] != SPC:
                end = i
                break
        else:
            end = BOARD_WIDTH
        pos_msg = self.judge_jukugo(row, start, self.drop_x, end)
        self.hop_pos = []
        self.hop_msg = []
        for each1 in pos_msg:
            each_hop = []
            for each2 in range(each1[0], each1[1]):
                each_hop.append([each2, self.drop_y])
            self.hop_pos.append(each_hop)
            self.hop_msg.append(each1[2])
        column = [r[self.drop_x] for r in self.board]
        column[self.drop_y] = block
        for i in range(self.drop_y-1, -1, -1):
            if not column[i] and column[i] != SPC:
                start = i+1
                break
        else:
            start = 0
        for i in range(self.drop_y+1, BOARD_HEIGHT):
            if not column[i] and column[i] != SPC:
                end = i
                break
        else:
            end = BOARD_HEIGHT
        pos_msg = self.judge_jukugo(column, start, self.drop_y, end)
        for each1 in pos_msg:
            each_pop = []
            for each2 in range(each1[0], each1[1]):
                each_pop.append([self.drop_x, each2])
            self.hop_pos.append(each_pop)
            self.hop_msg.append(each1[2])
        return True if self.hop_pos else False

    def update(self):
        if self.msgscrl > 0:
            self.msgscrl -= 1
        
        if self.status == STATUS_TITLE:
            self.status = STATUS_START

        elif self.status == STATUS_START:
            self.allcandrop = self.candrop()
            self.status = STATUS_SELECT_DROP

        elif self.status == STATUS_SELECT_DROP:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):  # RIGHT_BUTTON_UP
                self.select_pos += 1
                if self.select_pos >= len(self.inhand):
                    self.select_pos = 0
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                if 0 <= pyxel.mouse_x-STARTBTN_X < 12 and 0 <= pyxel.mouse_y-STARTBTN_Y < 12:
                    self.restart()
                    self.status = STATUS_TITLE
                    return
                select_x = (pyxel.mouse_x-STAND_X)//12
                select_y = (pyxel.mouse_y-STAND_Y)//12
                if select_x == 0 and 0 <= select_y < len(self.inhand):
                    self.select_pos = select_y
                    return
                select_x = (pyxel.mouse_x-BOARD_X)//12
                select_y = (pyxel.mouse_y-BOARD_Y)//12
                if 0 <= select_x < BOARD_WIDTH and 0 <= select_y < BOARD_HEIGHT:
                    for pos in self.allcandrop:
                        if select_x == pos[0] and select_y == pos[1]:
                            self.drop_x = select_x
                            self.drop_y = select_y
                            self.move_count = 0
                            self.move_x = STAND_X
                            self.move_y = STAND_Y+12*self.select_pos
                            self.status = STATUS_TOBOARD
                            return

        elif self.status == STATUS_TOBOARD:
            MV_CNT = 15
            self.move_count += 1
            if self.move_count <= MV_CNT:
                self.move_x = STAND_X+(BOARD_X+12*self.drop_x-STAND_X)*self.move_count//MV_CNT
                self.move_y = STAND_Y+12*self.select_pos+(BOARD_Y+12*self.drop_y-(STAND_Y+12*self.select_pos))*self.move_count//MV_CNT
            else:
                self.status = STATUS_JUDGE

        elif self.status == STATUS_JUDGE:
            if self.isjudge(self.inhand[self.select_pos]):
                self.board[self.drop_y][self.drop_x] = self.inhand[self.select_pos]
                self.newinhand = self.inhand[self.select_pos+1:]
                self.inhand = self.inhand[:self.select_pos]
                self.newinhand_y = 12
                self.hop_n  = 0
                self.status = STATUS_MATCH
            else:
                pyxel.play(0, 8)
                self.move_count = 0
                self.move_x = BOARD_X+12*self.drop_x
                self.move_y = BOARD_Y+12*self.drop_y
                self.status = STATUS_TOSTAND

        elif self.status == STATUS_TOSTAND:
            MV_CNT = 10
            self.move_count += 1
            if self.move_count <= MV_CNT:
                self.move_x = BOARD_X+12*self.drop_x+(STAND_X-(BOARD_X+12*self.drop_x))*self.move_count//MV_CNT
                self.move_y = BOARD_Y+12*self.drop_y+(STAND_Y+12*self.select_pos-(BOARD_Y+12*self.drop_y))*self.move_count//MV_CNT
            else:
                self.status = STATUS_START

        elif self.status == STATUS_MATCH:
            self.in_message(self.hop_msg[self.hop_n])
            self.hop_y  = 0
            self.hop_dy = -8
            pyxel.play(0, self.hop_n if self.hop_n < 8 else 7)
            self.status = STATUS_HOP

        elif self.status == STATUS_HOP:
            self.hop_y  += self.hop_dy//5
            self.hop_dy += 1
            if self.hop_y > 0:
                self.hop_n += 1
                if self.hop_n < len(self.hop_pos):
                    self.status = STATUS_MATCH
                else:
                    self.status = STATUS_CLEAR_CHECK

        elif self.status == STATUS_CLEAR_CHECK:
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    if self.board[i][j] == SPC:
                        break
                else:
                    continue
                break
            else:
                self.inhandmsg = 'すてえじ★くりあ'
                self.select_pos = -1
                self.allcandrop = []
                self.inhand = []
                self.newinhand_y = 12*(len(self.inhandmsg)-1)
                pyxel.play(0, [4,5,6,7,7,7])
                self.status = STATUS_CLEAR_MSG
                return
            self.status = STATUS_NEW_INHAND

        elif self.status == STATUS_NEW_INHAND:
            self.newinhand_y -= 1
            if self.newinhand_y <= 0: 
                self.newinhand_y = 0
                self.inhand.extend(self.newinhand)
                self.newinhand = []
                self.inhand.append(random.choice(self.charset))
                self.status = STATUS_START

        elif self.status == STATUS_CLEAR_MSG:
            self.newinhand_y -= 2
            self.newinhand = self.inhandmsg[:len(self.inhandmsg)-(self.newinhand_y+11)//12]
            if self.newinhand_y <= 0:
                self.newinhand_y = 0
                self.inhand = self.inhandmsg[:]
                self.newinhand = []
                self.status = STATUS_CLEAR

        elif self.status == STATUS_CLEAR:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                self.restart()
                self.status = STATUS_TITLE
                return
            self.drop_x, self.drop_y = random.randrange(BOARD_WIDTH), random.randrange(BOARD_HEIGHT)
            blk = self.board[self.drop_y][self.drop_x]
            if blk and self.isjudge(blk):
                self.hop_n  = random.randrange(len(self.hop_pos))
                self.in_message(self.hop_msg[self.hop_n])
                self.hop_y  = 0
                self.hop_dy = -8
                self.status = STATUS_CLEAR_HOP

        elif self.status == STATUS_CLEAR_HOP:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                self.restart()
                self.status = STATUS_TITLE
                return
            self.hop_y  += self.hop_dy//5
            self.hop_dy += 1
            if self.hop_y > 0:
                self.status = STATUS_CLEAR

    def draw_board(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.board[i][j]:
                    pyxel.rectb(BOARD_X+12*j  , BOARD_Y+12*i  , 13, 13, 0)
                    pyxel.rect( BOARD_X+12*j+1, BOARD_Y+12*i+1, 11, 11, self.bdbgcol)

    def draw_piece(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                p = self.board[i][j]
                if p and p != SPC:
                    if self.status == STATUS_HOP or self.status == STATUS_CLEAR_HOP:
                        if [j, i] in self.hop_pos[self.hop_n]:
                            pyxel.blt(BOARD_X+1+j*12, BOARD_Y+1+i*12+self.hop_y, 0, self.board_color[i][j]*16, 16, 13, 13, 1)
                            mkfont.text(BOARD_X+3+j*12, BOARD_Y+3+i*12+self.hop_y, p, 7) # 14
                        else:
                            pyxel.blt(BOARD_X+1+j*12, BOARD_Y+1+i*12, 0, self.board_color[i][j]*16, 0, 13, 13, 1)
                            mkfont.text(BOARD_X+3+j*12, BOARD_Y+3+i*12, p, 7)
                    else:
                        pyxel.blt(BOARD_X+1+j*12, BOARD_Y+1+i*12, 0, self.board_color[i][j]*16, 0, 13, 13, 1)
                        mkfont.text(BOARD_X+3+j*12, BOARD_Y+3+i*12, p, 7)

    def draw_message(self):
        pyxel.rectb(MSG_X  , MSG_Y  , 172, 19, 0)
        pyxel.rect( MSG_X+1, MSG_Y+1, 170, 17, self.msgbgcol)
        if self.msgscrl:
            mkfont.text(MSG_X+2, MSG_Y+2+self.msgscrl, self.msg2, 7)
        else:
            mkfont.text(MSG_X+2, MSG_Y+2, self.msg2, 7)
            mkfont.text(MSG_X+2, MSG_Y+10, self.msg1, 7)

    def draw_stand(self):
        pyxel.rectb(STAND_X  , STAND_Y  , 13, 97, 0)
        pyxel.rect( STAND_X+1, STAND_Y+1, 11, 95, self.bdbgcol)

    def draw_inhand(self):
        if self.status == STATUS_CLEAR or self.status == STATUS_CLEAR_HOP:
            col = pyxel.frame_count//5%4
        else:
            col = self.blkcol
        
        for i, blk in enumerate(self.inhand):
            if i == self.select_pos:
                if self.status == STATUS_TOBOARD or self.status == STATUS_JUDGE or self.status == STATUS_TOSTAND:
                    pass
                else:
                    pyxel.blt(STAND_X+1, STAND_Y+1+12*i, 0, self.blkcol*16, 16, 13, 13, 1)
                    mkfont.text(STAND_X+3, STAND_Y+3+12*i, blk, 7)
            else:
                pyxel.blt(STAND_X+1, STAND_Y+1+12*i, 0, col*16, 0, 13, 13, 1)
                mkfont.text(STAND_X+3, STAND_Y+3+12*i, blk, 7)
        
        for i, blk in enumerate(self.newinhand):
                pyxel.blt(STAND_X+1, STAND_Y+1+12*(len(self.inhand)+i)+self.newinhand_y, 0, col*16, 0, 13, 13, 1)
                mkfont.text(STAND_X+3, STAND_Y+3+12*(len(self.inhand)+i)+self.newinhand_y, blk, 7)

    def draw_startbtn(self):
        if 0 <= pyxel.mouse_x-STARTBTN_X < 12 and 0 <= pyxel.mouse_y-STARTBTN_Y < 12:
            pyxel.blt(STARTBTN_X+1, STARTBTN_Y+1, 0, self.btncol*16, 16, 13, 13, 1)
            mkfont.text(STARTBTN_X+3, STARTBTN_Y+3, '始', 7)
        else:
            pyxel.blt(STARTBTN_X+1, STARTBTN_Y+1, 0, self.btncol*16, 0, 13, 13, 1)
            mkfont.text(STARTBTN_X+3, STARTBTN_Y+3, '始', 13)

    def draw_select(self, col=9):
        for i in range(len(self.inhand)):
            pyxel.rect(STAND_X+1, STAND_Y+1+12*i, 15, 15, col)

    def draw_drop(self, col_select=9, col_drop=10):
        for pos in self.allcandrop:
            pyxel.circ(BOARD_X+6+pos[0]*12, BOARD_Y+6+pos[1]*12, 1, col_drop)

    def draw_move(self):
        pyxel.blt(self.move_x+1, self.move_y+1, 0, self.blkcol*16, 16, 13, 13, 1)
        mkfont.text(self.move_x+3, self.move_y+3, self.inhand[self.select_pos], 7)

    def draw(self):
        pyxel.cls(self.bgcol)
        self.draw_message()
        self.draw_board()
        self.draw_stand()
        self.draw_startbtn()
        self.draw_drop()
        self.draw_piece()
        self.draw_inhand()
        if self.status == STATUS_TOBOARD or self.status == STATUS_JUDGE or self.status == STATUS_TOSTAND:
            self.draw_move()

App()