
let graph_prices = null;
let layout = null;


function load_detail(stock_symbol) {
    $.ajax({
        data: { symbol: stock_symbol },
        type: 'POST',
        url: '/stock/stock_info'
    }).done(function (data) {

        raw_data = data['data'][stock_symbol]
        console.log(raw_data)
        opened = []
        close_arr = []
        high = []
        low = []
        timestamps = []
        raw_data.forEach(element => {
            opened.push(element['open'])
            close_arr.push(element['close'])
            high.push(element['high'])
            low.push(element['low'])
            timestamps.push(element['timestamp'])
        });
        chart_parameters = [{
            x: timestamps,
            close: close_arr,
            decreasing: {line: {color: '#c23010'}},
            high: high,
            increasing: {line: {color: '#10c260'}}, 
            line: {color: 'rgba(31,119,180,1)'},
            low: low,
            open: opened,
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
        }];

        var layout = {
            // dragmode: 'zoom', 
            margin: {
              r: 10, 
              t: 25, 
              b: 40, 
              l: 60
            }, 
            showlegend: false, 
            // xaxis: { title: "Date", autorange: true }, 
            yaxis: {
              title: "Price",
              domain: [0,1],
              range: [Math.min(opened),Math.max(close_arr)],
              cliponaxis: false, 
              type: 'linear'
            }
          };

        Plotly.newPlot("price_plot", chart_parameters, layout);

        var open_price = "Open price: " + raw_data.slice(-1)[0]['open']
        var close_price = "Close price : " + raw_data.slice(-1)[0]['close']
        $('#open_price').text(open_price);
        $('#close_price').text(close_price);
        console.log(open_price)

    }).fail(function () {
        console.log("Failed AJAX Call");
    });
}


function cycle_next_stock() {
    current_stock = current_stock.next();
    if (current_stock.length == 0) {
        current_stock = $("#stock_listing").first();
    }
    current_stock.click();
}


$(window).resize(function () {
    Plotly.newPlot("price_plot", chart_parameters, layout);
});

