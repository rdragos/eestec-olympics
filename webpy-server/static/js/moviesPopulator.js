var rottenTomatoesApiKey = "mdrfvydcj2c44cvfvxy2bv6z";
var rottentTomatoesBaseUrl = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies";

function getMovies(page_limit) {
	var method = "in_theaters";
	var format = "json";
	var query = $.ajax({
		type : "GET",
		url : rottentTomatoesBaseUrl + "/" + method + "." + format,
		crossDomain : true,
		dataType : "jsonp",
		data : "apikey=" + rottenTomatoesApiKey + "&" + "page_limit=" + page_limit
  	});
  	return query;
}

function populateUiMovies() {

	var request = getMovies(50);
	request.done(function(data) {
		var totalMovies = data.movies.length;
		for (var index = 0; index < totalMovies; index++) {
			var movieObject = data.movies[index];
			var movieTitle = movieObject.title;
			var rating = movieObject.ratings.audience_score;
			var imageUrl = null;

			if ("posters" in movieObject) {
				if ("detailed" in movieObject.posters) {
					imageUrl = movieObject.posters.detailed;
				}
				if ("profile" in movieObject.posters) {
					imageUrl = movieObject.posters.profile;
				}
				if ("original" in movieObject.posters) {
					imageUrl = movieObject.posters.original;
				}
				if ("thumbnail" in movieObject.posters) {
					imageUrl = movieObject.posters.thumbnail;
				}
			}

			$("#movie-list").append("<div class=\"music-container\"><img src = \"{{imageUrl}}\"><div><h2>{{movieTitle}}</h2><p>Rating {{rating}}</p></div></div>".
				replace("{{movieTitle}}",movieTitle).replace("{{rating}}",rating).replace("{{imageUrl}}",imageUrl));
		}
	});

	request.fail(function (jqXHR, textStatus) {
		alert("Cannot fetch the movies!");
	});
}