import pyxel


class ship:
    def __init__(self, FW):
        self.field_width = FW
        self.field_length = self.field_width * 2

        self.slength = self.field_length / 20
        self.swidth = self.field_width / 5
        self.sx = self.field_width / 2
        self.sy = self.field_length - self.slength

    def smove(self):
        self.sx = pyxel.mouse_x

        if self.sx < 4:
            self.sx = 4
        if self.sx > self.field_width - 4:
            self.sx = self.field_width - 4

class enemy:
    def __init__(self, FW, x, y):
        self.field_width = FW
        self.field_length = self.field_width * 2

        self.ey = y
        self.ex = x
        self.lowx = x
        self.espeed = 2
        self.mxhp = 5
        self.esize = 10

    def emove(self):
        self.ex += self.espeed
        if self.lowx > self.ex or self.ex > self.lowx + self.field_width/2 - self.esize :
            self.espeed *= -1

    def edraw(self):
        pyxel.rect(self.ex, self.ey, self.esize, self.esize, pyxel.COLOR_ORANGE)
    
class mybullet:
    def __init__(self, FW):
        self.m_speed = 5
        self.field_width = FW
        self.field_length = self.field_width * 2
        self.restart()

    def restart(self):
        self.my = self.field_length - self.field_length / 20
        self.mx = pyxel.mouse_x

    def mmove(self):
        self.my -= self.m_speed

    def mdraw(self):
        pyxel.rect(self.mx, self.my, 4, 8, pyxel.COLOR_RED)
        
        
class enebullet:
    def __init__(self, FW, ex):
        self.eb_speed = 3
        self.field_width = FW
        self.field_length = self.field_width * 2
        self.ex = ex
        self.ebrestart()
        

    def ebrestart(self):
        self.eby = 25
        self.ebx = self.ex

    def ebmove(self):
        self.eby += self.eb_speed

    def ebdraw(self):
        pyxel.rect(self.ebx, self.eby, 4, 8, pyxel.COLOR_GREEN)


class App:
    def __init__(self):
        self.field_width = 150
        self.field_length = self.field_width * 2
        pyxel.init(self.field_width, self.field_length)

        self.score = 0
        self.alive = True
        self.life = 5

        self.cooltime = 10
        self.previous_bullet_frame = 0

        self.enemy_cooltime = 20
        self.enemy_previous_bullet_frame = 0

        self.ship = ship(self.field_width)
        self.mybullet = []
        self.enebullet = []
        self.enemy =[enemy(self.field_width, 0, 20),enemy(self.field_width, self.field_width/2, 20)]
        
        pyxel.run(self.update, self.draw)

    def bulletnum(self):
        #スペースキーを長押しするだけで続けて弾を発射できる。
        if pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count - self.previous_bullet_frame > self.cooltime:
            self.mybullet.append(mybullet(self.field_width))
            self.framecount = pyxel.frame_count
            self.previous_bullet_frame = pyxel.frame_count
        for mynum in self.mybullet:
            if mynum.my < 0:
                self.mybullet.remove(mynum)

    def enemy_bulletnum(self):
        if pyxel.frame_count - self.enemy_previous_bullet_frame > self.enemy_cooltime:
            for enenum in self.enemy:
                self.enebullet.append(enebullet(self.field_width, enenum.ex))
            self.enemy_framecount = pyxel.frame_count
            self.enemy_previous_bullet_frame = pyxel.frame_count
        for enenum in self.enebullet:
            if enenum.eby > self.field_length: 
                self.enebullet.remove(enenum)

    def myhit(self):
        for o in self.mybullet:
            for n in self.enemy:
                if n.ex <= o.mx and o.mx <= n.ex + n.esize:
                    if n.ey <= o.my and o.my <= n.ey + n.esize:
                        n.mxhp -= 1
                        self.mybullet.remove(o)
                        if n.mxhp == 0:
                            self.enemy.remove(n)

    def enehit(self):
        for p in self.enebullet:
            if self.ship.sx - self.ship.swidth/2 <= p.ebx and p.ebx <= self.ship.sx + self.ship.swidth - self.ship.swidth/2:
                if self.ship.sy <= p.eby and p.eby <= self.ship.sy + self.ship.slength:
                    self.enebullet.remove(p)
                    self.life -= 1
                    if self.life == 0:
                        self.alive = False

    def update(self):
        if self.alive == True:
            self.myhit()
            self.enehit()
            self.bulletnum()
            self.enemy_bulletnum()
            for b in self.mybullet:
                b.mmove()
            self.ship.smove()
            for e in self.enemy:
                e.emove()
            for f in self.enebullet:
                f.ebmove()
        
        #敵が全部消えた場合、敵の弾を全て消す。
        if self.enemy == []:
            self.enebullet = []

    def draw(self):
        if self.alive == True:
            pyxel.cls(7)
            for t in self.mybullet:
                t.mdraw()
            pyxel.rect(self.ship.sx - self.ship.swidth/2, self.ship.sy, self.ship.swidth, self.ship.slength, pyxel.COLOR_NAVY)
            pyxel.text(self.ship.sx +1 - self.ship.swidth/2 + 13, self.ship.sy + 5, f"{self.life}", pyxel.COLOR_BLACK)
            for h in self.enemy:
                    h.edraw()
                    pyxel.rect(h.ex, h.ey,10, 10, pyxel.COLOR_ORANGE)
                    pyxel.text(h.ex + 3, h.ey +3, f"{h.mxhp}", pyxel.COLOR_BLACK)
                    pyxel.text(h.ex + 4, h.ey +3, f"{h.mxhp}", pyxel.COLOR_WHITE)
            for e in self.enebullet:
                    e.ebdraw()
            
            if self.enemy == []:
                pyxel.text(self.field_width / 2, self.field_length / 2, "Clear!", pyxel.COLOR_BLACK)
        else:
            pyxel.text(self.field_width / 2, self.field_length / 2, "GAMEOVER", pyxel.COLOR_BLACK)  

App()