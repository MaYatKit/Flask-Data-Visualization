function search_by_date(date) {
    let XHR = new XMLHttpRequest();
    let result = {};
    result['date'] = date;
    let pay_load = {"new_result": result};
    XHR.open('POST', '/api/search_by_date');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');
                let ots = results[0];
                let mts = results[1];
                let cts = results[2];
                let roks = results[3];
                let rols = results[4];

                let label_points = results[5];
                let labels = results[6];

                let ot_names = ots.split(",")[0];
                let ot_dates = ots.split(",")[1];
                let ot_values = ots.split(",")[2];
                let ot_validities = ots.split(",")[3];
                let ot_mills = ots.split(",")[4];


                let mt_names = mts.split(",")[0];
                let mt_dates = mts.split(",")[1];
                let mt_values = mts.split(",")[2];
                let mt_validities = mts.split(",")[3];
                let mt_mills = mts.split(",")[4];

                let ct_names = cts.split(",")[0];
                let ct_dates = cts.split(",")[1];
                let ct_values = cts.split(",")[2];
                let ct_validities = cts.split(",")[3];
                let ct_mills = cts.split(",")[4];

                let rok_names = roks.split(",")[0];
                let rok_dates = roks.split(",")[1];
                let rok_values = roks.split(",")[2];
                let rok_validities = roks.split(",")[3];
                let rok_mills = roks.split(",")[4];

                let rol_names = rols.split(",")[0];
                let rol_dates = rols.split(",")[1];
                let rol_values = rols.split(",")[2];
                let rol_validities = rols.split(",")[3];
                let rol_mills = rols.split(",")[4];

                plotGraphs(ot_dates, ot_values, mt_dates, mt_values, ct_dates, ct_values, rok_dates, rok_values, rol_dates, rol_values,label_points, labels)

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
    XHR.open('POST', '/api/search_by_date_recipe');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');
                let ots = results[0];
                let mts = results[1];
                let cts = results[2];
                let roks = results[3];
                let rols = results[4];

                let ot_names = ots.split(",")[0];
                let ot_dates = ots.split(",")[1];
                let ot_values = ots.split(",")[2];
                let ot_validities = ots.split(",")[3];
                let ot_mills = ots.split(",")[4];


                let mt_names = mts.split(",")[0];
                let mt_dates = mts.split(",")[1];
                let mt_values = mts.split(",")[2];
                let mt_validities = mts.split(",")[3];
                let mt_mills = mts.split(",")[4];

                let ct_names = cts.split(",")[0];
                let ct_dates = cts.split(",")[1];
                let ct_values = cts.split(",")[2];
                let ct_validities = cts.split(",")[3];
                let ct_mills = cts.split(",")[4];

                let rok_names = roks.split(",")[0];
                let rok_dates = roks.split(",")[1];
                let rok_values = roks.split(",")[2];
                let rok_validities = roks.split(",")[3];
                let rok_mills = roks.split(",")[4];

                let rol_names = rols.split(",")[0];
                let rol_dates = rols.split(",")[1];
                let rol_values = rols.split(",")[2];
                let rol_validities = rols.split(",")[3];
                let rol_mills = rols.split(",")[4];

                plotGraphs(ot_dates, ot_values, mt_dates, mt_values, ct_dates, ct_values, rok_dates, rok_values, rol_dates, rol_values)

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
    XHR.open('POST', '/api/search_by_date_recipe_number');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');
                let ots = results[0];
                let mts = results[1];
                let cts = results[2];
                let roks = results[3];
                let rols = results[4];

                let ot_names = ots.split(",")[0];
                let ot_dates = ots.split(",")[1];
                let ot_values = ots.split(",")[2];
                let ot_validities = ots.split(",")[3];
                let ot_mills = ots.split(",")[4];


                let mt_names = mts.split(",")[0];
                let mt_dates = mts.split(",")[1];
                let mt_values = mts.split(",")[2];
                let mt_validities = mts.split(",")[3];
                let mt_mills = mts.split(",")[4];

                let ct_names = cts.split(",")[0];
                let ct_dates = cts.split(",")[1];
                let ct_values = cts.split(",")[2];
                let ct_validities = cts.split(",")[3];
                let ct_mills = cts.split(",")[4];

                let rok_names = roks.split(",")[0];
                let rok_dates = roks.split(",")[1];
                let rok_values = roks.split(",")[2];
                let rok_validities = roks.split(",")[3];
                let rok_mills = roks.split(",")[4];

                let rol_names = rols.split(",")[0];
                let rol_dates = rols.split(",")[1];
                let rol_values = rols.split(",")[2];
                let rol_validities = rols.split(",")[3];
                let rol_mills = rols.split(",")[4];

                plotGraphs(ot_dates, ot_values, mt_dates, mt_values, ct_dates, ct_values, rok_dates, rok_values, rol_dates, rol_values)

            } else {
                alert("Internal Error!")
            }
        }
    };

}