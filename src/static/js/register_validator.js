$().ready(function() {
    $("#newUser").validate({
        rules: {
            confirmpword: {
                equalTo: "#pword"
            }
        }
    });
});