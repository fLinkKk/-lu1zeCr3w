#!/usr/bin/python3
'''
Created on 11.04.2016

@author: steffen
'''
import urllib.parse
import httplib2


class LoginHandler:
    '''
    classdocs
    This class does not do any I/O operations
    It does not create a html file output. This can be done somewhere else
    It's focus is on request handling
    it's also designed to handle multiple request to the same target.
    This can be defined in the "run" method.
    
    '''

    
    def __init__(self,
                 header:dict, 
                 credentials:dict,
                 targetUrl:str,
                 filterTag:str, 
                 httpHandler:httplib2.Http,
                 httpRequestType:str,
                 debugPrint:bool):
        '''
            Constructor
            @param header: contains the cookie already.
             
        '''  
          
        self.header=header
        self.credentials=credentials        
        self.targetUrl=targetUrl        
        self.filterTag=filterTag.strip()
        self.requestType=httpRequestType
        self.httpHandler=httpHandler
        self.debugPrint=debugPrint
        if(self.debugPrint):
            print("Print args here")
            
        

    def run(self):        
        self.prepareRequest()
        self.performRequest()
        self.postProcessRequest()
    
    def getStatus(self):
        return self.status
    
    def getCookie(self):
        return self.cookie
    #
    # do client side stuff
    #
    
    def prepareRequest(self):   
        if(self.debugPrint):
            print("Preprocess Request") 
        #add cookie to header
        #self.header['Cookie']=self.cookie        
        self.body=self.credentials
        return    

    def performRequest(self): 
        http=self.httpHandler; 
        url = self.targetUrl
        requestType=self.requestType
        header=self.header
        body=self.body
        
        if(self.debugPrint):
            print("HTTP Request to "+url)
        
        response, content = http.request(url, requestType, headers=header, 
                                           body=urllib.parse.urlencode(body))
        if(self.debugPrint):            
            print("finished request: "+str(response.status))            
            
        self.httpResponse=response 
        self.httpContent=content
        
                
    
    def postProcessRequest(self):
        if(self.debugPrint):
            print("Postprocess Request")
            print(self.httpResponse)   
        content=self.httpContent.decode(encoding='utf-8')        
        response=self.httpResponse
        
        if(response.status>=200 and response.status<=400):
                self.status=response.status
        
        cookie=response['set-cookie']
        cookie=str(cookie).split(sep=';')[0]
        
        if self.debugPrint:
                    print("request seems successfully")
                    print("cookie:"+cookie)                    
                    
        self.header['Cookie']=cookie   
        self.cookie=cookie
        self.httpContent=content
        
        return    