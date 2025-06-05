import json
from bson import ObjectId
from datetime import datetime
def convert_obj(obj):
    if isinstance(obj,ObjectId):
        return str(obj)
    elif isinstance(obj,datetime):
        return obj.isoformat()
    return obj
class Response:
    def __init__(self):
        self.__headerTextPlain = ('200 OK',[('Content-type','plain/text')])
        self.__headerJson = ('200 OK',[('Content-type','application/json')])
        self.__headerHtml = ('200 OK',[('Content-type','text/html')])
        self.__headerCSS = ('200 OK',[('Content-type','text/css')])
        self.__headerJavascript = ('200 OK',[('Content-type','text/javascript')])
        self.__headerPng = ('200 OK',[('Content-type','image/png')])
        self.__headerJpg = ('200 OK',[('Content-type','image/jpg')])
        self.__headerJpeg = ('200 OK',[('Content-type','image/jpeg')])
        self.__headerGif = ('200 OK',[('Content-type','image/gif')])
        self.__headerError = ('401',[('Content-type','plain/text')])
        #self.__headerOther = ('200 OK',[('Content-Type', 'application/octet-stream'),('Content-Disposition', f'attachment; filename="{filename}"')])
    def error(self,body):
        print(body)
        return (self.__headerError,body)
    def text(self,body):
        return (self.__headerTextPlain,body)
    def png(self,body):
        return (self.__headerPng,body)
    def jpg(self,body):
        return (self.__headerJpg,body)
    def jpeg(self,body):
        return (self.__headerJpeg,body)
    def gif(self,body):
        return (self.__headerGif,body)
    def html(self,body):
        return (self.__headerHtml,body)
    def css(self,body):
        return (self.__headerCSS,body)
    def js(self,body):
        return(self.__headerJavascript,body)
    def json(self,body):
        b = json.dumps(body,default=convert_obj)
        print(str(b),self.__headerJson)
        return(self.__headerJson,b)
    def other(self,body,filename):
        print("imprimindo filename")
        print(filename)
        ('200 OK',[('Content-Type', 'application/octet-stream'),('Content-Disposition', f'attachment; filename="{filename}"')])
        return(self.__headerOther.body)


