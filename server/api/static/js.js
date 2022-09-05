
function do_login() {
    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {
            uId: $("#username"). val(),
            uPassword: $("#password"). val()
        },
        success: function(response) {
            console.log(response);
            if (response.success == 't'){
                alert("登入成功");
                document.cookie = ("access_token_cookie=" + response.jwt_token);
                window.location.href = '/remote';
            }
            else {
                alert("登入失敗");
            }
        }
    })
}