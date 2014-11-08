function submit_credentials() {
    var email = $("#inputEmail").val();
    var pass = $("#inputPassword").val(); 
    
    request = $.ajax({
        type: "POST",
        url: "/login",
        data: email + "\n" + pass
    });

    request.done(function (data) {
        alert(email);
        $.cookie("user_email", email); 
        window.location = "/mainpage";
    });
}
