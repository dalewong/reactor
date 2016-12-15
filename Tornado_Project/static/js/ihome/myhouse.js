$(document).ready(function(){

    $.get("/api/myhouse",function(data){
        console.log(data);
        var usrdata = {
            list : data.errmsg,
        }
        console.log(template("house-info",usrdata));
        $(".houses-list a").after(template("house-info",usrdata));
    });
    
    
})

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}