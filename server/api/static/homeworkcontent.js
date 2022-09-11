var token = document.cookie.split(";" )[0];
var currentCookie = token.split("=")[1];

function changeHomeworkContent() {
    $.ajax({
        type: 'PUT',
        url: '/api/homework',
        headers: {
            'Authorization': 'Bearer ' + currentCookie,
            'Content-Type' : 'application/json' 
        },
        data: JSON.stringify({
            homeworkName: $('#homeworkName').val(),
            courseName: $('#courseName').text().split(":")[1],
            homeworkInfo: $('homeworkInfo').val(),
            score1: $('score1').val(),
            score2: $('score2').val(),
            score3: $('score3').val()
        }),
        success: function(response){
            alert(response.message);
        }
    })
}

function upload_file() {
    let formData = new FormData();
    formData.append('workType', 1);
    formData.append('className', $('#courseName').text().split(":")[1]);
    formData.append('homeworkName', $('#homeworkName').val());
    formData.append('pgvFile', document.getElementById('pgv1').files[0]);
    formData.append('pgvFile2', document.getElementById('pgv2').files[0]);
    formData.append('pgvFile3', document.getElementById('pgv3').files[0]);
    formData.append('sofFile', document.getElementById('sof1').files[0]);
    formData.append('score', $('#score1').val());
    formData.append('score2', $('#score2').val());
    formData.append('score3', $('#score3').val());

    $.ajax({
        type: 'POST',
        url: '/api/ProgrammingRequest',
        headers: {
            'Authorization': 'Bearer ' + currentCookie
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){}
    })
}

function show_change_homeworkcontent() {
    document.getElementsByClassName('dialog')[0].showModal();
}

function pay_change_homeworkcontent() {
    changeHomeworkContent()
    //document.getElementsByClassName('dialog')[0].close();
    //location.reload();
}

function close_change_homeworkcontent() {
    location.reload();
}