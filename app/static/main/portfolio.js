
let graph_prices = null;
let layout = null;
let current_stock = $("#stock_listing").first();
const CYCLE_TIME = 7500;
/*
Loads the detail of a stock using its stockid
stockid -- id of the stock
*/

function load_detail(id) {
    $.ajax({
        data: { id: id },
        type: 'POST',
        url: '/query_stock_info'
    }).done(function (data) {

        let name = data['corporate_name'];
        $('#stock_graph').text(name);

        graph_prices = [{
            x: data['dates'],
            y: data['prices'],
            mode: "lines"
        }];

        layout = {
            xaxis: { title: "Date", autorange: true },
            yaxis: { title: "Recorded Price", autorange: true },
            margin: {
                l: 75,
                r: 25,
                b: 75,
                t: 25,
                pad: 4
            }
        };

        Plotly.newPlot("price_plot", graph_prices, layout);

        if (data['status_code'] == 200) {
            $('#price').text(data['price']);
            $('#percent_change').text(data['percent_change'] + '%');
            $('#open').text(data['open']);
            $('#high').text(data['high']);
            $('#low').text(data['low']);
            $('#vol').text(data['volume']);
            $('#prev_close').text(data['prev_close']);
            $('#pe_ratio').text(data['pe_ratio']);
            $('#beta').text(data['beta']);
            $('#avg_vol').text(data['avg_volume']);
    
            if (data['percent_change'] < 0) {
                $('#percent_change').css('color', 'red');
            } else {
                $('#percent_change').css('color', 'green');
            }
    
            $('#detail_link').attr("href", "/stock/detail?stock=" + data['symbol']);
        }

    }).fail(function () {
        console.log("Failed AJAX Call");
    });
}
/*
cycle to the next stock
after 7.5 seconds
*/

function cycle_next_stock() {
    if (document.getElementById('auto_scroll').checked) {
        current_stock = current_stock.next();
        // if the last sock is reached, refesh the page
        if (current_stock.length == 0) {
            // sets an argument to keep the auto scroll enabled
            let url = '/index?auto=true';
            location.href = url;
        }
        current_stock.click();
    }
}


$(window).resize(function () {
    Plotly.newPlot("price_plot", graph_prices, layout);
});


$(document).ready(function () {
    let num = $('#stock_listing').first().attr('value');
    load_detail(num);

    setInterval(function () {
        cycle_next_stock();
    }, CYCLE_TIME);
});