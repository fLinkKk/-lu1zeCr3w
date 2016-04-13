#!/usr/bin/env python3
'''
Created on 12.04.2016

@author: steffen
'''

from basis import staticMethods
import argparse


def genConfigFile(workbenchDir, destDir, targetUrl, filterTags,httpMethod, outputHtmlFile,sslCertFile):
    
    
    configFilename=staticMethods.joinPaths(destDir, "request.config",globalDebugOutput)
    if(globalDebugOutput):
        print("generating .config file: "+configFilename)
        
    config={}
    config['workbenchDir']=workbenchDir
    config['targetUrl']=targetUrl
    config['filterTags']=filterTags
    config['httpMethod']=httpMethod
    config['outputHtmlFile']=outputHtmlFile
    config['sslCert']=sslCertFile
    staticMethods.writeDicToFile(config, configFilename, "::", False, globalDebugOutput)    
    return 


def getWorkbenchPath():
    workbenchPath=staticMethods.readStringFromFile("workbench.path", False)
    workbenchPath=staticMethods.solvePath(workbenchPath,False)
    return workbenchPath        

def getChallengesDir(workbenchDir):    
    challengesPath=staticMethods.joinPaths(workbenchDir, "challenges.path", False)    
    challengesDir=staticMethods.readStringFromFile(challengesPath, False)
    return challengesDir
    
def main():
    runningScriptDir= staticMethods.getScriptPath()
    runningScriptDir = staticMethods.getParentDir(runningScriptDir)
    staticMethods.setRunningDir(runningScriptDir)
    workbenchDir=getWorkbenchPath()
    challengesDir=getChallengesDir(workbenchDir)     
    defaultCAStorePath="/etc/ssl/cert.pem"
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirChallenge","-d", nargs=1, 
                        help="""Enter an relative path to place the challenge files. \n"
                        They are located as subdirectories of """+ challengesDir
                        +""" example: web/xss/1"""
                        )
                        
    parser.add_argument("--targetUrl","-t", nargs=1, help="url to login")
    parser.add_argument("--httpMethod","-m", nargs=1, help="GET|POST|PUT|OPTION",
                        default="GET")
    parser.add_argument("--filterTags","-f", nargs=1, help="challenge-wrapper", 
                        default="challenge-wrapper")    
    parser.add_argument("--outputHtmlFile","-o", nargs=1, help="response.html", 
                        default="response.html")    
    
    parser.add_argument("--sslCertFile","-s", nargs=1, 
                        help="Enter an absolute path to the certificate store\nIn Arch Linux it is e.g.:"+ defaultCAStorePath,
                        default=defaultCAStorePath)
    
    parser.add_argument("--challengeDirAsPyPackage","-c", help="create __init__.py files recursively in the challenges dir", 
                        action="store_true", default=True)
    parser.add_argument("--verbose","-v", help="Verbose", action="store_true", default=False)
    args = parser.parse_args()
    
    global globalDebugOutput
    globalDebugOutput=False
    if(args.verbose):
        print("Verbose is on. Have fun with debug output")
        globalDebugOutput=True
         
    if(args.targetUrl==None):
        print("No target url set. Please specifiy a target url. Program will exit now.")
        return
    
    if(args.dirChallenge==None):
        print("No challenge directory set. Please specifiy a directory to place the challenge files. Program will exit now.")
        return
    
    dirNewChallenge=staticMethods.getFirstArgument(args, "dirChallenge", globalDebugOutput)
    dirNewChallenge=staticMethods.joinPaths(challengesDir, dirNewChallenge, globalDebugOutput)
    isSuccess=staticMethods.createDir(dirNewChallenge, globalDebugOutput)    
    
    if not isSuccess:
        print("Challenge dir:"+dirNewChallenge+" could not be created. Program is exiting now")
        return
    
    basisDir=staticMethods.joinPaths(runningScriptDir,"basis")
    staticMethods.copyAllFilesInFolder(basisDir, dirNewChallenge, ".py", False, globalDebugOutput)
    
    targetUrl=staticMethods.getFirstArgument(args, "targetUrl", globalDebugOutput)
    
    httpMethod=staticMethods.getFirstArgument(args, "httpMethod", globalDebugOutput)
    
    filterTags=staticMethods.getFirstArgument(args, "filterTags", globalDebugOutput)
    
    outputHtmlFile=staticMethods.getFirstArgument(args, "outputHtmlFile", globalDebugOutput)
    
    challengeDirAsPyPackage=staticMethods.getFirstArgument(args, "challengeDirAsPyPackage", globalDebugOutput)
    
    sslCertFile=staticMethods.getFirstArgument(args, "sslCertFile", globalDebugOutput)
    
    if(challengeDirAsPyPackage):
        staticMethods.createPyPackages(dirNewChallenge, runningScriptDir,globalDebugOutput)
    genConfigFile(workbenchDir=workbenchDir,destDir=dirNewChallenge, 
                  targetUrl=targetUrl, filterTags=filterTags, httpMethod=httpMethod,
                  outputHtmlFile=outputHtmlFile, sslCertFile=sslCertFile)
    

if __name__ == '__main__':
    main()