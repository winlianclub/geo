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
				with open("authToken2.txt", "r") as token:
					authToken = token.read().replace("\n","")
					if not authToken:
						client = LINE()
						with open("authToken2.txt","w") as token:
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

with open("authToken2.txt", "w") as token:
    token.write(str(client.authToken))
channel = Channel(client, client.server.CHANNEL_ID['JUNGEL_PANG'])
channelToken = channel.getChannelResult()
clientMid = client.profile.mid
clientPoll = OEPoll(client)

sunmid = "u541bbaba15d68f3a652106a0de5a3e94"

help = """╔〘""" + client.getProfile().displayName +"""〙
║
╠═✪〘 ข้อความช่วยเหลือ  〙
╠➣ /logout
╠✪〘 คำสั่งปกติ 〙
╠➣ /me (@)
╠➣ /mid (@)
╠➣ /picture (@)
╠➣ /bio (@)
╠➣ /yt [txt]
║
╠✪〘 คำสั่งเฉพาะกลุ่ม  〙
╠➣ /kill [@]
║
╠✪〘 คำสั่งพิเศษ  〙
╠➣ sun
║
╚〘""" + client.getProfile().displayName +"""〙"""

def clientBot(op):
	global help
	global end
	global sunmid
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print("[ 5 ] NOTIFIED ADD CONTACT")
			try:
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
					"cc": channelToken.token,
					"to": op.param1,
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
					"cc": channelToken.token,
					"to": op.param1,
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
				client.sendContact(op.param1, client.profile.mid)
				print("[ INFO ] SUCCESS")
			except Exception as Error:
				client.sendMessage(op.param1, "THX FOR ADD ME {}".format(str(client.getContact(op.param1).displayName)))
				print("[ ERROR ] " + Error + " AND SEND RESRVE MESSAGE TO " + client.getContact(op.param1).displayName)
				
		if op.type == 13:
			if op.param2 in sunmid:
				client.acceptGroupInvitation(op.param1)
				
		if op.type == 19:
			client.inviteIntoGroup(op.param1,[sunmid])
				
		if op.type == 18:
			client.inviteIntoGroup(op.param1,[sunmid])
				
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
						if "sun" in text:
							client.inviteIntoGroup(to,[sunmid])
							print("[ INV SENT ]")
						if "/help" == text:
							client.sendMessage(to, str(help))
						if "/picture" in text:
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								txt = "[ LIST PICTURE ]"
								lh = 0
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									lh = lh + 1
									contact = client.getContact(ls)
									txt += "\n" + str(sh) + ". " + "{t}: http://dl.profile.line.naver.jp/{n}".format(n=contact.pictureStatus,t=contact.displayName)
								client.sendMessage(to, txt)
							else:
								path = "http://dl.profile.line.naver.jp/{}".format(client.getProfile().pictureStatus)
								client.sendMessage(to, txt)
						if text.startswith("/yt "):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╔══〘 Youtube Search 〙"
								for anu in data["videos"]:
									no += 1
									result += "\n╠ {}. {}\n║Link: {}".format(str(no),str(anu["title"]),str(anu["webpage"]))
								result += "\n╚══〘 Total {} Result 〙".format(str(len(data["videos"])))
								client.sendMessage(to, result)
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
						if text == "/logout":
							client.sendMessage(to, "SHUT DOWN")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
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
						"""if "/rm chat" in text:
							try:
								client.removeAllMessages(op.param2)
								client.sendMessage(to, "Removed chat")
							except:
								pass
						"""
						if "/kill" in text:
							key = eval(msg.contentMetadata["MENTION"])
							key["MENTIONEES"][0]["M"]
							targets = []
							for x in key["MENTIONEES"]:
								targets.append(x["M"])
							for target in targets:
								try:
									G = client.getGroup(to)
									G.preventedJoinByTicket = False
									client.updateGroup(G)
									gurl = client.reissueGroupTicket(to)
									client.kickoutFromGroup(to, [target])
									client.sendMessage(client.getContact(target).mid, "http://line.me/R/ti/g/"+gurl + "\n[ THIS IS TEST KICK ]")
									client.inviteIntoGroup(to, [target])
								except:
									pass
			except Exception as Error:
				print("[ ERROR ] " + Error)
			

		if op.type == 26:
			print("[ 26 ] RECEIVE MESSAGE")
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
						if "/bx" in text:
							if sender == sunmid:
								client.leaveGroup(to)
			
			except Exception as Error:
				print("[ ERROR ] " + Error)
							
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
