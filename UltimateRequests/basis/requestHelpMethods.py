#!/usr/bin/env python3
'''
Created on 15.04.2016

contains useful methods to preprare request.
like encode b64
or hash

@author: steffen
'''

import binascii
import hashlib
import urllib.parse
import time
import base64

def getCurTime(debugOutput=False):
    curTime=time.perf_counter()
    if(debugOutput):
        print("Current time is:"+str(curTime))
    return curTime
    
def urlEncodeString(value:dict, debugOutput=False):
    '''
    encoded the given dictionary for http 
    '''
    result=urllib.parse.urlencode(value)
    if debugOutput:
        print("encoded '"+value+"' to :"+result)
    return result
    
    
def strToSha1(value:str, debugOutput=False):
    '''
    converts string to sha1
    '''
    result=hashlib.sha1(value.encode(encoding='utf_8')).hexdigest()
    if debugOutput:
        print("Converted '"+value+"' to sha1:"+result)
    return result

def strToSha512(value:str, debugOutput=False):
    '''
    converts string to sha512
    '''
    result=hashlib.sha512()(value.encode(encoding='utf_8')).hexdigest()
    if debugOutput:
        print("Converted '"+value+"' to sha512:"+result)
    return result

def strToHex(value:str, debugOutput=False):
    '''
    converts string to hex
    '''
    encValue=value.encode("utf-8")
    result=binascii.b2a_hex(encValue).decode("utf-8")+")"
    if debugOutput:
        print("Converted '"+value+"' to hex:"+result)
    return result

def packStrInSelectHex(value:str,debugOutput=False):
    hexValue=strToHex(value, debugOutput)
    result="(SELECT 0x"+hexValue+")"
    if debugOutput:
        print("Orig value:         "+value+"")
        print("Generated statement:"+result+"'")
    return result

def binaryStrToUtf8(binaryString,debugOutput=False):
    '''
    converts a given binary string to a utf-8
    '''
    
    hexContent=('%x' % int(binaryString, 2))
    result=bytes.fromhex(hexContent)
    result=result.decode(encoding="utf-8")
    if(debugOutput):
        print("Converted binary string:"+binaryString)
        print("To hex string:"+hexContent)
        print("To utf-8 string:"+result)
    return result

def strToB64(value:str,debugOutput=False):
    '''
    converts a given string to b64
    '''
    result=value.encode('UTF-8')
    result=base64.b64encode(result)
    result=result.decode('UTF-8')
    if debugOutput:
        print("Orig value:         "+value+"")
        print("Generated b64:"+result+"'")
    return result
        