#!/usr/bin/env python3
'''
Created on 11.04.2016

@author: steffen
'''
import urllib.parse
import httplib2
from bs4 import BeautifulSoup


class LoginCheck:
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
                 sessionCookie:str,
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
        self.cookie=sessionCookie 
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
        
    def getIsLoggedIn(self):
        return not (self.httpContent==None)
    
    #
    # do client side stuff
    #
    
    def prepareRequest(self):    
        #add cookie to header
        self.header['Cookie']=self.cookie        
        self.body=""
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
        
                
    # parse HTML file in template
    def postProcessRequest(self):
        if(self.debugPrint):
            print("Postprocess Request")
            print(self.httpResponse)   
        content=self.httpContent.decode(encoding='utf-8')        
        response=self.httpResponse
        
        if(response.status>=200 and response.status<=400):
                self.status=response.status        
        
        #https://www.crummy.com/software/BeautifulSoup/
        soup=BeautifulSoup(content, "html.parser")
        
        warningInChallengeWrapper=soup.findAll('div', attrs={"class":"alert-danger"})
        if len(warningInChallengeWrapper)>0:
            warning=warningInChallengeWrapper[0].contents
            if "Please log in if you want to play" in str(warning):
                self.httpContent=None
                print(warning)
                return
        
        
        content=""
        #<class="challenge-wrapper">interesting stuff </div>
        extractedChallengeWrapper=soup.findAll('div', attrs={"class":self.filterTag})
        for div in extractedChallengeWrapper:            
            content+=str(div)
            if(self.debugPrint):
                print(str(div))#<div class="alert alert-danger" role="alert">Please log in if you want to play.</div>        
        
        self.httpContent=content
        
        
        return    