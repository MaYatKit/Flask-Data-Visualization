function search_by_date(date) {
    let XHR = new XMLHttpRequest();
    let parameter = {};
    parameter['date'] = date;
    let pay_load = {"parameter": parameter};
    XHR.open('POST', '/api/reinhardt/get_ot_by_date');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');

                let ot_dates = results[0];
                let ot_values = results[1];


                plotGraphs(ot_dates, ot_values)
            } else {
                alert("Internal Error!")
            }
        }
    };

}


function search_by_date_recipe(date, recipe) {
    let XHR = new XMLHttpRequest();
    let result = {};
    result['date'] = date;
    result['recipe'] = recipe;
    let pay_load = {"new_result": result};
    XHR.open('POST', '/api/reinhardt/search_by_date_recipe');
    XHR.setRequestHeader('content-type', 'application/json');
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let ots = XHR.responseText;
                let ot_dates = ots.split(",")[0];
                let ot_values = ots.split(",")[1];
                plotGraphs(ot_dates, ot_values);


                // Load k kord data by date and intervals
                let date_format_for_arm = date.split("-")[2] + "-" + date.split("-")[1] + "-" + date.split("-")[0];
                search_arm_by_date_intervals(date_format_for_arm, 1, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 2, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 3, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 4, ot_dates, ot_values);
                $("#search_button").prop("disabled", false);
                $("#search_button").children().filter("span").remove();
                $("#search_button").text("Search");
            } else {
                alert("Internal Error!")
            }
        }
    };

}


function search_by_date_recipe_number(date, recipe, number) {
    let XHR = new XMLHttpRequest();
    let result = {};
    result['date'] = date;
    result['recipe'] = recipe;
    result['number'] = number;
    let pay_load = {"new_result": result};
    XHR.open('POST', '/api/reinhardt/search_by_date_recipe');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let ots = XHR.responseText;
                let ot_dates = ots.split(",")[0];
                let ot_values = ots.split(",")[1];
                plotGraphs(ot_dates, ot_values);


                // Load k kord data by date and intervals
                let date_format_for_arm = date.split("-")[2] + "-" + date.split("-")[1] + "-" + date.split("-")[0];
                search_arm_by_date_intervals(date_format_for_arm, 1, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 2, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 3, ot_dates, ot_values);
                search_arm_by_date_intervals(date_format_for_arm, 4, ot_dates, ot_values);
                // document.getElementById("loading").style = "visibility: hidden";
                $("#search_button").prop("disabled", false);
                $("#search_button").children().filter("span").remove();
                $("#search_button").text("Search");
            } else {
                alert("Internal Error!")
            }
        }
    };

}