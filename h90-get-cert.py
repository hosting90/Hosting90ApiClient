import urllib,requests,json
import sys, re, signal, os
import logging

class HostingApi(object):
	def __init__(self, url, sid = None,fn = None):
		self.sid = sid
		self.fn = fn
		self.url = url
	
	def __getattr__(self, name):
		attr = type(self)(self.url,self.sid, name)
		
		return attr.__call__
	
	def __call__(self,**kwargs):
		"""docstring for __call"""
		if self.fn == None:
			return None
		if self.sid != None:
			kwargs['sid'] = self.sid
		if 'post' in kwargs:
			post_args = kwargs['post']
			del kwargs['post']
		else:
			post_args = None
		myurl = self.url+'/'+self.fn+'?reply=json&'+urllib.urlencode(kwargs)
		if post_args == None:
			u = requests.get(myurl)
			text = u.content
		else:
			u = requests.post(myurl, data=post_args)
			text = u.content
		
		ret = json.loads(text)
		
		if ret['reply']['status']['code'] == 0:
			del(ret['reply']['status'])
			return ret['reply']
		else:
			raise Exception((ret['reply']['status']['code'], ret['reply']['status']['text']))
	
	def logout(self):
		self.fn = 'logout'
		ret = self.__call__(sid=self.sid)
		self.sid = None
		return ret
	
	def login(self,uid,password):
		self.fn = 'login'
		self.sid = None
		ret = self.__call__(uid=uid,password=password)
		
		self.sid = ret['sid']
		return self
	
	def login_callback(self,login,callback_hash):
		self.fn = 'login_callback'
		self.sid = None
		ret = self.__call__(login=login,password=callback_hash)
		
		self.sid = ret['sid']
		return self

if __name__ == "__main__":
	import getopt
	import sys
	try:
		opts, args = getopt.getopt(sys.argv[1:], "u:p:k:c:bd:", ["username=","password=","keyout=","certout=","onchange=","callbacklogin","domain=","cn="])
	except:
		logging.error(getopt.GetoptError)
		sys.exit(1)
	
	username = None
	password = None
	keyout = None
	certout = None
	onchange = None
	domain = None
	cn = None
	callback_login = False
	
	for opt, arg in opts:
		if opt in ('-u','--username'):
			username = arg
		elif opt in ('-p','--password'):
			password = arg
		elif opt in ('-k','--keyout'):
			keyout = arg
		elif opt in ('-c','--certout'):
			certout = arg
		elif opt in ('-d','--domain'):
			domain = arg
		elif opt in ('--cn'):
			cn = arg
		elif opt in ('--onchange',):
			onchange = arg
		elif opt in ('-b','callbacklogin'):
			callback_login = True
		else:
			raise ValueError('Invalid opt %s %s' % (opt,arg))
	
	api = HostingApi('https://administrace.hosting90.cz/api')
	
	if callback_login:
		api.login_callback(username,password)
	else:
		api.login(username,password)
	try:
		domain = filter(lambda x: x['name'] == domain,api.domain_list()['domains'])[0]
	except:
		raise
	if cn is not None:
		cert = api.domain_certificate(domain_id=domain['domain_id'],cn=cn)['certificate']
	else:
		cert = api.domain_certificate(domain_id=domain['domain_id'])['certificate']
	if cert['certificate'][-1] != '\n':
		cert['certificate'] = cert['certificate'] + '\n'
	if cert['private_key'][-1] != '\n':
		cert['private_key'] = cert['private_key'] + '\n'
	changed = True

	if os.path.exists(keyout) and os.path.exists(certout):
		if keyout != certout:
			if open(certout).read().strip() == cert['certificate'].strip() and open(keyout).read().strip() == cert['private_key'].strip():
				changed = False
		else:
			if open(keyout).read().strip() ==  (cert['certificate'] + cert['private_key']).strip():
				changed = False 
	if changed:
		if keyout != certout:
			fh = open(certout,'w')
			fh.write(cert['certificate'])
			fh.close()
			fh = open(keyout,'w')
			fh.write(cert['private_key'])
			fh.close()
		else:
			fh = open(keyout,'w')
			fh.write(cert['certificate'])
			fh.write(cert['private_key'])
			fh.close()
		if onchange != None:
			import subprocess
			subprocess.check_call(onchange,shell=True)
	
		