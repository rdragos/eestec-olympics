
var scrobblerApiKey = "d455c0755fdc3ff4c626caeefef6d9fb";
var scrobblerBaseUrl = "http://ws.audioscrobbler.com/2.0";

function getTopTracks() {
	var method = "chart.gettoptracks";
	var format = "json";
	var query = $.ajax({
		type : "GET",
		url : scrobblerBaseUrl,
		crossDomain : true,
		dataType : "jsonp",
		data : "api_key=" + scrobblerApiKey + "&" + "method=" + method + "&" + "format=" + format,
  	});
  	return query;
}

function populateUi() {

	var request = getTopTracks();
	request.done(function(data) {
		for (var index = 0; index < data.tracks.track.length; index++) {

			var track = data.tracks.track[index];
			var artistName = track.artist.name;
			var songName = track.name;
			var imageUrl = "http://djtt-cdn-w3cache.s3.amazonaws.com/wp-content/uploads/2011/08/online-music.bmp";
			if ("image" in track) {
				var imagesCount = track.image.length;
				if (imagesCount > 0) {
					imageUrl = track.image[imagesCount - 1]['#text'];
				}
			}

			$("#music-list").append("<div class=\"music-container\"><img src = \"{{imageUrl}}\"><div><h2>{{artistName}}</h2><p>{{songName}}</p></div></div>".
				replace("{{artistName}}",artistName).replace("{{songName}}",songName).replace("{{imageUrl}}",imageUrl));
		}
	});

	request.fail(function (jqXHR, textStatus) {
		alert("Cannot fetch the latest music!");
	});
}

$(document).ready(function() {
  populateUi();
  populateUiMovies();
})
