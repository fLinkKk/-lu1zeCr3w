#!/usr/bin/env python3
'''
Created on 13.04.2016
@author: steffen

contains static methods which can be reused by the other scripts
'''
import os
import base64
import shutil
from pathlib import Path

def getFirstArgument(args,attributeName,debugOutput=False):
    args=getattr(args, attributeName)
    if(isinstance(args,list)):      
        args=args[0] 
    return args

def fileExists(path):
    return os.path.exists(path)

def createDir(directoryName,debugOutput=False):
    if(os.path.exists(directoryName)==False):        
        os.makedirs(directoryName)    
        if debugOutput:
            print("Created dir: "+directoryName)        
    return os.path.exists(directoryName)

def copyFile(srcFilename,dstFilename, debugOutput=False):
    try:                
        shutil.copy(srcFilename, dstFilename)
        if(debugOutput):
            print("Copy "+srcFilename + " to "+dstFilename)
    except OSError as why:
        print(srcFilename, dstFilename, str(why))                  
    finally:
        if (not os.path.exists(dstFilename)):
            print(dstFilename+" could not be created")
    return

def copyAllFilesInFolder(srcFolder,targetFolder, endsWith="",removeFilteredEnding=False,debugOutput=False):
    
    srcFolder=finalizePath(srcFolder)
    targetFolder=finalizePath(targetFolder)
    
    
        
    for srcFilename in os.listdir(srcFolder):
        srcFilename = os.path.join(srcFolder,srcFilename)
        if(os.path.isfile(srcFilename) and str(srcFilename).endswith(endsWith)):
            dstFilename = os.path.basename(srcFilename)
            dstFilename = os.path.join(targetFolder, dstFilename)
            if removeFilteredEnding:
                base, ext = os.path.splitext(dstFilename)
                if(ext==endsWith):
                    dstFilename=base
            copyFile(srcFilename, dstFilename,debugOutput)
        
    return


def setRunningDir(path,debugOutput=False):
    if(debugOutput):
        print("Change running dir to: "+ path)
    os.chdir(path)

def getScriptPath(debugOutput=False):
    scriptPath=os.path.dirname(os.path.realpath(__file__))
    if debugOutput:
        print("Script is located at: "+ scriptPath)
    return scriptPath

def getParentDir(path,debugOutput=False):
    return str(Path(path).parent.absolute())     

   
def finalizePath(path,debugOutput=False):
    oldPath=path
    path=solvePath(path,debugOutput)
    path=os.path.abspath(path)
    if debugOutput:
        print("Finalized "+oldPath+" to :"+ path)
    return path
    
def solvePath(path,debugOutput=False):
    oldPath=path
    path=os.path.expanduser(path)
    if debugOutput:
        print("Finalized "+oldPath+" to :"+ path)
    return path   
    
def getAbsolutePathFromRelative(relativePath,debugOutput=False):
    absPath=joinPaths(os.getcwd(), relativePath,debugOutput)  
    if debugOutput:
        print("Converted relative path "+relativePath+" to absolute path:"+ absPath)
    return absPath

def joinPaths(path1,path2,debugOutput=False):
    if debugOutput:
        print("join "+path1 +" and path2 "+path2)
        
    joinedPath=os.path.join(path1, path2)
    if debugOutput:
        print("joined path1 "+path1 +"and path2 "+path2+" to new path: "+ joinedPath)
    return joinedPath

def readStringFromFile(filename,debugOutput=False):
    content=""
    if (not filename)==False: 
            with open(filename, 'r') as readStream:                
                content=readStream.read()                    
    if debugOutput:
        print("Read content: "+content + " from file: "+ filename)
    content=content.strip()
    return content

def writeStringToFile(filename, content,debugOutput=False):
    if debugOutput:
        print("Write content: "+content + " to file: "+ filename)
    if (not filename)==False: 
            with open(filename, 'w') as writeStream:                
                writeStream.write(str(content))                    
    return

def readFileToDic(filename, delimiter="::",decodeValueB64=False,debugOutput=False):
    dic={}    
    if debugOutput:
        print("Read into dictionary from file: "+filename + " using delimiter "+ delimiter+ " and b64= "+str(decodeValueB64))
    with open(filename, 'r') as out:
        for line in out:       
            line=line.strip()     
            if debugOutput:
                print("Reading line: "+line)
            curProperty=line.split(delimiter)
            key=curProperty[0]
            value=curProperty[1]
            if(decodeValueB64):    
                value=value.encode('UTF-8')
                value=base64.decodebytes(value)         
                value=value.decode('UTF-8')
                value=value.strip()
            if debugOutput:
                print("Read Key="+key+" value="+value)
            dic[key]=value
    return dic
    
def writeDicToFile(dic,filename,delimiter='::',encodeValueB64=False,debugOutput=False):
    if debugOutput:
        print("Write dictionary into file: "+filename + " using delimiter "+ delimiter+ " and b64= "+str(encodeValueB64))
    with open(filename, 'w') as filestream:                        
        for key in dic:
            value=dic[key]
            if debugOutput:
                print("Write Key="+key+" value="+value)
            if(encodeValueB64):
                value=value.encode('UTF-8')                
                value=base64.b64encode(value)
                value=value.decode('UTF-8')
            
            line=key+delimiter+value
            filestream.write(line+'\n')
            if debugOutput:
                print("Writing line:"+line)

def createPyPackages(startDir, baseDir, debugOutput=False): 
    if debugOutput:
        print("Create __init__.py files recursively up from "+ startDir+ " to "+baseDir)
    if(not startDir.startswith(baseDir)):
        if debugOutput:
            print(startDir+ " is not subdir of "+ baseDir)
        return
    
    while True:
        newFile=joinPaths(startDir, "__init__.py", debugOutput)
        touch(newFile,debugOutput)
        startDir=getParentDir(startDir, debugOutput)
        if(getAbsolutePathFromRelative(startDir, debugOutput)==getAbsolutePathFromRelative(baseDir, debugOutput)):
            if(debugOutput):
                print("Reached base dir.")
            break    
    return
                
def touch(path,debugOutput=False):
    if(fileExists(path)):
        if debugOutput:
            print("File "+ path+ " already exists")
            return
    with open(path, 'a'):
        os.utime(path, None)
    if debugOutput:
            print("Touch empty file: "+ path)
        
        
        
        