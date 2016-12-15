function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){

    para = {
        strings:1,
    }

    $.ajax({
        url:'api/local',
        contentType:'applicatin/json',
        dataType: 'json',
        data: JSON.stringify(para),
        type: 'post',
        headers: 
            {
                "X-XSRFTOKEN": getCookie("_xsrf")
            },

        success: function(data){
            
            if  ("0" == data.erron){
                // console.log(data.errmsg.uname);
                $("#user-name").html(data.errmsg.uname);
                $("#user-mobile").html(data.errmsg.umobile);
                $("#user-avatar").attr("src",data.errmsg.uavatar);
            }
            
            
            if  ("4101" == data.errno){
                window.location.href = data.errsmg;
            }

        }

    });
});