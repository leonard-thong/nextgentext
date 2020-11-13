$(document).ready(function () {
    l = location.pathname;
    path = l.split("/").slice(-1)[0];

    if (path === "dashboard.html") {
        // loading dashboard.html
        var userID = localStorage.getItem("userid");

        $("#item_list").empty();
        var bookNames = [];

        $.get(
            "http://159.65.223.140:5001/" + userID + "/get-all-books",
            function (res) {
                bookNames = res;
                console.log(res);
            }
        ).done(function () {
            bookNames.forEach((book) => {
                i = document.createElement("img");
                i.setAttribute("src", "assets/img/tech/image2.jpg");
                i.setAttribute("class", "img-fluid d-block mx-auto");

                a = document.createElement("a");
                a.append(i);

                d = document.createElement("div");
                d.setAttribute("class", "image");
                d.append(i);

                a2 = document.createElement("a");
                a2.setAttribute(
                    "href",
                    "book.html?name=" + encodeURIComponent(book)
                );
                a2.setAttribute("id", "book_redirect");
                $(a2).text(book);

                d2 = document.createElement("div");
                d2.setAttribute("class", "product-name");
                d2.append(d, a2);

                d3 = document.createElement("div");
                d3.setAttribute("class", "clean-product-item");
                d3.append(d2);

                d4 = document.createElement("div");
                d4.setAttribute("class", "col-12 col-md-6 col-lg-4");
                d4.append(d3);

                $("#item_list").append(d4);
                console.log("dashboard path");
            });
        });
    }

    if (path === "book.html") {
        var userID = localStorage.getItem("userid");

        // loading book.html
        url = decodeURIComponent(location);
        bookname = url.split("=").slice(-1)[0];

        $("#book_name").text(bookname);
        options = [];

        $.get(
            "http://159.65.223.140:5001/" +
                bookname +
                "/get-all-audiobook-chapters",
            function (res) {
                options = res;
                console.log(res);
            }
        ).done(function () {
            $("#chapter_options").empty();
            options.sort(function (a, b) {
                return a.localeCompare(b, undefined, {
                    numeric: true,
                    sensitivity: "base",
                });
            });
            options.forEach((option) => {
                o = document.createElement("option");
                $(o).text(option).appendTo("#chapter_options");
            });
            console.log("book path");
        });
    }
});
