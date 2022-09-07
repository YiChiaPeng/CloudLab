function do_addHomework() {
    var token = document.cookie.split(";" )[0];
    var currentCookie = token.split("=")[1];
    $.ajax({
        type: 'POST',
        url: '/api/homework',
        headers: {
            'Authorization': 'Bearer ' + currentCookie,
            'Content-Type' : 'application/json' 
        },
        data: JSON.stringify({
            homeworkInfo: $('#homeworkInfo').val(),
            homeworkName: $('#homeworkName').val(),
            courseName: $('#courseName').text().split(":" )[1]

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

function showDialog() {
    document.getElementsByClassName('dialog')[0].showModal();
}

function closeDialog() {
    do_addHomework();
    document.getElementsByClassName('dialog')[0].close();
    location.reload();
}

function do_delete() {
    
}
