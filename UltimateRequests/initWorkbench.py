#!/usr/bin/env python3
'''
Created on 12.04.2016

@author: steffen
#creates ~/.rzt directory
#copies all *.tpl files from directory templates to target ~/.rzt
#asks user name and password and stores it 
'''

import argparse
from basis import staticMethods
import getpass



def loginData(isPasswordPlain):
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    if isPasswordPlain:
        p1=input("Password for %s: " % user)
    else:
        pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
    
        p1, p2 = pprompt()
        
        while p1 != p2 or not p1:
            if(not p1):
                print("Password must not be empty. If you try to copy & paste it use plain parameter --passwordPlain on program start")
            if(p1!=p2):
                print('Passwords do not match. Try again')
            p1, p2 = pprompt()

    user=user.strip()
    p1=p1.strip()
    return user, p1


def main():
    parser = argparse.ArgumentParser()
    
    scriptPath= staticMethods.getScriptPath()
    scriptPath = staticMethods.getParentDir(scriptPath)
    staticMethods.setRunningDir(scriptPath)
    scriptPath=staticMethods.joinPaths(scriptPath,"challenges")
    workbenchPath="~/.rzt"
    workbenchPath=staticMethods.solvePath(workbenchPath)
    parser.add_argument("--verbose","-v", 
                        help="Verbose", 
                        action="store_true", default=False)
    parser.add_argument("--dirWorkbench","-d", 
                        nargs=1, help="absolute path to workbench. default is "+workbenchPath,
                        default=workbenchPath)    
    parser.add_argument("--dirChallenges","-c", 
                        nargs=1, help="absolute path to challenges directory. default is "+scriptPath,
                        default=scriptPath)
    parser.add_argument("--passwordPlain","-p", 
                        help="enables to set the password interactively in plaintext",
                        action="store_true", default=False)
    args = parser.parse_args()
    
    global globalDebugOutput
    globalDebugOutput=False
    
    globalDebugOutput=staticMethods.getFirstArgument(args,"verbose", globalDebugOutput)
    if(globalDebugOutput):
        print("Verbose is on. Have fun with debug output")
    
    isPasswordPlain=staticMethods.getFirstArgument(args,"passwordPlain", globalDebugOutput)
    if(isPasswordPlain and globalDebugOutput):
        print("Password plain mode enabled")
        
    dirWorkbench=staticMethods.getFirstArgument(args, "dirWorkbench", globalDebugOutput)
    dirWorkbench=staticMethods.solvePath(dirWorkbench, globalDebugOutput)
    if(globalDebugOutput):
        print("Workbench is set to: "+dirWorkbench)    
    
    dirChallenges=staticMethods.getFirstArgument(args, "dirChallenges", globalDebugOutput)
    dirChallenges=staticMethods.solvePath(dirChallenges, globalDebugOutput)
    if(globalDebugOutput):
        print("Challenges dir is set to: "+dirChallenges)    
    
    
    staticMethods.writeStringToFile("workbench.path",dirWorkbench, globalDebugOutput)
    
    isSuccess= staticMethods.createDir(dirWorkbench, globalDebugOutput)
    
    if not isSuccess:
        print("Workbench directory "+dirWorkbench+ " could not be created")
        print("Program will exit not.")
        return
    
    challengesPath=staticMethods.joinPaths(dirWorkbench, "challenges.path", globalDebugOutput)
    staticMethods.writeStringToFile(filename=challengesPath, content=dirChallenges, debugOutput=globalDebugOutput)
        
    '''
    copy all *.tpl files from template directory
    '''
    isSuccess=staticMethods.copyAllFilesInFolder("templates", dirWorkbench, ".tpl",True, globalDebugOutput)            
        
    username,password=loginData(isPasswordPlain)
    
    credentials = {"username":username,
                   "password":password}
    
    if globalDebugOutput:
        print("Username="+username+" password="+password)
    credentialsFilename=staticMethods.joinPaths(dirWorkbench,"credentials.dat", globalDebugOutput)
    staticMethods.writeDicToFile(dic=credentials, filename=credentialsFilename, delimiter="::", encodeValueB64=True, debugOutput=globalDebugOutput)
    
    staticMethods.readFileToDic(filename=credentialsFilename, delimiter="::", decodeValueB64=True, debugOutput=globalDebugOutput)
    return 0
        
        
if __name__ == "__main__":
    main()
