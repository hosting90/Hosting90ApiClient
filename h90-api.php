<?php
	/*
	The MIT License (MIT)

	Copyright (c) 2015 HOSTING90 systems s.r.o.

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
	*/
	
	define('HAPI_URL','https://administrace.hosting90.cz/api');
	define('HAPI_USE_CURL', true);
	
	/**
	* 
	*/
	class HostingApi
	{
		private $sid;
		function __construct()
		{
			$this->sid = null;
		}
		
		function __call($name, $params)
		{
			$url = HAPI_URL.'/'.$name.'?reply=json';
			if (count($params)) {
				if (count($params) !== 1 || !is_array($params[0])) {
					return false;
				}
				foreach ($params[0] as $key => $value) {
					$url .= '&'.urlencode($key).'='.urlencode((string)$value);
				}
			}
			if ($this->sid) {
				$url .= '&sid='.$this->sid;
			}
			if (HAPI_USE_CURL) {
				$ch = curl_init($url);
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
				curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
				$text = curl_exec($ch);
				curl_close($ch);
			} else {
				$text = file_get_contents($url);
			}
			$ret = json_decode($text);
			if (is_object($ret) && isset($ret->reply)) {
				return $ret->reply;
			} else {
				return false;
			}
		}

		function login($uid, $password)
		{
			$ret = $this->__call('login', array(array('uid' => $uid, 'password' => $password)));
			if ($ret && $ret->status->code == 0) {
				$this->sid = $ret->sid;
				return true;
			} else {
				return false;
			}

		}
	}
	