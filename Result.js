function getResult() {
    document.getElementById("output").innerHTML = "Your Application is Processing......(LOADING)"
    var url = "http://localhost:8000";   // The URL and the port number must match the server-side
    var endpoint = "/apply";

    var http = new XMLHttpRequest();

    var days_elapsed = document.getElementById("days_elapsed").value;
    var usd_goal_real = document.getElementById("usd_goal_real").value;
    var country = document.getElementById("country").value;
    var main_category = document.getElementById("main_category").value;
    var category = document.getElementById("category").value;
    var month_launched = document.getElementById("month_launched").value;

    var apply = {"days_elapsed": days_elapsed, "usd_goal_real": usd_goal_real, "country": country, "main_category": main_category, "category": category, "month_launched": month_launched};

    // JSON string to post
    var application = JSON.stringify(apply);

    // POST request
    http.open("POST", url+endpoint, true);

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            replyString = http.responseText;

            replyObj = JSON.parse(replyString);
            document.getElementById("result").innerHTML = "Your Funding Project is: "+replyObj.result;
        }
    };

    // Send request
    http.send(application);



}