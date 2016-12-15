function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    para = {
        fire: "b",
    }

    $.ajax({
        url:"/api/local",
        contentType:"applicatin/json",
        dataType: "json",
        data: JSON.stringify(para),
        type: "post",
        headers: 
            {
                "X-XSRFTOKEN": getCookie("_xsrf")
            },

        success: function(data){
            
            if  ("0" == data.erron){              
                $("#user-avatar").attr("src",data.errmsg.uavatar);
            }       
    
        }
    });


    $("#form-avatar").submit(function(e){
        console.log('haha');
        e.preventDefault();
        console.log('hehe');
        var options = {
            url: "/api/profile/avatar",
            type: "post",
            headers: {"X-XSRFTOKEN" : getCookie("_xsrf")},
            success: function(data){
                if ("0" == data.erron){
                    $("#user-avatar").attr("src", data.errmsg);
                } 
            }
        }
        $("#form-avatar").ajaxSubmit(options);

    });    
    
    $("#form-name").submit(function(e){
        var uname = $("#user-name").val();
        e.preventDefault();
        if (uname != null){
                para = {
                    usrname : uname,
                }
                
                $.ajax({
                    url : "/api/namemodify",
                    data: JSON.stringify(para),
                    type: "post",
                    dataType: "json",
                    contentType: "application/json",
                    headers: {"X-XSRFTOKEN": getCookie("_xsrf")},
                    success: function(data){                        
                        $(".error-msg").html(data.errmsg);
                        $(".error-msg").show();
                        
                    }

                });
                
            }
    })

    

    

});

