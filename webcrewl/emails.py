# -*- coding: utf-8 -*-

import smtplib  
from email.mime.text import MIMEText
from scrapy.conf import settings

mailto_list=['86905901@qq.com'] 
mail_host="smtp.qq.com"  #设置服务器
mail_user="14907232@qq.com"    #用户名
mail_pass="aaaaaaaaaaaaaa"   #口令 
mail_postfix="qq.com"  #发件箱的后缀
  
def send_mail(sub,content, href):  
    me="水木社区"+"<"+mail_user+"@"+mail_postfix+">"
    content += '<br/><a href="%s%s">原帖<%s></a>'%(settings['ROOT_URL'],href, sub)
    
    msg = MIMEText(content,_subtype='html',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(mailto_list)
    
    try:  
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.set_debuglevel(1)
        server.login(mail_user,mail_pass)  
        server.sendmail(me, mailto_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:
        print str(e)  
        return False 
