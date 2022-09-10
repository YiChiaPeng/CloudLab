//燒錄
var token = document.cookie.split(";" )[0];
var currentCookie = token.split("=")[1];

function do_sofupload() {
    $("#sofupload").empty();
    $("#sofupload").append(SofUploadForm);
}

document.getElementById("soffile").addEventListener("change", function() {
    do_sofupload();
    console.log(this.value);
})

function do_pgvupload() {
    $("#pgvupload").empty();
    $("#pgvupload").append(PgvUploadForm);
}

document.getElementById("pgvfile").addEventListener("change", function() {
    console.log(this.value);
    do_pgvupload();
})

function do_pay() {
    let formData = new FormData();
    formData.append('sofFile', document.getElementById('soffile').files[0]);
    formData.append('pgvFile', document.getElementById('pgvfile').files[0]);
    formData.append('workType', 0);

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