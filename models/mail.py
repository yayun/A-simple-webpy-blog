#coding:utf-8
'''
import web
#用web的模块来实现邮件的发送
def sendmail(email):
    web.config.smtp_server = "smtp_host"
    web.config.smtp_port = 587
    web.config.smtp_username = 'user_name@gmail.com'
    web.config.smtp_password = 'psw'
    web.config.smtp_starttls = True
    subject="欢迎您注册blog  请完成以下验证"
    message="hello world"
    web.sendmail('yayunx@gmail.com',"18766964368@139.com", subject, message)
'''
def sendmail(mail):
    host="smtp.163.com"
    user="123@163.com"
    psw="123"
    import smtplib
    server=smtplib.SMTP()
    server.connect(host)
    server.ehlo()
    server.starttls()#All SMTP commands that follow will be encrypted.
    server.login(user,psw)
    server.sendmail(user,mail,"welcome yayun's blog ^^*")
    import time
    T=time.time()
    time.sleep(2.0)
    #验证gmail中是否有新邮件到达然后确认邮件是否发送成功 来判断邮件地址是否正确'''

    import imaplib,string,email
    #imap是Internet Message Access Protocol 交互邮件访问协议 可以访问到远程服务器上的邮件
    M=imaplib.IMAP4_SSL("imap.163.com")
    M.login(user,psw)
    M.select() 
    query='(UNSEEN SINCE "30-Jun-2013")'
    typ, data = M.search("utf-8", query)
    re=None
    for num in string.split(data[0]):
        typ, data=M.fetch(num,'(RFC822)')
        msg=email.message_from_string(data[0][1])
        re=msg["From"]
    if re==None:
        return "success"
    else:
        return None
    M.close()
    M.logout()
