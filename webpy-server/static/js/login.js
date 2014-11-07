function submit_credentials() {
    var email = $("#inputEmail").val();
    var pass = $("#inputPassword").val(); 
    
    $.ajax({
        type: "POST",
        url: "/login",
        data: email + "\n" + pass,
        success: function(data) {
            alert("Success");
            window.location = "/";
        },
        error: function(data) {
            alert("Error");
            window.localtion = "/login";
        }
    });
}
