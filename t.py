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

xas = client

def clientBot(op):
	global end
	try:
		if op.type == 0:
			end = end + 1
			print ("[ 0 ] END OF OPERATION [ " + str(end) + " ]")
			return

		if op.type == 5:
			print("[ 5 ] NOTIFIED ADD CONTACT")
			client.findAndAddContactsByMid(op.param1)
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
												"title": "THX FOR @ ME",
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
														"text": "Contact me"
													}
												]
											}
											
										}
									}
								]
							}
			data = json.dumps(jsonData)
			sendPost = _session.post(url, data=data, headers=headers)
			#client.sendMessage(op.param1, "CONTACT ME")
			client.sendContact(op.param1, client.profile.mid)
			
		if op.type == 25:
			try:
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = text.lower()
				if msg.contentType == 7:
					print("[ 25 ] SEND MESSAGE [ TO: " + client.getGroup(receiver).name + " ] [ STKID: " + msg.contentMetadata['STKID'] +" ]")
				else:
					print("[ 25 ] SEND MESSAGE [ TO: " + client.getGroup(receiver).name + " ] [ TEXT: " + cmd +" ]")
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
						#ret_ = "[[ POST DETAIL ]]"
						if msg.contentMetadata["serviceType"] == "GB":
							contact = client.getContact(sender)
							auth = "[ POST AUTHOR ]\n{}".format(str(contact.displayName))
						else:
							auth = "[ POST AUTHOR ]\n{}".format(str(msg.contentMetadata["serviceName"]))
						purl = "\n[ POST URL ]\n{}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
						ret_ = auth
						ret_ += purl
						if "mediaOid" in msg.contentMetadata:
							object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
							if msg.contentMetadata["mediaType"] == "V":
								if msg.contentMetadata["serviceType"] == "GB":
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
									murl = "\n[ MEDIA URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
								else:
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									murl = "\n[ MEDIA URL]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
								ret_ += murl
							else:
								if msg.contentMetadata["serviceType"] == "GB":
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
								else:
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
							ret_ += ourl
						if "stickerId" in msg.contentMetadata:
							stck = "\n[ POST STICKER ]\nhttps://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
							ret_ += stck
						if "text" in msg.contentMetadata:
							text = "\n[ POST TEXT ]\n{}".format(str(msg.contentMetadata["text"]))
							ret_ += text
						ret_ += "\n\n" + client.getProfile().displayName
						client.sendMessage(to, ret_)#"[ URL POST ]\n" + msg.contentMetadata["postEndUrl"])
					if msg.contentType == 0:
						if "/ti/g/" in msg.text.lower():
							link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
							links = link_re.findall(text)
							n_links = []
							for l in links:
								if l not in n_links:
									n_links.append(l)
							for ticket_id in n_links:
								group = client.findGroupByTicket(ticket_id)
								client.acceptGroupInvitationByTicket(group.id,ticket_id)
								client.sendMessage(to, "Joined %s" % str(group.name))
						if cmd.startswith("/spamcall: "):
							proses = text.split(":")
							strnum = text.replace(proses[0] + ":","")
							jmlh =  int(strnum)
							group = client.getGroup(to)
							members = [mem.mid for mem in group.members]
							if jmlh <= 1000:
								for x in range(jmlh):
									try:
										client.acquireGroupCallRoute(to)
										client.inviteIntoGroupCall(to, contactIds=members)
									except Exception as e:
										client.sendMessage(to,str(e))
							else:
								client.sendMessage(to,"Limit")
							client.sendMessage(to,"Spam total " + str(jmlh))
							
						if cmd.startswith("/yt"):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "[ Youtube Search ]"
								for anu in data["videos"]:
									no += 1
									result += "\n{}. {}".format(str(no),str(anu["title"]))
								result += "\n" + client.getProfile().displayName
								client.sendMessage(to, result)
						if cmd == "/picture":
							contact = client.getContact(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						if cmd == "/mention":
							group = client.getGroup(msg.to)
							nama = [contact.mid for contact in group.members]
							k = len(nama)//100
							for a in range(k+1):
								txt = u''
								s=0
								b=[]
								shi=1
								shix=0
								mem = 0
								for i in group.members[a*100 : (a+1)*100]:
									b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
									mem = mem + 1
									shix = shix + 1
									s += 7
									shi= shi + 1
									txt += u'@Alin \n'
									if shix > 12:
										client.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
										txt = u''
										b=[]
										s=0
										shix = 0
								client.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
								client.sendMessage(to, "Total " + str(mem) + " members")
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
														"text": "Leave the chat to read the message."
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
												},
												{
													"thumbnailImageUrl": "https://www.clipmass.com/upload/news/23/22373_full.gif",
													"title": client.getProfile().displayName + " ( PRIVATE 2 )",
													"text": "/picture, /spamcall: [number], /yt [text], /speed",
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
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = text.lower()
				if msg.contentType == 7:
					print("[ 26 ] RECEIVE MESSAGE [ SENDER: " + client.getContact(sender).displayName + " ] [ STKID: " + msg.contentMetadata['STKID'] +" ]")
				elif(cmd != "none"):
					print("[ 26 ] RECEIVE MESSAGE [ SENDER: " + client.getContact(sender).displayName + " ] [ TEXT: " + cmd +" ]")
				else:
					print("[ 26 ] RECEIVE MESSAGE [ SENDER: " + client.getContact(sender).displayName + " ] [ TEXT: UNKNOW ]")
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
						#ret_ = "[[ POST DETAIL ]]"
						if msg.contentMetadata["serviceType"] == "GB":
							contact = client.getContact(sender)
							auth = "[ POST AUTHOR ]\n{}".format(str(contact.displayName))
						else:
							auth = "[ POST AUTHOR ]\n{}".format(str(msg.contentMetadata["serviceName"]))
						purl = "\n[ POST URL ]\n{}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
						ret_ = auth
						ret_ += purl
						if "mediaOid" in msg.contentMetadata:
							object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
							if msg.contentMetadata["mediaType"] == "V":
								if msg.contentMetadata["serviceType"] == "GB":
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
									murl = "\n[ MEDIA URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
								else:
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									murl = "\n[ MEDIA URL]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
								ret_ += murl
							else:
								if msg.contentMetadata["serviceType"] == "GB":
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
								else:
									ourl = "\n[ URL OBJECT ]\nhttps://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
							ret_ += ourl
						if "stickerId" in msg.contentMetadata:
							stck = "\n[ POST STICKER ]\nhttps://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
							ret_ += stck
						if "text" in msg.contentMetadata:
							text = "\n[ POST TEXT ]\n{}".format(str(msg.contentMetadata["text"]))
							ret_ += text
						ret_ += "\n\n" + client.getProfile().displayName
						client.sendMessage(to, ret_)#"[ URL POST ]\n" + msg.contentMetadata["postEndUrl"])
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
						if 'MENTION' in msg.contentMetadata.keys() != None:
							if msg.toType != 0 and msg.toType == 2:
								name = re.findall(r'@(\w+)', msg.text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								for mention in mentionees:
									if clientMid in mention["M"]:
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
																"text": "Contact me as a private chat."
															}
														]
													}
													
												}
											}
										]
										}
										data = json.dumps(jsonData)
										sendPost = _session.post(url, data=data, headers=headers)
										client.sendContact(to, client.profile.mid)
										break
						if "/ti/g/" in msg.text.lower():
							link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
							links = link_re.findall(text)
							n_links = []
							for l in links:
								if l not in n_links:
									n_links.append(l)
							for ticket_id in n_links:
								group = client.findGroupByTicket(ticket_id)
								client.acceptGroupInvitationByTicket(group.id,ticket_id)
								client.sendMessage(to, "Joined %s" % str(group.name))
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
