import requests
import json
import calendar
import time
import datetime as DT
import os

now = calendar.timegm(time.gmtime())
before = now - 60 #query last minute

nowFormat = DT.datetime.utcfromtimestamp(now).isoformat()
beforeFormat = DT.datetime.utcfromtimestamp(before).isoformat()

# Set following line to your Spark Token (from developer.ciscospark.com)
# eg, botAuthToken = "123456789012345678901234567890"
botAuthToken = os.environ.get("SPARK_ACCESS_TOKEN")

print("\n================\n")
print ("Just querying Spark...\n\n")


def get_Events():
    baseurl = "https://api.ciscospark.com/v1"
    endpointUrl = "/events?resource=memberships&type=created&from=%s.000Z&to=%s.000Z" % (beforeFormat,nowFormat)
    finalUrl = baseurl + endpointUrl
    
    headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "Authorization": "Bearer %s" % botAuthToken
           }

    resp = requests.get(finalUrl, headers=headers)

    events = json.loads(resp.text)['items']

    matchCount = 0
    missCount = 0

    for event in events:
        personEmail = event["data"]["personEmail"]
        membershipId = event["data"]["id"]
        actorId = event["actorId"]
        roomId = event["data"]["roomId"]

        # change following line to desired domain
        if "@gmail.com" in personEmail:
            print("Contains Gmail Account")
            matchCount += 1

            deleteUser(membershipId)
            getPersonDidIt(actorId)
        else:
            missCount += 1

    print ("Matches: %s\nNo Match: %s" % (matchCount,missCount))


def deleteUser(membershipId):
    print("About to delete user")

    finalUrl = "https://api.ciscospark.com/v1/memberships/" + membershipId
    print(finalUrl)

    bot_auth_token = botAuthToken

    headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "Authorization": "Bearer %s" % botAuthToken
           }

    me_resp = requests.delete(finalUrl, headers= headers)


def getPersonDidIt(actorId):
    print("About to get Person who did it")
    url = "https://api.ciscospark.com/v1/people/" + actorId
    print(url)

    bot_auth_token = botAuthToken

    headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "Authorization": "Bearer %s" % botAuthToken
           }
    

    resp = requests.get(url, headers=headers)

    actorEmail = json.loads(resp.text)['emails'][0]

    postToSpark(actorEmail)


def postToSpark(personEmail):
    url = "https://api.ciscospark.com/v1/messages"

    imageUrl = "https://talk2spark.com/events/alert.png"

    headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "Authorization": "Bearer %s" % botAuthToken
           }


    payload = {
        "toPersonEmail": personEmail,
        "files": imageUrl
    }
    data = json.dumps(payload)
    print (data)
    response = requests.post(url, data=data, headers=headers)


if __name__ == '__main__':
    get_Events()
    
