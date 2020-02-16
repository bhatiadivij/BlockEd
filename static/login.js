$(document).ready(function() {

    $("#form1").on("submit",function(e) {
        e.preventDefault(); // cancel submission

        localStorage.setItem("userID", $("#username").val());
        // alert(window.location + "/university");
        // window.location.replace(window.location + "/university");
    });

})

