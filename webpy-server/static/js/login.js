function submit_credentials() {
    var email = $("#inputEmail").val();
    var pass = $("#inputPassword").val(); 
    
    $.ajax({
        type: "POST",
        url: "/login",
        data: email + "\n" + pass,
        success: null,
        dataType: null
    });
}
