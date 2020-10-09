function plotGraphs(ot_dates, ot_values, mt_dates, mt_values, ct_dates, ct_values, rock_a_dates, rock_a_values, roll_a_dates, roll_a_values, label_points_str, labels_str) {

    if (!!(document.getElementById('OT_line_chart'))) {
        document.getElementById('OT_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "OT_line_chart");
        document.getElementById('OT_line_chart_parent').appendChild(canvas);
    }
    if (!!(document.getElementById('MT_line_chart'))) {
        document.getElementById('MT_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "MT_line_chart");
        document.getElementById('MT_line_chart_parent').appendChild(canvas);
    }
    if (!!(document.getElementById('CT_line_chart'))) {
        document.getElementById('CT_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "CT_line_chart");
        document.getElementById('CT_line_chart_parent').appendChild(canvas);
    }
    if (!!(document.getElementById('CT_MT_mix_line_chart'))) {
        document.getElementById('CT_MT_mix_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "CT_MT_mix_line_chart");
        document.getElementById('CT_MT_mix_line_chart_parent').appendChild(canvas);
    }
    if (!!(document.getElementById('RockA_line_chart'))) {
        document.getElementById('RockA_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "RockA_line_chart");
        document.getElementById('RockA_line_chart_parent').appendChild(canvas);
    }
    if (!!(document.getElementById('RollA_line_chart'))) {
        document.getElementById('RollA_line_chart').remove();
        let canvas = document.createElement('canvas');
        canvas.setAttribute("id", "RollA_line_chart");
        document.getElementById('RollA_line_chart_parent').appendChild(canvas);
    }

//Oven_Temperature_PV
//     const OT_line_chart = document.getElementById('OT_line_chart').getContext('2d');
// //Mould_Temperature_PV
//     const MT_line_chart = document.getElementById('MT_line_chart').getContext('2d');
// //Cooling_Temperature_PV
//     const CT_line_chart = document.getElementById('CT_line_chart').getContext('2d');
//Mould_Cooling_mix_PV
    const CT_MT_mix_line_chart = document.getElementById('CT_MT_mix_line_chart').getContext('2d');
//Rock_Angle_PV
    const RockA_line_chart = document.getElementById('RockA_line_chart').getContext('2d');
//Roll_Angle_PV
    const RollA_line_chart = document.getElementById('RollA_line_chart').getContext('2d');


    // {#-------Oven_Temperature_PV--------#}
    let tempList = ot_dates.split("_");
    let valueList = ot_values.split("_");

    let timeList = [];
    for (const i of tempList) {
        timeList.push(i.split(" ")[1]);
    }
    let day = tempList[0].split(" ")[0];


    let OT_newDataList = [], OT_newTimeList = [];



    const timeFormat = 'h:mm:ss';
    ot_decimation(valueList, timeList, OT_newDataList, OT_newTimeList, 0, 400);

    // {#---------Mould_Temperature_PV--------#}

    valueList.splice(0, valueList.length);
    tempList.splice(0, tempList.length);
    timeList.splice(0, timeList.length);
    day.length = 0;

    tempList = mt_dates.split("_");
    valueList = mt_values.split("_");
    for (const i of tempList) {
        timeList.push(i.split(" ")[1]);
    }
    day = tempList[0].split(" ")[0];

    let MT_newDataList = [], MT_newTimeList = [];
    MT_decimation(valueList, timeList, MT_newDataList, MT_newTimeList, 20, 200);



    // {#-------Cooling_Temperature_PV--------#}

    valueList.splice(0, valueList.length);
    tempList.splice(0, tempList.length);
    timeList.splice(0, timeList.length);
    day.length = 0;

    tempList = ct_dates.split("_");
    valueList = ct_values.split("_");
    for (const i of tempList) {
        timeList.push(i.split(" ")[1]);
    }
    day = tempList[0].split(" ")[0];
    let CT_newDataList = [], CT_newTimeList = [];

    CT_decimation(valueList, timeList, CT_newDataList, CT_newTimeList, 0, 200);


    // {#------------CT_MT_mix_chart------------#}

    let labels = [];
    let label_points;
    if (labels_str !== undefined) {
        let str;
        for (str of labels_str.split("_")) {
            if (str === '1.0') {
                labels.push('1200 x 6 Pipe v1')
            } else if (str === '2.0') {
                labels.push('1000 pipe v6')
            } else if (str === '3.0') {
                labels.push('645-800 pipe v1')
            } else if (str === '4.0') {
                labels.push('1200 x 5 Pipe v1')
            }
        }
        label_points = label_points_str.split("_");
    }

    let combineDataList_CT = [], combineTimeList = [], combineDataList_MT = [], combineDataList_OT = [];

    CombineMTandCTandOT(CT_newDataList, CT_newTimeList, MT_newDataList, MT_newTimeList, OT_newDataList, OT_newTimeList, combineDataList_CT, combineDataList_MT, combineDataList_OT, combineTimeList);


    $('#CT_MT_mix_line_chart').hover(function (e) {
        // $('.chart--root').css('pointer-events', 'none')
        console.log(e.type);
        if (e.type === 'mouseenter' && entering === false) {
            entering = true;
            console.log("showLabel = false");
            showLabel = false;
            CT_MT_mix_chart.update();
        } else if (e.type === 'mouseleave' && leaving === false) {
            leaving = true;
            console.log("showLabel = true");
            showLabel = true;
            CT_MT_mix_chart.update();
        }
    });

    let zooming = false;
    let panning = false;
    const CT_MT_mix_chart = new Chart(CT_MT_mix_line_chart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: combineTimeList,
            datasets: [{
                label: 'Cooling Temperature',
                borderColor: window.chartColors.orange,
                backgroundColor: 'transparent',
                data: combineDataList_CT,
                fill: false,
                pointRadius: 0,
                borderWidth: 2,
                spanGaps: false
            },
                {
                    label: 'Mould Temperature',
                    borderColor: window.chartColors.purple,
                    backgroundColor: 'transparent',
                    data: combineDataList_MT,
                    fill: false,
                    pointRadius: 0,
                    borderWidth: 2,
                    spanGaps: false
                },
                {

                    label: 'Oven Temperature',
                    borderColor: window.chartColors.blue,
                    backgroundColor: 'transparent',
                    data: combineDataList_OT,
                    fill: false,
                    pointRadius: 0,
                    borderWidth: 2,
                    spanGaps: false
                }]
        },

        //Configuration options go here
        options: {
            animation: {
                onComplete: function () {
                    if (labels_str !== undefined && !zooming && !panning) {
                        entering = false;
                        leaving = false;
                        if (showLabel && !drawingLabel) {
                            console.log("showLabel");
                            drawingLabel = true;
                            for (let i = 0; i < labels.length; i++) {
                                setTimeout(drawTooltip('#F25961', '#F25961', label_points[i], this, labels[i]), 50);
                            }
                            drawingLabel = false;
                        }
                    }
                }
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20
                    // fontColor: window.chartColors.orange,
                }
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear', //series or linear: data are spread at the same distance from each other
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
                    // type: 'string',
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
                enabled: (!zooming && !panning),
                bodySpacing: 4,
                intersect: false,
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10,
                callbacks: {
                    label: function (tooltipItems, data) {
                        let multiStringText = [tooltipItems.yLabel];
                        if (combineDataList_CT[tooltipItems.index] !== tooltipItems.yLabel) {
                            setTimeout(multiStringText.push(findNearestOTorMT(tooltipItems, combineTimeList, combineDataList_MT, combineDataList_OT, MT_newDataList, MT_newTimeList, OT_newDataList, OT_newTimeList)), 50);
                        }
                        return multiStringText;
                    }
                }
            },
            plugins: {
                zoom: {
                    // Container for pan options
                    pan: {
                        // Boolean to enable panning
                        enabled: true,

                        // Panning directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow panning in the y direction
                        mode: 'x',
                        // Function called while the user is panning
                        onPan: function ({chart}) {
                            // console.log(`I'm panning!!!`);
                            panning = true;
                        },
                        // Function called once panning is completed
                        onPanComplete: function ({chart}) {
                            // console.log(`I was panned!!!`);
                            panning = false;
                        }
                    },

                    // Container for zoom options
                    zoom: {
                        // Boolean to enable zooming
                        enabled: true,

                        // Zooming directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow zooming in the y direction
                        mode: 'x',
                        onZoom: function ({chart}) {
                            // console.log(`I'm zooming!!!`);
                            zooming = true;

                        },
                        // Function called once zooming is completed
                        onZoomComplete: function ({chart}) {
                            // console.log(`I was zoomed!!!`);
                            zooming = false;
                        }
                    }
                }
            }
        }
    });

    // {#------------Rock_Angle_PV------------#}

    valueList.splice(0, valueList.length);
    tempList.splice(0, tempList.length);
    timeList.splice(0, timeList.length);
    day.length = 0;

    tempList = rock_a_dates.split("_");
    valueList = rock_a_values.split("_");
    for (const i of tempList) {
        timeList.push(i.split(" ")[1]);
    }
    day = tempList[0].split(" ")[0];

    //keep a same range as the CT_MT_mix_chart
    let leastTime = 0;
    let biggestTime = 0;

    if (transformDateTimestamp(CT_newTimeList[0]) <= transformDateTimestamp(MT_newTimeList[0]) && transformDateTimestamp(CT_newTimeList[0]) <= transformDateTimestamp(OT_newTimeList[0])) {
        leastTime = CT_newTimeList[0];
    } else if (transformDateTimestamp(OT_newTimeList[0]) <= transformDateTimestamp(MT_newTimeList[0]) && transformDateTimestamp(OT_newTimeList[0]) <= transformDateTimestamp(CT_newTimeList[0])) {
        leastTime = OT_newTimeList[0];
    } else if (transformDateTimestamp(MT_newTimeList[0]) <= transformDateTimestamp(OT_newTimeList[0]) && transformDateTimestamp(MT_newTimeList[0]) <= transformDateTimestamp(CT_newTimeList[0])) {
        leastTime = MT_newTimeList[0];
    }

    if (transformDateTimestamp(CT_newTimeList[CT_newTimeList.length - 1]) >= transformDateTimestamp(MT_newTimeList[MT_newTimeList.length - 1]) && transformDateTimestamp(CT_newTimeList[CT_newTimeList.length - 1]) >= transformDateTimestamp(OT_newTimeList[OT_newTimeList.length - 1])) {
        biggestTime = CT_newTimeList[CT_newTimeList.length - 1];
    } else if (transformDateTimestamp(OT_newTimeList[OT_newTimeList.length - 1]) >= transformDateTimestamp(MT_newTimeList[MT_newTimeList.length - 1]) && transformDateTimestamp(OT_newTimeList[OT_newTimeList.length - 1]) >= transformDateTimestamp(CT_newTimeList[CT_newTimeList.length - 1])) {
        biggestTime = OT_newTimeList[OT_newTimeList.length - 1];
    } else if (transformDateTimestamp(MT_newTimeList[MT_newTimeList.length - 1]) >= transformDateTimestamp(OT_newTimeList[OT_newTimeList.length - 1]) && transformDateTimestamp(MT_newTimeList[MT_newTimeList.length - 1]) >= transformDateTimestamp(CT_newTimeList[CT_newTimeList.length - 1])) {
        biggestTime = MT_newTimeList[MT_newTimeList.length - 1];
    }

    let RA_newDataList = valueList.slice(), RA_newTimeList = timeList.slice();

    RA_newTimeList.push(leastTime);
    RA_newDataList.push(null);
    RA_newTimeList.push(biggestTime);
    RA_newDataList.push(null);

    const RockA_chart = new Chart(RockA_line_chart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: RA_newTimeList,
            datasets: [{
                label: day,
                borderColor: window.chartColors.purple,
                backgroundColor: 'transparent',
                data: RA_newDataList,
                fill: false,
                pointRadius: 0,
                borderWidth: 2,
                spanGaps: false,
                showLine: true
            }]
        },

        //Configuration options go here
        options: {
            // animation: {
            //     onComplete: function () {
            //         if (showLabel) {
            //             setTimeout(drawTooltip(500, this, "test"), 50);
            //         }
            //         $('#RockA_line_chart').hover(function (e) {
            //             // $('.chart--root').css('pointer-events', 'none')
            //             if (e.type === 'mouseenter') {
            //                 showLabel = false;
            //                 RockA_chart.update();
            //             } else if (e.type === 'mouseleave') {
            //                 showLabel = true;
            //                 RockA_chart.update();
            //             }
            //         });
            //     }
            // },
            responsiveAnimationDuration: 0, // animation duration after a resize
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'bottom',
                labels: {
                    padding: 10

                }
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear', //data are spread at the same distance from each other
                    ticks: {
                        // source: 'data',
                        // autoSkip: true,
                        // maxRotation: 0,
                        // autoSkipPadding: 50
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
                    // type: 'data',
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


    // {#------------Roll_Angle_PV------------#}

    tempList.length = 0;
    valueList.length = 0;
    timeList.length = 0;
    day.length = 0;

    tempList = roll_a_dates.split("_");
    valueList = roll_a_values.split("_");
    for (const i of tempList) {
        timeList.push(i.split(" ")[1]);
    }
    day = tempList[0].split(" ")[0];


    let RollA_newDataList = valueList.slice(), RollA_newTimeList = timeList.slice();

    RollA_newTimeList.push(leastTime);
    RollA_newDataList.push(null);
    RollA_newTimeList.push(biggestTime);
    RollA_newDataList.push(null);


    const RollA_chart = new Chart(RollA_line_chart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: RollA_newTimeList,
            datasets: [{
                label: day,
                borderColor: window.chartColors.red,
                backgroundColor: 'transparent',
                data: RollA_newDataList,
                fill: false,
                pointRadius: 0,
                borderWidth: 2,
                showLine: true
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
                        // source: 'data',
                        // autoSkip: true,
                        // maxRotation: 0,
                        // autoSkipPadding: 50
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
                    // time: 'time',
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


function ot_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    for (let index = 0; index < dataList.length; index++) {
        const value = parseInt(dataList[index].split(".")[0]);
        if (value > max || value <= min) {
            newDataList.push(null);
            newTimeList.push(timeList[index]);
        } else {
            newDataList.push(value);
            newTimeList.push(timeList[index]);
        }
    }
}



function MT_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    for (let index = 0; index < dataList.length; index++) {
        const value = parseInt(dataList[index].split(".")[0]);
        if (value > max || value < min) {
            newDataList.push(null);
            newTimeList.push(timeList[index]);
        } else {
            newDataList.push(value);
            newTimeList.push(timeList[index]);
        }
    }
}


function CT_decimation(dataList, timeList, newDataList, newTimeList, min, max) {
    for (let index = 0; index < dataList.length; index++) {
        const value = parseInt(dataList[index].split(".")[0]);
        if (value > max || value <= min) {
            if (value === 0) {
                newDataList.push(null);
                newTimeList.push(timeList[index]);
            }
        } else {
            newDataList.push(value);
            newTimeList.push(timeList[index]);
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

// let combineDataList_CT = [], combineTimeList = [], combineDataList_MT = [];
//
// CombineMTandCT(CT_newDataList, CT_newTimeList, MT_newDataList, MT_newTimeList, combineDataList_CT, combineDataList_MT, combineTimeList);
//
// const CT_MT_mix_chart = new Chart(CT_MT_mix_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: combineTimeList,
//         datasets: [{
//             label: 'Cooling Temperature',
//             borderColor: window.chartColors.orange,
//             backgroundColor: 'transparent',
//             data: combineDataList_CT,
//             fill: false,
//             pointRadius: 0,
//             borderWidth: 2,
//             spanGaps: false
//         },
//             {
//                 label: 'Mould Temperature',
//                 borderColor: window.chartColors.purple,
//                 backgroundColor: 'transparent',
//                 data: combineDataList_MT,
//                 fill: false,
//                 pointRadius: 0,
//                 borderWidth: 2,
//                 spanGaps: false
//             }]
//     },
//
//     //Configuration options go here
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         legend: {
//             position: 'bottom',
//             labels: {
//                 padding: 20
//                 // fontColor: window.chartColors.orange,
//             }
//         },
//         scales: {
//             xAxes: [{
//                 type: 'time',
//                 distribution: 'linear', //series or linear: data are spread at the same distance from each other
//                 ticks: {
//                     beginAtZero: false,
//                     source: 'time',
//                     autoSkip: true,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//                 time: {
//                     format: timeFormat,
//                     unit: 'minute'
//                 },
//                 gridLines: {
//                     display: true
//                 }
//             }],
//             yAxes: [{
//                 // type: 'string',
//                 display: 'auto',
//                 ticks: {
//                     source: 'data',
//                     autoSkip: false,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//
//                 gridLines: {
//                     display: true
//                 }
//             }]
//         },
//         hover: {
//             animationDuration: 0 // duration of animations when hovering an item
//         },
//         layout: {
//             padding: {left: 15, right: 15, top: 15, bottom: 15}
//         },
//         tooltip: {
//             bodySpacing: 4,
//             mode: "nearest",
//             intersect: 0,
//             position: "nearest",
//             xPadding: 10,
//             yPadding: 10,
//             caretPadding: 10
//         }
//     }
// });


// valueList.splice(0, valueList.length);
// tempList.splice(0, tempList.length);
// timeList.splice(0, timeList.length);
// // tempList.length = 0;
// // valueList.length = 0;
// // timeList.length = 0;
// day.length = 0;
//
// tempList = rock_a_dates.split("_");
// valueList = rock_a_values.split("_");
// for (const i of tempList) {
//     timeList.push(i.split(" ")[1]);
// }
// day = tempList[0].split(" ")[0];
//
// let RA_newDataList = valueList.slice(), RA_newTimeList = timeList.slice();
//
// const RockA_chart = new Chart(RockA_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: RA_newTimeList,
//         datasets: [{
//             label: day,
//             borderColor: window.chartColors.purple,
//             backgroundColor: 'transparent',
//             data: RA_newDataList,
//             fill: false,
//             pointRadius: 0.5,
//             borderWidth: 2,
//             spanGaps: false,
//             showLine: false
//         }]
//     },
//
//     //Configuration options go here
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         legend: {
//             position: 'bottom',
//             labels: {
//                 padding: 10
//
//             }
//         },
//         scales: {
//             xAxes: [{
//                 type: 'time',
//                 distribution: 'linear', //data are spread at the same distance from each other
//                 ticks: {
//                     // source: 'data',
//                     // autoSkip: true,
//                     // maxRotation: 0,
//                     // autoSkipPadding: 50
//                     beginAtZero: false,
//                     source: 'time',
//                     autoSkip: true,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//                 time: {
//                     format: timeFormat,
//                     unit: 'minute'
//                 },
//                 gridLines: {
//                     display: true
//                 }
//             }],
//             yAxes: [{
//                 // type: 'data',
//                 ticks: {
//                     source: 'data',
//                     autoSkip: false,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//
//                 gridLines: {
//                     display: true
//                 }
//             }]
//         },
//         hover: {
//             animationDuration: 0 // duration of animations when hovering an item
//         },
//         layout: {
//             padding: {left: 15, right: 15, top: 15, bottom: 15}
//         },
//         tooltip: {
//             bodySpacing: 4,
//             mode: "nearest",
//             intersect: 0,
//             position: "nearest",
//             xPadding: 10,
//             yPadding: 10,
//             caretPadding: 10
//         }
//     }
// });


// tempList.length = 0;
// valueList.length = 0;
// timeList.length = 0;
// day.length = 0;
//
// tempList = roll_a_dates.split("_");
// valueList = roll_a_values.split("_");
// for (const i of tempList) {
//     timeList.push(i.split(" ")[1]);
// }
// day = tempList[0].split(" ")[0];
//
//
// let RollA_newDataList = valueList.slice(), RollA_newTimeList = timeList.slice();
// const RollA_chart = new Chart(RollA_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: RollA_newTimeList,
//         datasets: [{
//             label: day,
//             borderColor: window.chartColors.red,
//             backgroundColor: 'transparent',
//             data: RollA_newDataList,
//             fill: false,
//             pointRadius: 0,
//             borderWidth: 2,
//             showLine: true
//         }]
//     },
//
//     //Configuration options go here
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         legend: {
//             position: 'bottom',
//             labels: {
//                 padding: 10
//                 // fontColor: window.chartColors.red,
//             }
//         },
//         scales: {
//             xAxes: [{
//                 type: 'time',
//                 distribution: 'linear', //data are spread at the same distance from each other
//                 ticks: {
//                     // source: 'data',
//                     // autoSkip: true,
//                     // maxRotation: 0,
//                     // autoSkipPadding: 50
//                     beginAtZero: false,
//                     source: 'time',
//                     autoSkip: true,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//                 time: {
//                     format: timeFormat,
//                     unit: 'minute'
//                 },
//                 gridLines: {
//                     display: true
//                 }
//             }],
//             yAxes: [{
//                 // time: 'time',
//                 ticks: {
//                     source: 'data',
//                     autoSkip: false,
//                     maxRotation: 0,
//                     autoSkipPadding: 10
//                 },
//
//                 gridLines: {
//                     display: true
//                 }
//             }]
//         },
//         hover: {
//             animationDuration: 0 // duration of animations when hovering an item
//         },
//         layout: {
//             padding: {left: 15, right: 15, top: 15, bottom: 15}
//         },
//         tooltip: {
//             bodySpacing: 4,
//             mode: "nearest",
//             intersect: 0,
//             position: "nearest",
//             xPadding: 10,
//             yPadding: 10,
//             caretPadding: 10
//         }
//     }
// });

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


function findNearestOTorMT(tooltipItems, combineTimeList, combineDataList_MT, combineDataList_OT, MT_newDataList, MT_newTimeList, OT_newDataList, OT_newTimeList) {
    if (combineDataList_MT[tooltipItems.index] === tooltipItems.yLabel) {// Current point is MT
        let MTTime = combineTimeList[tooltipItems.index];
        let OT_index = OT_newTimeList.indexOf(MTTime);
        if (OT_index !== -1) {
            return "Oven Temperature = " + OT_newDataList[OT_index] + " at " + MTTime
        } else {
            let min_interval = 24 * 60 * 60;
            let min_index = -1;
            for (OT_index = 0; OT_index < OT_newTimeList.length; OT_index++) {
                let OT_time = OT_newTimeList[OT_index];
                let interval = Math.abs(transformDateTimestamp(OT_time) - transformDateTimestamp(MTTime));
                if (interval < min_interval && OT_newDataList[OT_index] !== null) {
                    min_interval = interval;
                    min_index = OT_index;
                }
            }
            return "Oven Temperature = " + OT_newDataList[min_index] + " at " + OT_newTimeList[min_index];
        }
    } else { // Current point is OT
        let OTTime = combineTimeList[tooltipItems.index];
        let MT_index = MT_newTimeList.indexOf(OTTime);
        if (MT_index !== -1) {
            return "Mould Temperature = " + MT_newDataList[MT_index] + " at " + OTTime
        } else {
            let min_interval = 24 * 60 * 60;
            let min_index = -1;
            for (MT_index = 0; MT_index < MT_newTimeList.length; MT_index++) {
                let MT_time = MT_newTimeList[MT_index];
                let interval = Math.abs(transformDateTimestamp(MT_time) - transformDateTimestamp(OTTime));
                if (interval < min_interval && MT_newDataList[MT_index] !== null) {
                    min_interval = interval;
                    min_index = MT_index;
                }
            }
            return "Mould Temperature = " + MT_newDataList[min_index] + " at " + MT_newTimeList[min_index];
        }


    }
};
