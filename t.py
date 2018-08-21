# -*- coding: utf-8 -*-

from line.linepy import *
import json, requests, sys, time, re, ast

end = 0
listApp = [
	"CHROMEOS\t2.1.5\tHelloWorld\t11.2.5", 
	"DESKTOPWIN\t5.9.2\tHelloWorld\t11.2.5", 
	"DESKTOPMAC\t5.9.2\tHelloWorld\t11.2.5", 
	"IOSIPAD\t8.11.0\tHelloWorld\t11.2.5", 
	"WIN10\t5.5.5\tHelloWorld\t11.2.5"
]
try:
	for app in listApp:
		try:
			try:
				with open("authToken.txt", "r") as token:
					authToken = token.read().replace("\n","")
					if not authToken:
						client = LINE()
						with open("authToken.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName=app)
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					sys.exit("[ INFO ] BOT REVOKE")
				elif "auth" in error:
					continue
				else:
					sys.exit("[ INFO ] BOT ERROR")
		except Exception as error:
			print(error)
except Exception as error:
	print(error)

with open("authToken.txt", "w") as token:
    token.write(str(client.authToken))
channel = Channel(client, client.server.CHANNEL_ID['JUNGEL_PANG'])
channelToken = channel.getChannelResult()
clientMid = client.profile.mid
clientPoll = OEPoll(client)

help = """╔〘""" + client.getProfile().displayName +"""〙
║
╠═✪〘 ข้อความช่วยเหลือ  〙
║
╠✪〘 คำสั่งปกติ 〙
╠➣ /me (@)
╠➣ /mid (@)
╠➣ /picture (@)
║
╠✪〘 คำสั่งเฉพาะกลุ่ม  〙
╠➣ /kill [@]
║
╚〘""" + client.getProfile().displayName +"""〙"""

def clientBot(op):
	global help
	global end
	try:
		if op.type == 0:
			if("a"=="b"):print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			if("a"=="a"):print("[ 5 ] NOTIFIED ADD CONTACT")
			try:
				clientSendW(op.param1,channelToken.token)
			except Exception as Error:
				client.sendMessage(op.param1, "THX FOR ADD ME {}".format(str(nadya.getContact(op.param1).displayName)))
				print("[ ERROR ] " + Error)
				
		if op.type == 25:
			print("[ 25 ] SEND MESSAGE")
			try:
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if "/help" == text:
							client.sendMessage(to, str(help))
						if "/picture" in text:
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									path = "http://dl.profile.line.naver.jp/{}".format(contact.pictureStatus)
									client.sendImageWithURL(to, str(path))
							else:
								path = "http://dl.profile.line.naver.jp/{}".format(client.getProfile().pictureStatus)
								client.sendImageWithURL(to, str(path))
						if "/bio" in text:
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								sh = 0
								txt = "[ LIST BIO ]"
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									sh = sh + 1
									contact = client.getContact(ls)
									txt += "\n" + str(sh) + ". " + contact.displayName + "\n{}".format(str(contact.statusMessage))
									txt += "\n"
								client.sendMessage(to,txt)
							else:
								client.sendMessage(to,client.getProfile().statusMessage)
						if "/mid" in text:
							if 'MENTION' not in msg.contentMetadata.keys()!= None:
								client.sendMessage(to, client.getProfile().displayName + ": " + clientMid)
							else:
								key = eval(msg.contentMetadata["MENTION"])
								key["MENTIONEES"][0]["M"]
								txt = "[ LIST MID ]"
								targets = []
								lh = 0
								for x in key["MENTIONEES"]:
									targets.append(x["M"])
								for target in targets:
									try:
										lh = lh + 1
										name = client.getContact(target).displayName
										txt += "\n" + str(lh) + ". " + name + ": " + str(target)
									except:
										pass
								client.sendMessage(to,txt)
						if text == '/me':
							if 'MENTION' not in msg.contentMetadata.keys()!= None:
								client.sendContact(to, clientMid)
							else:
								key = eval(msg.contentMetadata["MENTION"])
								key["MENTIONEES"][0]["M"]
								targets = []
								for x in key["MENTIONEES"]:
									targets.append(x["M"])
								for target in targets:
									try:
										client.sendContact(to, target)
									except:
										pass
						if "/kill " in text:
							key = eval(msg.contentMetadata["MENTION"])
							key["MENTIONEES"][0]["M"]
							targets = []
							for x in key["MENTIONEES"]:
								targets.append(x["M"])
							for target in targets:
								try:
									G = client.getGroup(to)
									client.updateGroup(G)
									client.kickoutFromGroup(to, [target])
								except:
									pass
			except Exception as Error:
				print("[ ERROR ] " + Error)
			

		if op.type == 26:
			if("a"=="b"):print("[ 26 ] RECEIVE MESSAGE")
		
	except Exception as error:
		print(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					print(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()

def clientSendW(param,ch):
	client.findAndAddContactsByMid(param)
	_session = requests.session()
	image = "https://lh3.googleusercontent.com/proxy/-qcXIaVI5RPLI_rZgSi8T-QyHCDuVXRoFQUksJ2tzKKOGt8vGLQ6EW7yZBO9SIpQ0b5GlZgahj8S4lENJRr2PDK7jN-vPImkR628uGfvOlr3HpSjBCWrGfCGiOsj9pT7PjH8OuZ6bZ7_9RB7tTeUcmld8U5z=w256-h256-nc"
	url = "https://game.linefriends.com/jbp-lcs-ranking/lcs/sendMessage"
	headers = {
		"Host": "game.linefriends.com",
		"Content-Type": "application/json",
		"User-Agent": "Mozilla/5.0",
		"Referer": "https://game.linefriends.com/cdn/jbp-lcs/"
	}
	jsonData = {
		"cc": ch,
		"to": param,
		"messages": [
						{
							"type": "template",
							"altText": client.getProfile().displayName + " หล่อ",
							"template": {
								"type": "carousel",
								"actions": [],
								"columns": [
									{
										"title": "THX FOR ADD ME",
										"text": "BY " + client.getProfile().displayName,
										"actions": [
													{
														"type": "uri",
														"label": "LOVE U",
														"uri": "line://ch/1341209850"
													}
										]
									}
								]
							}
						}
					]
	}
	data = json.dumps(jsonData)
	sendPost = _session.post(url, data=data, headers=headers)
	session = requests.session()
	image = "https://lh3.googleusercontent.com/proxy/-qcXIaVI5RPLI_rZgSi8T-QyHCDuVXRoFQUksJ2tzKKOGt8vGLQ6EW7yZBO9SIpQ0b5GlZgahj8S4lENJRr2PDK7jN-vPImkR628uGfvOlr3HpSjBCWrGfCGiOsj9pT7PjH8OuZ6bZ7_9RB7tTeUcmld8U5z=w256-h256-nc"
	url = "https://game.linefriends.com/jbp-lcs-ranking/lcs/sendMessage"
	headers = {
		"Host": "game.linefriends.com",
		"Content-Type": "application/json",
		"User-Agent": "Mozilla/5.0",
		"Referer": "https://game.linefriends.com/cdn/jbp-lcs/"
	}
	jsonData = {
		"cc": ch,
		"to": param,
		"messages": [
						{  
							"type": "flex",
							"altText": client.getProfile().displayName + " หล่อ",
							"contents": {
								"type": "bubble",
								"body": {
									"type": "box",
									"layout": "vertical",
									"contents": [
													{
														"type": "text",
														"text": "Contact"
													}
												]
								}
											
							}
						}
					]
	}
	data = json.dumps(jsonData)
	sendPost = _session.post(url, data=data, headers=headers)
	client.sendContact(param, client.profile.mid)
	print("[ INFO ] SUCCESS")
