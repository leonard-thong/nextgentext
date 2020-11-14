$("#add_textbook_button").on("click", function (e) {
    e.preventDefault();

    var storageRef = firebase.storage().ref();
    var userID = localStorage.getItem("userid");
    var file = document.querySelector("#file_upload").files[0];
    var voice_name = $("#voice_options :selected").val();

    console.log(voice_name);
    storageRef.child("temp/temp.pdf").put(file);

    var settings = {
        crossDomain: true,
        url:
            "https://159.65.223.140:5001/create-pdf?user_id=" +
            userID +
            "&voice_name=" +
            voice_name,
        method: "GET",
        timeout: 999999,
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
    });
});
