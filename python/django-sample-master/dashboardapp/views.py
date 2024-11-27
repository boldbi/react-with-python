import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from . import models

import requests
import json
import hashlib
import hmac
import base64
def index(request):
    
    return render(request,'index.html')

@api_view(['POST'])
def get_embed_details(request):
    body = json.loads(request.body.decode('utf-8'))
    embedQuerString = body.get("embedQuerString")
    dashboardServerApiUrl = body.get("dashboardServerApiUrl")
    embedQuerString = embedQuerString +"&embed_user_email=" + models.EmbedProperties.UserEmail
    timeStamp = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
    embedQuerString += "&embed_server_timestamp=" + str(timeStamp)
    embedDetailsUrl = "/embed/authorize?" + embedQuerString + "&embed_signature=" + get_signature_url(embedQuerString)
    result_content=requests.get(dashboardServerApiUrl+embedDetailsUrl)
    return HttpResponse(result_content)


def get_signature_url(message):
    #EmbedSecret = "G6zjbRHBGDzzsSoLwmRs9o7rqZJ2njIe"
    EmbedSecret = models.EmbedProperties.EmbedSecret
    keyBytes = bytes(EmbedSecret.encode('utf-8'))
    messageBytes = bytes(message.encode('utf-8'))
    hashMessage = base64.b64encode(hmac.new(keyBytes,messageBytes,digestmod=hashlib.sha256).digest())
    #var hashMessage = hmacsha1.ComputeHash(messageBytes);
    
    return str(hashMessage, "utf-8")
            
    


            