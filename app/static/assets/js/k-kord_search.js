function search_arm_by_date(date, arm) {
    let XHR = new XMLHttpRequest();
    let parameter = {};
    parameter['date'] = date;
    parameter['arm'] = arm;
    let pay_load = {"parameter": parameter};
    XHR.open('POST', '/api/k-kord/get_arm_by_date');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');

                let times = results[0];
                let arm_IATs = results[1];
                let arm_MWTs = results[2];
                let arm_AMBs = results[3];
                plotArmGraphs(times, arm_IATs, arm_MWTs, arm_AMBs, arm)
            } else {
                alert("Internal Error!")
            }
        }
    };

}


function search_arm_by_date_intervals(date, arm, intervals, ot_data) { // ot_data used to indicate the gap of two intervals
    let XHR = new XMLHttpRequest();
    let parameter = {};
    parameter['date'] = date;
    parameter['arm'] = arm;
    parameter['intervals'] = intervals;
    parameter['ot_data'] = ot_data;
    let pay_load = {"parameter": parameter};
    XHR.open('POST', '/api/k-kord/get_arm_by_date_intervals');
    XHR.setRequestHeader('content-type', 'application/json');  //先open再设置请求头
    XHR.send(JSON.stringify(pay_load));

    XHR.onreadystatechange = function () {
        //if Response finish and success
        if (XHR.readyState === 4 && XHR.status === 200) {
            if (XHR.responseText) {
                let results = XHR.responseText.split(';');

                let times = results[0];
                let arm_IATs = results[1];
                let arm_MWTs = results[2];
                let arm_AMBs = results[3];
                plotArmGraphs(times, arm_IATs, arm_MWTs, arm_AMBs, arm)
            } else {
                alert("Internal Error!")
            }
        }
    };

}