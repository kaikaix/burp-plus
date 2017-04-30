from burp import IBurpExtender
import requests
import os
import re
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from burp import IHttpRequestResponse


class BurpExtender(IBurpExtender,IIntruderPayloadGeneratorFactory,IHttpRequestResponse):
    def registerExtenderCallbacks(self,callbacks):
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        callbacks.setExtensionName("code")
    
    def getGeneratorName(self):
        return "vcode"

    def createNewInstance(self,attack):
        tem = "".join(chr(abs(x)) for x in attack.getRequestTemplate())
        tem = re.findall("Cookie:(.+?)\n",tem)
        return DetectXss(attack,tem)

class DetectXss(IIntruderPayloadGenerator):
    def __init__(self,attack,cookie):
        self.target="input the code's link here"
        self.cookie = cookie
        self.max = 1
        self.num = 0
        self.attack = attack

    def hasMorePayloads(self):
        if self.num == self.max:
            return False
        else:
            return True

    def getNextPayload(self,payload):
        headers = {'Cookie':self.cookie}
        r = requests.get(self.target,headers=headers)
        f = open('code.png','w')
        f.write(r.content)
        f.close()
        os.system('python code.py')

        f = open('result.txt','r')
        code = f.read()
        f.close()
        
        return code
        
    def reset(self):
        print "reset"
        self.num = 0
        return