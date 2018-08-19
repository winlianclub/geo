# -*- coding: utf-8 -*-

from line.linepy import *
import json, requests, sys, time

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

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 25:
			try:
				print("[ 26 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = text.lower()
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
					if msg.contentType == 16:
						msg.contentType = 0
						client.sendMessage(to,"[ URL POST ]\n" + msg.contentMetadata["postEndUrl"] + "\n" + client.getProfile().displayName)
					if msg.contentType == 0:
						if cmd == "/mention":
							group = client.getGroup(msg.to)
							nama = [contact.mid for contact in group.members]
							k = len(nama)//100
							for a in range(k+1):
								txt = u''
								s=0
								b=[]
								shi=1
								for i in group.members[a*100 : (a+1)*100]:
									b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
									s += 7
									shi= shi + 1
									txt += u'@Alin \n'
								client.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
						if cmd == "/speed":
							start = time.time()
							client.sendMessage(to, "loading... [1/2]")
							elapsed_time = time.time() - start
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
								"to": to,
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
														"text": str(elapsed_time) + " [1/2]"
													}
												]
											}
											
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
							start = time.time()
							client.sendMessage(to, "loading... [2/2]")
							elapsed_time = time.time() - start
							client.sendMessage(to,format(str(elapsed_time)) + " [2/2]")
						if cmd == "/me":
							client.sendMessage(to, client.getProfile().displayName)
							client.sendContact(to, client.profile.mid)
						if cmd.startswith("/info"):
							key = eval(msg.contentMetadata["MENTION"])
							key1 = key["MENTIONEES"][0]["M"]
							contact = client.getContact(key1)
							try:
								text = "Name\n" + contact.displayName + "\n\nMid\n" + contact.mid + "\n\nStatus\n" + contact.statusMessage + "\nProfile\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n" + client.getProfile().displayName
							except:
								text = "Name\n" + contact.displayName + "\n\nMid\n" + contact.mid + "\n\nStatus\n" + contact.statusMessage + "\n\n" + client.getProfile().displayName
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
								"to": to,
								"messages": [
									{  
										"type": "text",
										"altText": "คนส่งข้อความหล่อ",
										"text":text
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
							
						if cmd == "/mid":
							client.sendMessage(to, client.getProfile().displayName + "\n" +  client.profile.mid)
						if cmd.startswith("/invisibletext"):
							sep = cmd.split(" ")
							sepx = cmd.replace(sep[0] + " ","")
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
								"to": to,
								"messages": [
									{  
										"type": "flex",
										"altText": sepx,
										"contents": {
											"type": "bubble",
											"body": {
												"type": "box",
												"layout": "vertical",
												"contents": [
													{
														"type": "text",
														"text": "This is invisible text"
													}
												]
											}
											
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd.startswith("/text"):
							sep = cmd.split(" ")
							sepx = cmd.replace(sep[0] + " ","")
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
								"to": to,
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
														"text": sepx
													}
												]
											}
											
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd == "/help2":
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
								"to": to,
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
														"text": "/me"
													},
													{
														"type": "text",
														"text": "/mid"
													},
													{
														"type": "text",
														"text": "/invisibletext [text]"
													},
													{
														"type": "text",
														"text": "/text [text]"
													},
													{
														"type": "text",
														"text": "/mention"
													},
													{
														"type": "text",
														"text": "By " + client.getProfile().displayName
													}
												]
											}
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd == "/list":
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
								"to": to,
								"messages": [
									{
										"type": "template",
										"altText": client.getProfile().displayName + " หล่อ",
										"template": {
											"type": "carousel",
											"actions": [],
											"columns": [
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"title": client.getProfile().displayName + " ()",
													"text": "List ",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												}
												#{
												#	"title": client.getProfile().displayName + " ( PAGE 2 )",
												#	"text": "none",
												#	"actions": [
												#		{
												#			"type": "uri",
												#			"label": "Contact",
												#			"uri": "https://line.me/R/ti/p/~esci_"
												#		}
												#	]
												#},
											]
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd == "/help":
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
								"to": to,
								"messages": [
									{
										"type": "template",
										"altText": client.getProfile().displayName + " หล่อ",
										"template": {
											"type": "carousel",
											"actions": [],
											"columns": [
												{
													"thumbnailImageUrl": "https://www.clipmass.com/upload/news/23/22373_full.gif",
													"title": client.getProfile().displayName + " ( PUBLIC )",
													"text": "/text [text]",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												},
												{
													"thumbnailImageUrl": "https://www.clipmass.com/upload/news/23/22373_full.gif",
													"title": client.getProfile().displayName + " ( PRIVATE 1 )",
													"text": "/me, /mid ,/mention, /text [text], /invisibletext [text]",
													"actions": [
														{
															"type": "uri",
															"label": "Contact",
															"uri": "https://line.me/R/ti/p/~esci_"
														}
													]
												}
												#{
												#	"title": client.getProfile().displayName + " ( PAGE 2 )",
												#	"text": "none",
												#	"actions": [
												#		{
												#			"type": "uri",
												#			"label": "Contact",
												#			"uri": "https://line.me/R/ti/p/~esci_"
												#		}
												#	]
												#},
											]
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd == "test":
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
								"to": to,
								"messages": [
									  {
											"type": "template",
											"altText": "",
											"template": {
												"type": "image_carousel",
												"columns": [
													{
														"imageUrl": "https://static-cdn.jtvnw.net/jtv_user_pictures/e91a3dcf-c15a-441a-b369-996922364cdc-profile_image-300x300.png",
														"action": {
															"type": "uri",
															"uri": "https://static-cdn.jtvnw.net/jtv_user_pictures/e91a3dcf-c15a-441a-b369-996922364cdc-profile_image-300x300.png"
														}
													}
												]
											}
										}
								]
							}
							data = json.dumps(jsonData) 
							sendPost = _session.post(url, data=data, headers=headers)
							
			except Exception as error:
				print(error)
		if op.type == 26:
			try:
				print("[ 26 ] RICIEVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = text.lower()
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
					if msg.contentType == 16:
						msg.contentType = 0
						client.sendMessage(to,"[ URL POST ]\n" + msg.contentMetadata["postEndUrl"] + "\n" + client.getProfile().displayName)
					if msg.contentType == 0:
						if cmd.startswith("/text"):
							sep = cmd.split(" ")
							sepx = cmd.replace(sep[0] + " ","")
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
								"to": to,
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
														"text": sepx
													},
													{
														"type": "text",
														"text": "From " + client.getContact(sender).displayName
													}
												]
											}
											
										}
									}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
						if cmd == "xximage coursel":
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
								"to": to,
								"messages": [
									  {
											"type": "template",
											"altText": "",
											"template": {
												"type": "image_carousel",
												"columns": [
													{
														"imageUrl": image,
														"action": {
															"type": "uri",
															"uri": image
														}
													}
												]
											}
										}
								]
							}
							data = json.dumps(jsonData)
							sendPost = _session.post(url, data=data, headers=headers)
			except Exception as error:
				print(error)
		
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
