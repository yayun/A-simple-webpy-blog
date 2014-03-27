#coding:utf-8
import web
from web import form
from web.contrib.template import render_jinja
from models import db,mail
    
urls=(
    '/','index',
    '/register','register',
    '/login','log',
    '/logout','logout',
    '/new','create_post'
        )
app=web.application(urls,globals())
#不可以在调试模式下使用sessionweb.config.debug=False
#session = web.session.Session(app, web.session.DiskStore('sessions'),initializer = {'name': None})
#如果非要在调试模式下使用session
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'name': None})
    web.config._session = session
else:
    session = web.config._session

render=render_jinja('templates',encoding='utf-8',globals={'session':session})# 使用webpy 内置的模板引擎 :render=web.template.render("templates",base="base")

#首页显示
class index(object):
    def GET(self):
        articles = web.ctx.orm.query(db.article).order_by(article.id)
        article_num=len(articles)
        '''title=[]
        time=[]
        content=[]
        author=[]
        tag=[]
        for i in articles:
            title.append(i.title)
            content.append(i.content)
            time.append(i.post_time)
            author.append(i.author)
            tag.append(i.tag)'''
        return render.index(article_list=articles)
       
#注册
class register(object):
    uname=form.regexp(r".","用户名不能为空")
    psw=form.regexp(r".{3,20}$","必须是3到20个字符")
    email=form.regexp(r".*@.*","请填入有效的邮件地址")
    register_form=form.Form(
    form.Textbox("username",uname,description="用户名"),
    form.Textbox("email",email,description="邮箱地址"),
    form.Password("password",psw,description="密码"),
    form.Password("password2",description="再次输入密码"),
    form.Button("submit",type="submit",description="register"),
    validators = [
            form.Validator("两次输入的密码不相同", lambda i: i.password == i.password2),
            ])
    #form.Validator("用户名已存在",lambda i: db.validate_name(i.username)==None)
    register="register"
    def GET(self):
        f=self.register_form()
        return render.register(form=f,re_log=self.register)
    def POST(self):
        f=self.register_form()
        if not f.validates():
            return render.register(form=f,re_log=self.register)
        if  web.ctx.orm.query(db.user).filter_by(user_name=f.d.username)!=None:
            return render.register(msg=u"用户名已经存在",form=f,re_log=self.register) 
        if web.ctx.orm.query(db.user).filter_by(email=f.d.email)!=None:
            return render.register(msg=u"邮箱已经被占用",form=f,re_log=self.register) 
        re=mail.sendmail(f.d.email) 
        if re==None:
            return render.register(msg=u"对不起 我们找不到你填入的邮箱地址 请输入有效的邮箱地址",form=f,re_log=self.register)
        else :
            user_add=db.user()
            user_add.user_name=f.d.username
            user_add.psw=f.d.password
            user_add.email=f.d.email
            web.ctx.orm.add(user_add)
            return render.register(msg=u"注册成功，赶快完成登录吧 ^^*",form=f,re_log=self.register)

class log(object):
    uname=form.regexp(r".","用户名不能为空")
    psw=form.regexp(r".","密码不能为空")
    log_form=form.Form(
    form.Textbox("username",uname,description="用户名"),
    form.Password("password",psw,description="密码"),
    form.Button("submit",type="submit",description="register"),
    )
    log="log"
    def GET(self):
        f=self.log_form()
        return render.register(form=f,re_log=self.log)
    def POST(self):
        f=self.log_form()
        if not f.validates():
            return render.register(form=f,re_log=self.log)
        if web.ctx.orm.query(db.user).filter_by(user_name=f.d.username,psw=f.d.password)==None:
            return render.register(msg=u"用户名或密码错误",form=f,re_log=self.log)
        else:
            session.name=f.d.username
            raise web.SeeOther("/")

class logout(object):
    def GET(self):
        session.kill()
        return render.index()

class create_post(object):
    titlexp=form.regexp(r".","标题不能为空")
    contentexp=form.regexp(r".","内容不能位空")
    tagexp=form.regexp(r'.',"标签不能为空")
    post_form = form.Form(
        form.Textbox('title', titlexp,size=30,description="Post title:"),
        form.Textarea('content', contentexp, rows=10, cols=30, description="Post content:"),
        form.Textbox('tag',tagexp, size=30, description="tag"),
        form.Button("submit",type="submit",description="register")
    )

    def GET(self):
        f= self.post_form()
        return render.new_post(form=f)

    def POST(self):
        f= self.post_form()
        if not f.validates():
            return render.new_post(form=f)
        if session.name==None:
            return render.new_post(post_err=u"对不起你没有",form=f)
        else:
            add_post=db.article()
            add_post.title=f.d.title
            add_post.content=f.d.content
            add_post.tag=f.d.tag
            add_post.author=session.name
            web.ctx.orm.add(add_post)
            raise web.SeeOther("/")


if __name__=='__main__':
    app.run()

'''
使用gunicorn 来serve
application = app.wsgifunc()
'''
