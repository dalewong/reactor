function showSuccessMsg() {
    $(".popup_con").fadeIn("fast", function() {
        setTimeout(function(){
            $(".popup_con").fadeOut("fast",function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $("#form-auth").submit(function(e){
        e.preventDefault();
        realName = $("#real-name").val();
        idCard   = $("#id-card").val();

        if (realName == null){
            $(".error-msg").show();
            return
        }

        if (idCard == null){
            $(".error-msg").show();
            return
        }

        $(".error-msg").hide();

        para = {
            realName: realName,
            idCard:   idCard
        }

        $.ajax({
            url: "/api/auth",
            data: JSON.stringify(para),
            contentType: "application/json",
            dataType: "json",
            type: "post",
            headers: {"X-XSRFTOKEN" : getCookie("_xsrf")},
            success: function(data){

                if ("0" == data.erron){
                    $(".error-msg").html(data.errmsg);
                    $(".error-msg").show();
                } 
                else{
                    $(".error-msg").show();
                }

                setInterval(function(){
                    window.location.href =  "my.html";
                },1000);

                
            }



        });  
    });  
});