function do_addCourse() {
    var token = document.cookie.split(";" )[0];
    var currentCookie = token.split("=")[1];

    $.ajax({
        type: 'POST',
        url: '/api/course',
        headers: {
            'Authorization': 'Bearer ' + currentCookie
        },
        data: JSON.stringify({
            couese: $('#course').val()
        }),
        success: function(response){
            if (response.success == 't'){
                location.reload();
            }else{
                alert(response.message);
            }
        }
    })
}