$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })
    var url = $('#pagelink').data('url')
    var percentage = []
    var accepted = []
    var rejected =[]
    var salespercentage = []


    $.ajax({
        type: 'POST',
        data: { 'status': 'count' },
        url: url,
        success: function (response) {
            console.log(response.data)
            var data = response.data
            var Accepted = response.accepted
            var Rejected = response.rejected
            for (var i = 0; i < data.length; i++) {
                percentage.push(data[i])
            }
            for (var i = 0; i < Accepted.length; i++) {
                accepted.push(Accepted[i])
            }for (var i = 0; i < Rejected.length; i++) {
                rejected.push(Rejected[i])
            }
            var ctx1 = $("#worldwide-sales").get(0).getContext("2d");
            var list = [15, 30, 55, 65, 60, 80, 95, 90, 50, 60, 45, 93]
            console.log(list)
            var myChart1 = new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: "Total Sales",
                        data: percentage,
                        backgroundColor: "rgba(0, 156, 255, .7)"
                    },
                    {
                        label: "Accepted ",
                        data: accepted,
                        backgroundColor: "rgba(0, 156, 255, .5)"
                    },
                    {
                        label: "Cancelled ",
                        data: rejected,
                        backgroundColor: "rgba(0, 156, 255, .3)"
                    }



                    ]
                },
                options: {
                    responsive: true
                }
            });



        }
    })
    $.ajax({
        type: 'POST',
        url: url,
        data: { 'status': 'sales' },
        success: function (response) {
            console.log(response.data)

            var datas = response.data
            console.log(datas)
            for (var i = 0; i < datas.length; i++) {
                salespercentage.push(datas[i])
            }
            var ctx2 = $("#salse-revenue").get(0).getContext("2d");
            var myChart2 = new Chart(ctx2, {
                type: "line",
                data: {
                    labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: "Sales",
                        data: salespercentage,
                        backgroundColor: "rgba(0, 156, 255, .5)",
                        fill: true
                    }
                    ]
                },
                options: {
                    responsive: true
                }
            });




        }
    })

})