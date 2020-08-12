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

    // OT_newDataList = valueList.slice();
    // OT_newTimeList = timeList.slice();


    const timeFormat = 'h:mm:ss';
    ot_decimation(valueList, timeList, OT_newDataList, OT_newTimeList, 0, 400);
    // const OT_chart = new Chart(OT_line_chart, {
    //     // The type of chart we want to create
    //     type: 'line',
    //
    //     // The data for our dataset
    //     data: {
    //         labels: OT_newTimeList,
    //         datasets: [{
    //             label: 'Oven Temperature',
    //             borderColor: window.chartColors.blue,
    //             backgroundColor: 'transparent',
    //             data: OT_newDataList,
    //             fill: false,
    //             pointRadius: 0,
    //             borderWidth: 2
    //
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
    //                 // fontColor: window.chartColors.blue,
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
    //
    //                 gridLines: {
    //                     display: true
    //                 }
    //             }],
    //             yAxes: [{
    //                 time: 'time',
    //                 ticks: {
    //                     source: 'data',
    //                     autoSkip: true,
    //                     maxRotation: 0,
    //                     autoSkipPadding: 10,
    //                     suggestedMin: 0,
    //                     suggestedMax: 500
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

    // const MT_chart = new Chart(MT_line_chart, {
    //     // The type of chart we want to create
    //     type: 'line',
    //
    //     // The data for our dataset
    //     data: {
    //         labels: MT_newTimeList,
    //         datasets: [{
    //             label: day,
    //             borderColor: window.chartColors.green,
    //             backgroundColor: 'transparent',
    //             data: MT_newDataList,
    //             fill: false,
    //             pointRadius: 0,
    //             borderWidth: 2,
    //             spanGaps: false
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
    //                 time: 'time',
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

    // const CT_chart = new Chart(CT_line_chart, {
    //     // The type of chart we want to create
    //     type: 'line',
    //
    //     // The data for our dataset
    //     data: {
    //         labels: CT_newTimeList,
    //         datasets: [{
    //             label: day,
    //             borderColor: window.chartColors.orange,
    //             backgroundColor: 'transparent',
    //             data: CT_newDataList,
    //             fill: false,
    //             pointRadius: 0,
    //             borderWidth: 2,
    //             spanGaps: false
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

    // {#------------CT_MT_mix_chart------------#}

    let labels = [];
    let label_points;
    if (labels_str !== undefined) {
        let str;
        for (str of labels_str.split("_")) {
            if (str === '1.0') {
                labels.push('Recipe 1')
            } else if (str === '2.0') {
                labels.push('Recipe 2')
            } else if (str === '3.0') {
                labels.push('Recipe 3')
            } else if (str === '4.0') {
                labels.push('Recipe 4')
            }
        }
        label_points = label_points_str.split("_");
    }

    let combineDataList_CT = [], combineTimeList = [], combineDataList_MT = [], combineDataList_OT = [];

    CombineMTandCTandOT(CT_newDataList, CT_newTimeList, MT_newDataList, MT_newTimeList, OT_newDataList, OT_newTimeList, combineDataList_CT, combineDataList_MT, combineDataList_OT, combineTimeList);

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
                    if (labels_str !== undefined) {
                        entering = false;
                        leaving = false;
                        if (showLabel) {
                            for (let i = 0; i < labels.length; i++) {
                                setTimeout(drawTooltip('#E80A15', '#E80A15', label_points[i], this, labels[i]), 50);
                            }
                        }
                        $('#CT_MT_mix_line_chart').hover(function (e) {
                            // $('.chart--root').css('pointer-events', 'none')
                            if (e.type === 'mouseenter' && entering === false) {
                                entering = true;
                                console.log("mouseenter");
                                showLabel = false;
                                CT_MT_mix_chart.update();
                            } else if (e.type === 'mouseleave' && leaving === false) {
                                leaving = true;
                                console.log("mouseleave");
                                showLabel = true;
                                CT_MT_mix_chart.update();
                            }
                        });
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
                enabled: true,
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10,
                // callbacks: {
                //     label: function (tooltipItems, data) {
                //         let multiStringText = [tooltipItems.yLabel];
                //         multiStringText.push(findNearestOTorMT(tooltipItems, combineTimeList, combineDataList_MT, combineDataList_OT));
                //         return multiStringText;
                //     }
                // }
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
            responsive: true,
            responsiveAnimationDuration: 0, // animation duration after a resize
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
            tooltip: {
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
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
            responsive: true,
            responsiveAnimationDuration: 0, // animation duration after a resize
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
            tooltip: {
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
            }
        }
    });

    // document.getElementById("loading").style = "visibility: hidden";
    $("#search_button").prop("disabled", false);
    $("#search_button").children().filter("span").remove();
    $("#search_button").text("Search");
}

// // {#-------Oven_Temperature_PV--------#}
// var ot_names = Data.ot_names;
// var ot_dates = Data.ot_dates;
// var ot_values = Data.ot_values;
// var ot_validities = Data.ot_validities;
// var ot_mills = Data.ot_mills;
//
// // {#---------Mould_Temperature_PV--------#}
// var mt_names = Data.mt_names;
// var mt_dates = Data.mt_dates;
// var mt_values = Data.mt_values;
// var mt_validities = Data.mt_validities;
// var mt_mills = Data.mt_mills;
//
//
// // {#-------Cooling_Temperature_PV--------#}
// var ct_names = Data.ct_names;
// var ct_dates = Data.ct_dates;
// var ct_values = Data.ct_values;
// var ct_validities = Data.ct_validities;
// var ct_mills = Data.ct_mills;
//
// // {#------------Rock_Angle_PV------------#}
// var rock_a_names = Data.rock_a_names;
// var rock_a_dates = Data.rock_a_dates;
// var rock_a_values = Data.rock_a_values;
// var rock_a_validities = Data.rock_a_validities;
// var rock_a_mills = Data.rock_a_mills;
//
//
// // {#------------Roll_Angle_PV------------#}
// var roll_a_names = Data.roll_a_names;
// var roll_a_dates = Data.roll_a_dates;
// var roll_a_values = Data.roll_a_values;
// var roll_a_validities = Data.roll_a_validities;
// var roll_a_mills = Data.roll_a_mills;
//
//
// //Oven_Temperature_PV
// const OT_line_chart = document.getElementById('OT_line_chart').getContext('2d');
// //Mould_Temperature_PV
// const MT_line_chart = document.getElementById('MT_line_chart').getContext('2d');
// //Cooling_Temperature_PV
// const CT_line_chart = document.getElementById('CT_line_chart').getContext('2d');
// //Mould_Cooling_mix_PV
// const CT_MT_mix_line_chart = document.getElementById('CT_MT_mix_line_chart').getContext('2d');
// //Rock_Angle_PV
// const RockA_line_chart = document.getElementById('RockA_line_chart').getContext('2d');
// //Roll_Angle_PV
// const RollA_line_chart = document.getElementById('RollA_line_chart').getContext('2d');
//
//
// let tempList = ot_dates.split("_");
// let valueList = ot_values.split("_");
//
// let timeList = [];
// for (const i of tempList) {
//     timeList.push(i.split(" ")[1]);
// }
// let day = tempList[0].split(" ")[0];
//
//
// let OT_newDataList = [], OT_newTimeList = [];

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

// decimation(valueList, timeList, OT_newDataList, OT_newTimeList, 0, 500);

// OT_newDataList = valueList.slice();
// OT_newTimeList = timeList.slice();
//
// var timeFormat = 'h:mm:ss';
// const OT_chart = new Chart(OT_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: OT_newTimeList,
//         datasets: [{
//             label: day,
//             borderColor: window.chartColors.blue,
//             backgroundColor: 'transparent',
//             data: OT_newDataList,
//             fill: false,
//             pointRadius: 0,
//             borderWidth: 2
//
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
//                 // fontColor: window.chartColors.blue,
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
//
//                 gridLines: {
//                     display: true
//                 }
//             }],
//             yAxes: [{
//                 time: 'time',
//                 ticks: {
//                     source: 'data',
//                     autoSkip: true,
//                     maxRotation: 0,
//                     autoSkipPadding: 10,
//                     suggestedMin: 0,
//                     suggestedMax: 500
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
//
// valueList.splice(0, valueList.length);
// tempList.splice(0, tempList.length);
// timeList.splice(0, timeList.length);
// // tempList.length = 0;
// //valueList.length = 0;
// // timeList.length = 0;
// day.length = 0;
//
// tempList = mt_dates.split("_");
// valueList = mt_values.split("_");
// for (const i of tempList) {
//     timeList.push(i.split(" ")[1]);
// }
// day = tempList[0].split(" ")[0];


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

// let MT_newDataList = [], MT_newTimeList = [];
// MT_decimation(valueList, timeList, MT_newDataList, MT_newTimeList, 20, 200);
//
// const MT_chart = new Chart(MT_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: MT_newTimeList,
//         datasets: [{
//             label: day,
//             borderColor: window.chartColors.green,
//             backgroundColor: 'transparent',
//             data: MT_newDataList,
//             fill: false,
//             pointRadius: 0,
//             borderWidth: 2,
//             spanGaps: false
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
//                 time: 'time',
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
//
//
// valueList.splice(0, valueList.length);
// tempList.splice(0, tempList.length);
// timeList.splice(0, timeList.length);
// // tempList.length = 0;
// // valueList.length = 0;
// // timeList.length = 0;
// day.length = 0;
//
// tempList = ct_dates.split("_");
// valueList = ct_values.split("_");
// for (const i of tempList) {
//     timeList.push(i.split(" ")[1]);
// }
// day = tempList[0].split(" ")[0];
//
//
// let CT_newDataList = [], CT_newTimeList = [];

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

// CT_decimation(valueList, timeList, CT_newDataList, CT_newTimeList, 0, 200);
//
// const CT_chart = new Chart(CT_line_chart, {
//     // The type of chart we want to create
//     type: 'line',
//
//     // The data for our dataset
//     data: {
//         labels: CT_newTimeList,
//         datasets: [{
//             label: day,
//             borderColor: window.chartColors.orange,
//             backgroundColor: 'transparent',
//             data: CT_newDataList,
//             fill: false,
//             pointRadius: 0,
//             borderWidth: 2,
//             spanGaps: false
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

function findNearestOTorMT(tooltipItems, combineTimeList, combineDataList_MT, combineDataList_OT) {
    if (combineDataList_MT[tooltipItems.index] === tooltipItems.yLabel) {
        let OTValues = combineDataList_OT[tooltipItems.index];

        if (OTValues != null) {
            return "Oven Temperature: " + OTValues + " at " + combineTimeList[tooltipItems.index]
        } else {
            let forwardIndex, backwardIndex; // Record how far seeking forward and backward
            let forwardValue, backwardValue; // Record nearest value forward and backward
            for (forwardIndex = tooltipItems.index; forwardIndex < combineDataList_OT.length; forwardIndex++) {
                if (combineDataList_OT[forwardIndex] != null) {
                    forwardValue = combineDataList_OT[forwardIndex];
                    break;
                }
            }
            for (backwardIndex = tooltipItems.index; backwardIndex >= 0; backwardIndex--) {
                if (combineDataList_OT[backwardIndex] != null) {
                    backwardValue = combineDataList_OT[backwardIndex];
                    break;
                }
            }
            if (Math.abs(tooltipItems.index - forwardIndex) >= Math.abs(tooltipItems.index - backwardIndex)) {
                // The nearest point is forward than current point
                return "Oven Temperature: " + forwardValue + " at " + combineTimeList[forwardIndex]
            } else {
                // The nearest point is backward than current point
                return "Oven Temperature: " + backwardValue + " at " + combineTimeList[backwardIndex]
            }
        }
    } else {
        let MTValues = combineDataList_MT[tooltipItems.index];
        if (MTValues != null) {
            return "Mould Temperature: " + MTValues + " at " + combineTimeList[tooltipItems.index]
        } else {
            let forwardIndex, backwardIndex; // Record how far seeking forward and backward
            let forwardValue, backwardValue; // Record nearest value forward and backward
            for (forwardIndex = tooltipItems.index; forwardIndex < combineDataList_MT.length; forwardIndex++) {
                if (combineDataList_MT[forwardIndex] != null) {
                    forwardValue = combineDataList_MT[forwardIndex];
                    break;
                }
            }
            for (backwardIndex = tooltipItems.index; backwardIndex >= 0; backwardIndex--) {
                if (combineDataList_MT[backwardIndex] != null) {
                    backwardValue = combineDataList_MT[backwardIndex];
                    break;
                }
            }
            if (Math.abs(tooltipItems.index - forwardIndex) >= Math.abs(tooltipItems.index - backwardIndex)) {
                // The nearest point is forward than current point
                return "Mould Temperature: " + forwardValue + " at " + combineTimeList[forwardIndex]
            } else {
                // The nearest point is backward than current point
                return "Mould Temperature: " + backwardValue + " at " + combineTimeList[backwardIndex]
            }
        }
    }
}
