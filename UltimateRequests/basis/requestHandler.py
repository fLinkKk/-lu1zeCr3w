#!/usr/bin/env python3
'''
Created on 11.04.2016

@author: steffen
'''

import httplib2
from bs4 import BeautifulSoup
import requestHelpMethods


class RequestHandler:
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
        self.targetUrl=targetUrl        
        self.filterTag=filterTag.strip()
        self.requestType=httpRequestType
        self.httpHandler=httpHandler
        self.debugPrint=debugPrint
        if(self.debugPrint):
            print("Print args here")
            
        

    def run(self):     
        '''
        define running circumstances here.
        you may want to loop the request.
        this can be done here.
        '''   
        self.debugPrint=True
        self.prepareRequest()
        self.performRequest()
        self.postProcessRequest()
        self.debugPrint=True
    
    #
    # do client side stuff
    #
    
    def prepareRequest(self):  
        '''
            prepare your request's content here
        '''                  
        body=""
        
        
        
        self.body=requestHelpMethods.urlEncodeString(body, self.debugPrint)
        return    

    def performRequest(self): 
        '''
            define how the request is performed
        '''
        http=self.httpHandler; 
        url = self.targetUrl
        requestType=self.requestType
        header=self.header
        body=self.body
        
        if(self.debugPrint):
            print("HTTP Request to "+url)
        
        response, content = http.request(url, requestType, headers=header, 
                                           body=body)
        if(self.debugPrint):            
            print("finished request: "+str(response.status))            
            
        self.httpResponse=response 
        self.httpContent=content
        
                
    # parse HTML file in template
    def postProcessRequest(self):
        '''
            process the result.
            by default the challenge stuff is extracted from the result
            but you can specify that like you want to
        '''
        if(self.debugPrint):
            print("Postprocess Request")
            print(self.httpResponse)   
        content=self.httpContent.decode(encoding='utf-8')
        response=self.httpResponse
        self.unProccessedContent=content
        
        if(response.status>=200 and response.status<=400):
                self.status=response.status        
        
        #https://www.crummy.com/software/BeautifulSoup/
        soup=BeautifulSoup(content, "html.parser")
        
        warningInChallengeWrapper=soup.findAll('div', attrs={"class":"alert-danger"})
        for div in warningInChallengeWrapper:
            print(str(div))
        
        content=""
        #<class="challenge-wrapper">interesting stuff </div>
        extractedChallengeWrapper=soup.findAll('div', attrs={"class":self.filterTag})
        for div in extractedChallengeWrapper:            
            content+=str(div)#<div class="alert alert-danger" role="alert">Please log in if you want to play.</div>
            if(self.debugPrint):
                print(str(div))        
        
        self.httpContent=content
        
        
        return 
    
    
    def getHttpContent(self,unprocessed=False):
        '''
        returns the filtered http content from response
        if param=true then it returns the original response
        '''
        if(unprocessed):
            return self.unProccessedContent
        else:
            return self.httpContent
    
    def getHttpResponse(self):
        '''
        returns the response header
        '''
        return self.httpResponse   