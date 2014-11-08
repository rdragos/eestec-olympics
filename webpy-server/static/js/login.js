function submit_credentials() {
    var email = $("#inputEmail").val();
    var pass = $("#inputPassword").val(); 
    
    request = $.ajax({
        type: "GET",
        url: "/login",
        data: "email=" + email + "&" + "password=" + pass
    });

    request.done(function (data) {

        if (data == "OK") {
            $.cookie("user_email", email); 
            window.location = "/mainpage";
        }
        else {
            alert("Username or password are not valid!");
        }        
    });

    request.fail(function (data) {
        alert("Server cannot be reached!");
    })
}
