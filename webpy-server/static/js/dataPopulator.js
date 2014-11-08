function getUserData() {

	var query = $.ajax({
		type : "GET",
		url : "/users",
		data : "email=" + $.cookie("user_email")
  	});
  	return query;
}

function populateUserDataUi() {

	var request = getUserData();
	request.done(function(data) {
		var jsonObject = JSON.parse(data);
		console.log(jsonObject);
		$(".nav-bar > .user-profile > p").text(jsonObject.firstName + " " + jsonObject.lastName);
	});

	request.fail(function() {
		alert("mamaie");
	});

}