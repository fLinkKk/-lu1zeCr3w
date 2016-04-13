#!/usr/bin/env python3
'''
Created on 11.04.2016

@author: steffen
#this class reads all neccessary parameters from the request.config file
it has a main but does not receive any arguments except the -v 
'''

import argparse
import httplib2

'''
relative import, so it is independant from its runtime environment
'''
from loginHandler import LoginHandler
from loginCheck import LoginCheck
from requestHandler import RequestHandler
import staticMethods



class ManageRequests:
    '''
    classdoc ManageRequests
    fills the requestsHandler with required input.
    Does write html output file if desired
    It also checks if user is logged in    
    '''
    
    def __init__(self, debugOutput):
        '''
        Constructor
        '''
        self.debugOutput=debugOutput
    
    def readConfig(self):
        '''
        reads config files
        
        READING COOKIE FILE IS MISSING
        '''
        configDic=staticMethods.readFileToDic("request.config", "::", False, self.debugOutput)
        self.targetUrl=configDic["targetUrl"]
        self.httpMethod=configDic["httpMethod"]
        self.filterTags=configDic["filterTags"]
        self.htmlFilename=configDic["outputHtmlFile"]
        sslCertFilename=configDic["sslCert"]
        self.httpHandler=httplib2.Http(ca_certs = sslCertFilename)
        workbenchDir=configDic["workbenchDir"]
                
        headerFile=staticMethods.joinPaths(workbenchDir, "header.dat", self.debugOutput)
        self.header=staticMethods.readFileToDic(headerFile,"::",False,self.debugOutput)
                
        self.cookieFile=staticMethods.joinPaths(workbenchDir, "cookie.dat", self.debugOutput)
                
        credentialsFile=staticMethods.joinPaths(workbenchDir, "credentials.dat", self.debugOutput)
        self.credentials=staticMethods.readFileToDic(credentialsFile,"::",True,self.debugOutput)
        
        loginUrlFile=staticMethods.joinPaths(workbenchDir, "loginUrl.dat", self.debugOutput)
        loginDic=staticMethods.readFileToDic(loginUrlFile,"::",False,self.debugOutput)
        self.loginUrl=loginDic["loginurl"]
        self.checkLoginUrl=loginDic["checkLoginUrl"]
        self.checkFilterTags=loginDic["checkFilterTag"]  
        self.loginhttpType=loginDic["loginhttpType"]  
        self.checkhttpType=loginDic["checkhttpType"]     
        
        
        
    def connectionSetup(self):
        '''
        Check login status and call login class if neccessary
        
        '''   
        self.isLoggedIn=False
        
        
        if(staticMethods.fileExists(self.cookieFile)):
            cookie=staticMethods.readStringFromFile(self.cookieFile, self.debugOutput)            
            '''
            do the login check here        
            '''            
            loginCheckHandle = LoginCheck(header=self.header,
                                          sessionCookie=cookie,                                       
                                          targetUrl=self.checkLoginUrl,
                                          filterTag=self.checkFilterTags, 
                                          httpHandler=self.httpHandler,
                                          httpRequestType=self.checkhttpType,
                                          debugPrint=self.debugOutput
                                          )
            loginCheckHandle.run()
            self.isLoggedIn=loginCheckHandle.getIsLoggedIn()
            
                       
            if(not self.isLoggedIn):
                '''
                if failed remove cookie from header
                ''' 
                self.header.pop('Cookie')        
        
        if not self.isLoggedIn:
            '''
            not logged in.
            log in
            '''
            loginHandle = LoginHandler(header=self.header,
                                       credentials=self.credentials,
                                       targetUrl=self.loginUrl,
                                       filterTag=self.filterTags, 
                                       httpHandler=self.httpHandler,
                                       httpRequestType=self.loginhttpType,
                                       debugPrint=self.debugOutput
                                       )
            loginHandle.run()
            self.isLoggedIn=loginHandle.isLoginSuccessfull()
            
            if(loginHandle.status>=200 and loginHandle.status<=400):   
                '''
                no need to add cookie to header. this is done in loginHandle.run automatically
                '''             
                if(self.isLoggedIn):
                    staticMethods.writeStringToFile(self.cookieFile, loginHandle.cookie, self.debugOutput)
        
    
    def runRequest(self):
        if(not self.isLoggedIn):
            print("writeOutputHTMLFile:not logged in. Can not execute request to challenge. Please check your credentials")
            return
        
        '''
        runs the http request
        ''' 
        requestHandle=RequestHandler( header=self.header,                                       
                                      targetUrl=self.targetUrl,
                                      filterTag=self.filterTags, 
                                      httpHandler=self.httpHandler,
                                      httpRequestType=self.checkhttpType,
                                      debugPrint=self.debugOutput
                                      )
        requestHandle.run()
        self.requestResult=requestHandle.getHttpContent(False)
        
        
    def writeOutputHTMLFile(self):
        '''
        Write output file
        Write output to console too
        '''
        if(not self.isLoggedIn):
            print("writeOutputHTMLFile:not logged in. Can not execute request to challenge. Please check your credentials")
            return
        staticMethods.writeStringToFile(self.htmlFilename, self.requestResult, True)
        
                
    def run(self):
        '''
        Start method
        connection setup can be looped for several attempts
        '''
        self.readConfig()
        self.connectionSetup()
        self.runRequest()
        self.writeOutputHTMLFile()
        
    

def main():
    
    debugOutput=False
    parser = argparse.ArgumentParser()
    scriptPath= staticMethods.getScriptPath()    
    staticMethods.setRunningDir(scriptPath)
    
    parser.add_argument("--verbose","-v", 
                        help="Verbose", 
                        action="store_true", default=False)
    args = parser.parse_args()
    debugOutput=staticMethods.getFirstArgument(args,"verbose", debugOutput)
    if(debugOutput):
        print("Verbose is on. Have fun with debug output")
        
    mr=ManageRequests(debugOutput)
    mr.run()
    
if __name__ == '__main__':
    main()