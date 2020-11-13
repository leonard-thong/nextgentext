$("#select_audio_button").on("click", function (e) {
    e.preventDefault();
    $("#audio_container").empty();
        audioElement = document.createElement("audio");

        audioElement.setAttribute(
            "src",
            "http://www.soundjay.com/misc/sounds/bell-ringing-01.mp3"
        );

        audioElement.setAttribute("controls", "");

        $("#audio_container").append(audioElement);
});
