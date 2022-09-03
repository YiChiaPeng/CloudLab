function do_login() {
    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {
            uId: $("#username"). val(),
            uPassword: $("#password"). val()
        },
        contentType: "application/json; charset=utf-8", // this
        dataType: "json", // and this
        success: function(response) {
            console.log(response);
            if (response.success == 't'){
                alert("登入成功");
                
            }
            else {
                alert("登入失敗");
            }
        }
    })
}