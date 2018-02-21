var serverPath = 'http://127.0.0.1:8000';
var tokenPath = '/get-token/';
var contactTypePath = '/contact-type/';
var username = "admin";
var password = "darvin123";
var authToken = "";

$(document).ready(function () {
    $.ajax({
        method: "POST",
        url: serverPath + tokenPath,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify({
            "username": username,
            "password": password
        }),
        success: function (data) {
            authToken = data["token"]
        },
        error: function (error) {
            console.log(error)
        }
    })
});

$('.organizations').click(function () {
    $.ajax({
        method: "GET",
        dataType: "json",
        url: serverPath + contactTypePath,
        headers: {
            "Authorization": "Token " + authToken
        },
        success: function (response) {
            $(function () {
                $.each(response, function (i, item) {
                    var $tr = $('<tr>').append(
                        $('<td>').text(item.name),
                        $('<td>').text(item.caption),
                        $('<td>').text(item.template),
                        $('<td>').text(item.infoText)
                    );
                    $tr.appendTo('#recordsTable');

                });
            });
        },
        error: function (error) {
            console.log(error)
        }
    })
});