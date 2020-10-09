function plotGraphs(ot_dates, ot_temps) {

    if (!!(document.getElementById('rh_OT_line_chart'))) {
        document.getElementById('rh_OT_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "rh_OT_line_chart");
        document.getElementById('rh_OT_line_chart_parent').appendChild(canvas);
    }


    const OT_line_chart = document.getElementById('rh_OT_line_chart').getContext('2d');


    // {#-------Oven_Temperature_PV--------#}
    let ot_dates_list = ot_dates.split("_");
    let ot_temps_list = ot_temps.split("_");

    let timeList = [];
    for (const i of ot_dates_list) {
        timeList.push(i.split(" ")[1]);
    }
    let day = ot_dates_list[0].split(" ")[0];


    const timeFormat = 'h:mm:ss';


    const oven_temperature_chart = new Chart(OT_line_chart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: timeList,
            datasets: [{
                label: day,
                borderColor: window.chartColors.red,
                backgroundColor: 'transparent',
                data: ot_temps_list,
                fill: false,
                pointRadius: 0,
                borderWidth: 2,
                spanGaps: false
            }]
        },

        //Configuration options go here
        options: {
            responsiveAnimationDuration: 0, // animation duration after a resize
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'bottom',
                labels: {
                    padding: 10
                    // fontColor: window.chartColors.red,
                }
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear', //data are spread at the same distance from each other
                    ticks: {
                        beginAtZero: false,
                        source: 'time',
                        autoSkip: true,
                        maxRotation: 0,
                        autoSkipPadding: 10
                    },
                    time: {
                        format: timeFormat,
                        unit: 'minute'
                    },
                    gridLines: {
                        display: true
                    }
                }],
                yAxes: [{
                    display: 'auto',
                    ticks: {
                        source: 'data',
                        autoSkip: false,
                        maxRotation: 0,
                        autoSkipPadding: 10
                    },

                    gridLines: {
                        display: true
                    }
                }]
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            layout: {
                padding: {left: 15, right: 15, top: 15, bottom: 15}
            },
            tooltips: {
                enabled: true,
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
            },
            plugins: {
                zoom: {
                    // Container for pan options
                    pan: {
                        // Boolean to enable panning
                        enabled: true,

                        // Panning directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow panning in the y direction
                        mode: 'x'
                    },

                    // Container for zoom options
                    zoom: {
                        // Boolean to enable zooming
                        enabled: true,

                        // Zooming directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow zooming in the y direction
                        mode: 'x',
                    }
                }
            }
        }
    });

    // document.getElementById("loading").style = "visibility: hidden";
    $("#search_button").prop("disabled", false);
    $("#search_button").children().filter("span").remove();
    $("#search_button").text("Search");
}

function plotReinhardtSetting(arm_recipe_data, recipe_settings) {
    let table = document.getElementById("reinhardt_setting_table");

    for (let i = 1; i <= arm_recipe_data.length; i++) {
        let row = table.insertRow(i);
        let arm = row.insertCell(0);
        let recipe_no = row.insertCell(1);
        let set_temp_1 = row.insertCell(2);
        let mould_speed = row.insertCell(3);
        let heat1 = row.insertCell(4);

        arm.innerHTML = i.toString();
        recipe_no.innerHTML = arm_recipe_data[i - 1];
        let recipe_setting = [];
        for (let each of recipe_settings) {
            if (each[0] === arm_recipe_data[i - 1]) {
                recipe_setting = each;
                break
            }
        }
        set_temp_1.innerHTML = recipe_setting[1];
        mould_speed.innerHTML = recipe_setting[2];
        heat1.innerHTML = recipe_setting[3];
    }

}

function ot_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    let lastSearchIndex = 0;
    for (data of dataList) {
        const value = parseInt(data.split(".")[0]);
        if (value > max || value <= min) {
            const ind = dataList.indexOf(data, lastSearchIndex);
            lastSearchIndex = ind;
            newDataList.push(null);
            newTimeList.push(timeList[ind]);
        } else {
            const ind = dataList.indexOf(data, lastSearchIndex);
            lastSearchIndex = ind;
            newDataList.push(value);
            newTimeList.push(timeList[ind]);
        }
    }
}


function MT_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    let lastSearchIndex = 0;
    for (data of dataList) {
        const value = parseInt(data.split(".")[0]);
        if (value > max || value < min) {
            // if (value < min) {
            const ind = dataList.indexOf(data, lastSearchIndex);
            lastSearchIndex = ind;
            newDataList.push(null);
            newTimeList.push(timeList[ind]);
            // }
        } else {
            const ind = dataList.indexOf(data, lastSearchIndex);
            lastSearchIndex = ind;
            newDataList.push(value);
            newTimeList.push(timeList[ind]);
        }
    }
}


function CT_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    let lastSearchIndex = 0;
    for (data of dataList) {
        const value = parseInt(data.split(".")[0]);
        if (value > max || value <= min) {
            if (value === 0) {
                const ind = dataList.indexOf(data, lastSearchIndex);
                lastSearchIndex = ind;
                newDataList.push(null);
                newTimeList.push(timeList[ind]);
            }
        } else {
            const ind = dataList.indexOf(data, lastSearchIndex);
            lastSearchIndex = ind;
            newDataList.push(value);
            newTimeList.push(timeList[ind]);
        }
    }
}


function transformDateTimestamp(time) {
    let hour = time.split(":")[0];
    let min = time.split(":")[1];
    let sec = time.split(":")[2];
    return parseInt(hour) * 60 * 60 + parseInt(min) * 60 + parseInt(sec);
}

function CombineMTandCTandOT(CT_DataList, CT_TimeList, MT_DataList, MT_TimeList, OT_DataList, OT_TimeList, combineDataList_CT, combineDataList_MT, combineDataList_OT, combineTimeList, label_points) {
    //Combine cooling temperature data and mould temperature data

    for (let ind in MT_TimeList) {
        combineTimeList.push(MT_TimeList[ind]);
        combineDataList_MT.push(MT_DataList[ind]);
        combineDataList_CT.push(null);
        combineDataList_OT.push(null);
    }

    for (let ind in CT_TimeList) {
        let ct_time = CT_TimeList[ind];
        combineTimeList.push(ct_time);
        combineDataList_CT.push(CT_DataList[ind]);
        combineDataList_MT.push(null);
        combineDataList_OT.push(null);
    }


    for (let ind in OT_TimeList) {
        combineTimeList.push(OT_TimeList[ind]);
        combineDataList_OT.push(OT_DataList[ind]);
        combineDataList_CT.push(null);
        combineDataList_MT.push(null);
    }
}


let showLabel = true;
let drawingLabel = false;
let hasDefineCallback = false;
let entering = false;
let leaving = false;

var drawTooltip = function (dotColor, textColor, xAxis, chartbody, label) {

    return function () {

        // var label__year = '年龄：' + year + '岁', label__sick = '致病率：' + (100 * sickData[+year]).toFixed(1, 10) + '%';

        var model = chartbody.chart.controller.getDatasetMeta(1).data[xAxis]._model;

        var ctx = chartbody.chart.ctx;


        ctx.lineWidth = 2;

        //ctx.strokeStyle = 'rgba(255,135,67,.4)';

        // ctx.fillStyle = '#fff';
        ctx.fillStyle = dotColor;

        ctx.beginPath();

        ctx.arc(model.x, model.y, 4, 0, 2 * Math.PI);

        ctx.closePath();

        //ctx.stroke();

        ctx.fill();

        //ctx.lineWidth = 3;

        //ctx.strokeStyle = window.chartColors.orange + '';

        // ctx.beginPath();
        //
        // ctx.arc(model.x, model.y, 3.5, 0, 2 * Math.PI);
        //
        // ctx.closePath();

        //ctx.stroke();

        // ctx.strokeStyle = '#fff6f2';

        // ctx.fillStyle = backgroundColor;
        //
        // var rectX = model.x, rectY = model.y - 20;
        //
        // var rectWidth = 60, rectHeight = 30;
        //
        // var cornerRadius = 10, margin = 5, dist = 30;
        //
        // ctx.lineJoin = 'round';
        //
        // ctx.lineWidth = 2;

        // ctx.strokeRect(rectX - rectWidth / 2, rectY - rectHeight / 1.5, rectWidth, rectHeight);

        // ctx.fillRect(rectX - rectWidth / 2, rectY - rectHeight / 1.5, rectWidth, rectHeight);

        ctx.font = '700 14px PingFangSC-Regular';

        ctx.fillStyle = textColor;

        let textWidth = ctx.measureText(label).width;
        let textheight = parseInt(ctx.font.match(/\d+/), 10);

        ctx.fillText(label, model.x - textWidth / 2, model.y - textheight * 1.5);

        //ctx.fillText("test2", rectX - 2 * dist, rectY - (dist / 2) + 2.5 * margin);


        // chartbody.update();
    }
};


