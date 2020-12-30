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