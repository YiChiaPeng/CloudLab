let submit = document.getElementById("btn_submit");
submit.addEventListener("click", submitFormData);

function submitFormData(){
    let emailInput = document.getElementById("floatingInput");
    let email = emailInput.value;
    let passwordInput = document.getElementById("floatingPassword");
    let password = passwordInput.value;
    
   $.$.ajax({
    type: "post",
    url: "url",
    data: {
        "email" : email,
        "password": password
    },
    dataType: "jason",
    success: function (response) {
        if(response.success == "t" ){
            document.cookie = response.jwt_token;
            alert(response.message);
        }
        else{
            alert(response.message);
        }
    }
   });
}