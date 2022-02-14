// ==UserScript==
// @name         刪除百度網盤重複文件
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @require      https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js
// @match        https://pan.baidu.com/disk/clear/list
// @icon         https://www.google.com/s2/favicons?sz=64&domain=baidu.com
// @grant        none
// ==/UserScript==
(function() {
    'use strict';

    // Your code here...
    //var testurl="/我的文档/嘉nian华/更多精彩关注微信公众号：哎生活vs爱生活.mkv";
    var bdstoken="xxx";

    setTimeout(function() {

        var testimonials = $(".choosen  a");

        for (var i = 0; i < testimonials.length; i++) {

            if (i % 2 == 1) continue;
            var url=$(testimonials[i + 1]).attr('title').trim() + "/" + $(testimonials[i]).attr('title').trim();
            //console.log(url);
            //setInterval(function() {
                //var now = new Date();
                delfile(url);

            //}, 5000);

            //$(".module-history-list").append(url);

        }

    }, 5000);
    function delfile(f){
        console.log(f);
        $.ajax({
            url:"https://pan.baidu.com/api/filemanager?opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken="+bdstoken+"&logid=RTQ4QjY3QTVFQjkxNkE4NjMzM0RDMzM3RDlFRTk5NDg6Rkc9MQ==&clienttype=0",
            type:'POST',
            async:false,
            data:{
                filelist:'["'+f+'"]'
	},
	dataType:'json',
	timeout:6666,
	success:function(resultObj){
        console.log(resultObj);
	}
});
    }
function getCookie(e) {
        var o, t;
        var n = document, c = decodeURI;
        return n.cookie.length > 0 && (o = n.cookie.indexOf(e + "="), -1 != o) ? (o = o + e.length + 1, t = n.cookie.indexOf(";", o), -1 == t && (t = n.cookie.length), c(n.cookie.substring(o, t))) : "";
    }
})();
