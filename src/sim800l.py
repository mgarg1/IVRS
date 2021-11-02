import time
import sys
import serial

def convert_to_string(buf):
    try:
        tt =  buf.decode('utf-8').strip()
        return tt
    except UnicodeError:
        tmp = bytearray(buf)
        for i in range(len(tmp)):
            if tmp[i]>127:
                tmp[i] = ord('#')
        return bytes(tmp).decode('utf-8').strip()

class SIM800L:
    def __init__(self,port,baud=9600):
        try:
            self.ser=serial.Serial(port,baudrate=baud, timeout=1)
        except Exception as e:
            sys.exit("Error: {}".format(e))
        self.incoming_action = None
        self.no_carrier_action = None
        self.clip_action = None
        self._clip = None
        self.msg_action = None
        self._msgid = 0
        self.savbuf = None

    def setup(self):
        self.command('ATE0\n')         # command echo off
        self.command('AT+CLIP=1\n')    # caller line identification
        self.command('AT+CMGF=1\n')    # plain text SMS
        self.command('AT+CLTS=1\n')    # enable get local timestamp mode
        self.command('AT+CSCLK=0\n')   # disable automatic sleep

    def callback_incoming(self,action):
        self.incoming_action = action

    def callback_no_carrier(self,action):
        self.no_carrier_action = action

    def get_clip(self):
        return self._clip

    def callback_msg(self,action):
        self.msg_action = action

    def get_msgid(self):
        return self._msgid

    def command(self, cmdstr, lines=1, waitfor=500, msgtext=None):
        while self.ser.in_waiting:
            self.ser.readline()
        self.ser.write(cmdstr.encode())
        if msgtext:
            self.ser.write(msgtext.encode())
        if waitfor>1000:
            time.sleep((waitfor-1000)/1000)
        buf=self.ser.readline() #discard linefeed etc
        print(buf)
        buf=self.ser.readline()
        if not buf:
            return None
        result = convert_to_string(buf)
        if lines>1:
            self.savbuf = ''
            for i in range(lines-1):
                buf=self.ser.readline()
                if not buf:
                    return result
                buf = convert_to_string(buf)
                if not buf == '' and not buf == 'OK':
                    self.savbuf += buf+'\n'
        return result

    def check_network(self):
        result = self.command('AT+CREG\n')
        return result

    def answer_call(self):
        result = self.command('ATA\n')
        # print('result is--> ')
        #print(result)

    def end_call(self):
        # https://stackoverflow.com/questions/14756791/terminating-a-voice-call-via-at-command
        result = self.command('ATH\n',1)
        print('result of end call - ')
        print(result)
        

    def send_sms(self,destno,msgtext):
        result = self.command('AT+CMGS="{}"\n'.format(destno),99,5000,msgtext+'\x1A')
        time.sleep(5)
        if result and result=='>' and self.savbuf:
            params = self.savbuf.split(':')
            if params[0]=='+CUSD' or params[0] == '+CMGS':
                return 'OK'
        return 'ERROR'

    def read_sms(self,id):
        result = self.command('AT+CMGR={}\n'.format(id),99)
        if result:
            params=result.split(',')
            if not params[0] == '':
                params2 = params[0].split(':')
                if params2[0]=='+CMGR':
                    number = params[1].replace('"',' ').strip()
                    date_data   = params[3].replace('"',' ').strip()
                    time_data   = params[4].replace('"',' ').strip()
                    return  [number,date_data,time_data,self.savbuf]
        return None

    def delete_sms(self,id):
        self.command('AT+CMGD={}\n'.format(id),1)

    def check_incoming(self):
        if self.ser.in_waiting:
            buf=self.ser.readline()
            # print(buf)
            buf = convert_to_string(buf)
            params=buf.split(',')

            if params[0][0:5] == "+CMTI":
                self._msgid = int(params[1])
                if self.msg_action:
                    self.msg_action()

            elif params[0] == "NO CARRIER":
                self.no_carrier_action()

            elif params[0] == "RING" or params[0][0:5] == "+CLIP":
                print('MG - RINGING')
                # extra readline to eataway the empty line
                buf=self.ser.readline()
                buf=self.ser.readline()
                # print(buf)                
                phoneNum=''
                if buf.find(b'+CLIP:') != -1:
                    phoneNum = buf[buf.index(b'+CLIP:')+7:].split(b',')[0]
                    # print('phoneNum extr - ' + str(phoneNum))
                phoneNum2 = [s for s in str(phoneNum) if s.isdigit()]
                phoneNum2 = ''.join(phoneNum2)
                # print('phone Num is:')
                # print(phoneNum2)
                self.incoming_action(str(phoneNum2))

    def read_and_delete_all(self):
        try:
            return self.read_sms(1)
        finally:
            self.command('AT+CMGDA="DEL ALL"\n',1)
