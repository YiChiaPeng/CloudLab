function do_sofupload() {
    $("#sofupload").empty();
    $("#sofupload").append(SofUploadForm);
}

document.getElementById("soffile").addEventListener("change", function() {
    console.log("change");
    do_sofupload();
})

function do_pgvupload() {
    $("#pgvupload").empty();
    $("#pgvupload").append(PgvUploadForm);
}

document.getElementById("pgvfile").addEventListener("change", function() {
    console.log("change");
    do_pgvupload();
})