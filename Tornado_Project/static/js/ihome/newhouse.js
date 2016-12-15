function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get('/api/newhouse',function(data){
        $("#area-id").html(template('areainfo', {list :data.areaList}));
    });

    $("#form-house-info").submit(function(e){
        e.preventDefault();
        console.log("preventok");

        var facility = [];
        $("input:checked[name=facility]").each(function(i){
            facility[i] = this.value;
        });

        usrChoices = {};
        $("#form-house-info").serializeArray().map(function(x){
            usrChoices[x.name] = x.value;
        });

        usrChoices["facility"] = facility;
        jsonData = JSON.stringify(usrChoices);        
        console.log(usrChoices);
        $.ajax({
            url: "/api/newhouse",
            data: jsonData,
            contentType: "application/json",
            type: "post",
            headers: {"X-XSRFTOKEN": getCookie("_xsrf")},

            success: function(data){
                console.log(data);
                if ("0" == data.erron){
                    $("#form-house-image").show();
                    $(".error-msg").html(data.errmsg);
                    $(".error-msg").show();
                    hid = data.hid
                    $("#form-house-info").hide();
                }
                else{
                    $(".error-msg").show();
                }
            }
        });

    });
    
    $("#form-house-image").submit(function(e){
        e.preventDefault();

        var options = {
            url : "/api/house/image",
            type: "post",
            headers: {"X-XSRFTOKEN": getCookie("_xsrf")},
            success: function(data){
                if ("0" == data.erron){
                    $(".popup_con").hide();
                    $(".error-msg").html(data.errmsg);
                    $(".error-msg").show();
                    
                } 
            }
        }
        $("#form-house-image").ajaxSubmit(options);
        $(".popup_con").show();

    });



});