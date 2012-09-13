""" RUM script injection helper methods

Copyright (C) 2012 by Tracelytics, Inc.
All rights reserved.
"""

import oboe

def header():
    cid = "CUSTOMERID"
    xid = str(oboe.Context.get_default())
    return r'''(function(){var e=this._tly={q:[],mark:function(a,b){e.q.push(["mark",a,b||(new Date).getTime()])},measure:function(a,b,c){e.q.push(["measure",a,b,c||(new Date).getTime()])},done:function(a){e.q.push(["done",a])},cid:"''' + customer_id + r'''",xt:"''' + xid + r'''"};e.mark("firstbyte");var f;f=function(){};var g=0;function h(a){return function(b){b[a]||(b[a]=!0,e.measure(["_ajax",b.a,a]))}}var i=h("recv"),j=h("send");
function l(){var a=this&&this._tl,b=a.b;4===this.readyState&&i(a);f();for(a=0;a<b.length;a++)b[a].apply(this,arguments)}var m=this.XMLHttpRequest,n=m&&m.prototype;
if(n){var o=n.open;n.open=function(a,b,c,d,r){f();this._tl||(this._tl={a:g++,async:c,b:[]},e.measure(["_ajax",this._tl.a,"init",a,b]));return d?o.call(this,a,b,c,d,r):o.call(this,a,b,c)};var p=n.send;n.send=function(a){function b(){try{var a;a:{var b=l;try{if(c.addEventListener){c.addEventListener("readystatechange",b);a=!0;break a}}catch(t){}a=!1}if(!a){var k=c.onreadystatechange;if(k){if(!k.apply)return;f();d.b.push(k)}f();c.onreadystatechange=l}}catch(u){}}var c=this,d=c&&c._tl;f();b();j(d);a=
p.call(c,a);!d.async||4===c.readyState?i(d):setTimeout(function(){try{4===c.readyState?i(d):c.onreadystatechange!==l&&b()}catch(a){}},0);return a}}this.onerror=function(a,b,c){e.measure(["_jserror ",a,"|",b,"|",c].join(""))};var q=document.createElement("script");q.type="text/javascript";q.async=!0;q.src="http://rumcdn.tlys.us/tly.js";var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(q,s);}());'''

def footer():
    return r'''this._tly&&this._tly.measure("domload");'''
