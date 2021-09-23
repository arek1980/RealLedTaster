#_data_comment_
import RPi.GPIO as GPIO
import time
import sqlite3
#
#-*- coding: utf-8 -*-

class sql_setup:
    def __init__(self, pfad=str):
        pfad = "{0}/datenbank.db".format(pfad)
        file = open(pfad,"a+")
        self.verbindung = sqlite3.connect(pfad)
        self.zeiger = self.verbindung.cursor()

    def create_table(self,name,spalte,typ,spalte2,typ2):
        create_table = 'CREATE TABLE IF NOT EXISTS "{0}" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"{1}" {2},"{3}" {4});'.format(name,spalte,typ,spalte2,typ2)
        self.zeiger.execute(create_table)
        self.verbindung.commit()

    def neue_spalte(self,tableName, spalte ,typ):
        spalte= "ALTER TABLE {0} ADD COLUMN {1} {2};".format(tableName,spalte,typ)
        self.zeiger.execute(spalte)
        self.verbindung.commit()
    def daten_einfuegen(self,tablename,data1,data2):
        insert = 'INSERT INTO {0} VALUES (NULL,"{1}", "{2}")'.format(tablename,data1,data2)
        self.zeiger.execute(insert)
        self.verbindung.commit()

class led:
    def __init__ (self,ledpin):
        self.ledpin = ledpin
        self.zustand = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ledpin,GPIO.OUT)
        GPIO.output(self.ledpin, GPIO.LOW)

    def led_an(self):
        GPIO.output(self.ledpin, GPIO.HIGH)
        self.zustand = True
        print(self.zustand)
    
    def led_aus(self):
        GPIO.output(self.ledpin, GPIO.LOW)
        self.zustand = False
        print(self.zustand)


class Taster:
    def __init__(self, tasterpin):
        self.tasterpin = tasterpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.tasterpin,GPIO.IN,GPIO.PUD_DOWN)

    def gedruekt(self):
        return GPIO.input(self.tasterpin)
            

try:

    if __name__ == "__main__":
        GPIO.setwarnings(False)
        GPIO.cleanup()
        db = sql_setup("/home/pi/Desktop")
        db.create_table("LEDundTASTER","zustand","TEXT","datum","TEXT")
        Taster = Taster(10)
        led = led(24)
        while True:
            if Taster.gedruekt() == True:
                while Taster.gedruekt() == True:
                    pass
                if led.zustand == True:
                    led.led_aus()
                    db.daten_einfuegen("LEDundTASTER",led.zustand,str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                elif led.zustand == False:
                    led.led_an()
                    db.daten_einfuegen("LEDundTASTER",led.zustand,str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))

            
except KeyboardInterrupt:
    GPIO.cleanup()
    
        
                
