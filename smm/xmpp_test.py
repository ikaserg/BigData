# -*- coding: utf-8 -*-
import xmpp
import StringIO

username = '574248559595'
uname = '574248559595@odnoklassniki.ru'
passwd = 'kas89105725829'
to='77820846472@odnoklassniki.ru'
msg='Привет, как дела'

user_list = []

def messageCB(sess,mess):
    print 'MESSAGE'*10
    print mess
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    #print mess.getStamp()
    #print mess,nick
    print text

def presenceCB(sess, mess):
    #print 'presence'*10
    #print mess.getFrom().node
    #print mess.getFrom().domain
    user_list.append(mess.getFrom().node)

def iqCB(sess, mess):
    print 'iq'*10
    #print mess

jid = xmpp.JID(uname)
client = xmpp.Client(jid.getDomain(), debug=[])
#client = xmpp.Client(jid.getDomain())
client.connect(server=('xmpp.odnoklassniki.ru',5222))
client.RegisterHandler('message', messageCB)

client.RegisterHandler('presence', presenceCB)
client.RegisterHandler('iq', iqCB)
client.Process(1)

client.auth(username, passwd, 'botty')
client.Process(1)

p = xmpp.Presence()
p.addChild(name='status', payload=[' '])
p.addChild(name='priority', payload=['0'])
p.addChild(name='option', namespace='http://www.odnoklassniki.ru/mark-chat-messages-read-on-exit', attrs={'value': 'false'})
client.send(p)
client.Process(1)

#client.sendInitPresence()

iq = xmpp.Iq(typ='get')
iq.addChild(name='query', namespace='http://www.odnoklassniki.ru/conversation-history-chunked',
            attrs={'jid': '77820846472@chat.odnoklassniki.ru'})
client.send(iq)

while 1:
    client.Process(1)

#p = xmpp.Presence()
#p.addChild(name='status', payload=[' '])
#p.addChild(name='priority', payload=['0'])
#p.addChild(name='option', namespace='http://www.odnoklassniki.ru/mark-chat-messages-read-on-exit', attrs={'value': 'false'})

#client.send(p)
#client.sendInitPresence(p)


#client.RegisterHandler('message',messageCB)
#client.auth(username, passwd, 'botty')


#iq = xmpp.Iq(typ='get')
#iq.addChild(name='query', namespace='http://www.odnoklassniki.ru/recent-conversations')
#client.send(iq)

#message = xmpp.Message(to, msg)


#iq = xmpp.Iq(typ='get')
#iq.addChild(name='pref', namespace='urn:xmpp:archive')

#print iq

#client.send(iq)

#client.send(message)

client.disconnect()