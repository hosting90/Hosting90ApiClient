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

require_once('h90-api.php');

define('UID', 0);
define('PASSWORD', 'password');

$api = new HostingApi();
if (! $api->login(UID, PASSWORD)) {
	echo "Invalid login";
	die(1);
}

$ret = $api->domain_list();
var_dump($ret);
$ret = $api->domain_list_email_subdomain(array('domain_id'=> 123));
var_dump($ret);
$ret = $api->domain_list_email(array("email_subdomain_id"=> 1234));
var_dump($ret);
