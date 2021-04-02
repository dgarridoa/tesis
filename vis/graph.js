export function graph(selector, url){
    var margin = {top: 25, right: 30, bottom: 20, left: 30}
    var width = 800
    var height = 400
    var thickness = 5

    function split(str){
        var mylist = str.split("-");
        var x = Number(mylist[0])
        var y = Number(mylist[1])
        return Array(x,y)
    }
    var svg = d3.select(selector)
        .append("svg")
            .classed("svg-graph", true)
            // .attr("width", 1000)
            // .attr("height", 1000)
        .call(d3.zoom().on("zoom", function () {
            svg.attr("transform",d3.event.transform)
        }))
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

    d3.json(url, function(data) {
        // x axis
        var x = d3.scaleLinear()
            .domain([1, d3.max(data.nodes, d=>d.epoch)])
            .range([margin.left, margin.left+width-margin.right-40])
            .interpolate(d3.interpolateRound);
        
        // y axis
        var y = d3.scaleLinear()
            .domain([1, d3.max(data.nodes, d=>d.id)])
            .range([margin.top+height-margin.bottom, margin.top])
            .interpolate(d3.interpolateRound)

        //// edges ////

        // edge thick
        var thick = d3.scaleLinear()
            .domain([d3.min(data.edges, d => d.w), 0, d3.max(data.edges, d => d.w)])
            .range([thickness, 1, thickness])

         // tooltips
        d3.select(selector)
            .append("div")
                .attr("class", "edgeTooltip")
                .style("position", "absolute")
                .style("visibility", "hidden")
                .style("font-size", "10px")
                .style("background-color", "white")
                .style("background-margin", "5px")
                .style("border", "solid")
                .style("border-width", "1px")
                .style("border-radius", "2px")
                
        function edgeMouseover(d) {
            d3.select(this)
                .style("stroke", "black")

            d3.select(".edgeTooltip")
            .style("visibility", "visible")
            .html(d.w.toFixed(3))
                .style("left", d3.event.pageX+10 + "px")
                .style("top", d3.event.pageY + "px")
        }
        function edgeMouseout(d) {
            d3.select(this)
            .style("stroke", "#999")

            d3.select(".edgeTooltip")
                .transition()
                .delay(1000)
                .style("visibility", "hidden")
        }

        // edges   
        svg.append("g")
        .selectAll("edges")
        .data(data.edges)
        .enter()
        .append("line")
            .attr("class", d=>"line"+d.s+"_"+d.t)
            .attr("x1", d=>x(split(d.s)[0]))
            .attr("y1", d=>y(split(d.s)[1]))
            .attr("x2", d=>x(split(d.t)[0]))
            .attr("y2", d=>y(split(d.t)[1]))
            .style("stroke", "#999")
            .attr("stroke-width", d=>thick(d.w))
            .style("opacity", d=>2*d.w)
            .on("mouseover", edgeMouseover)
            .on("mouseleave", edgeMouseout)

        //// nodes ////

        // node size
        var color = d3.scaleSequential()
            .domain([0, d3.max(data.nodes, d => d.size)])
            .interpolator(d3.interpolateViridis)

        // tooltip
        d3.select(selector)
            .append("div")
                .attr("class", "nodeTooltip")
                .style("position", "absolute")
                .style("visibility", "hidden")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("font-size", "10px")

        function nodeMouseover(d) {
            d3.select(this)
                .attr("stroke-width", 2)

            d3.select(".nodeTooltip")
                .style("visibility", "visible")
                .html(d.topn+"<br> size:"+d.size.toFixed(3))
                  .style("left", d3.event.pageX+10 + "px")
                  .style("top", d3.event.pageY+ "px")
            // input the topic id in menu?
            var topicID = "ldavis-topic"+d.id;
        
            var element = document.getElementById(topicID);
            element.addEventListener("mouseover", function() {
            console.log("Event triggered");
            });

            var event = new MouseEvent("mouseover", {
            "view": window,
            "bubbles": true,
            "cancelable": true
            });

            element.dispatchEvent(event); 
        }

        function nodeMouseout(d) {
            d3.select(this)
            .attr("stroke-width", 1)

            d3.select(".nodeTooltip")
            .transition()
            .delay(100)
            .style("visibility", "hidden")

            var topicID = "ldavis-topic"+d.id;
        
            var element = document.getElementById(topicID);
            element.addEventListener("mouseover", function() {
            console.log("Event triggered");
            });

            var event = new MouseEvent("mouseover", {
            "view": window,
            "bubbles": true,
            "cancelable": true
            });

            element.dispatchEvent(event); 
  
        }

        // nodes
        svg.append("g")
        .selectAll("nodes")
        .data(data.nodes)
        .enter()
        .append("circle")
            .attr("class", d=>"circle"+d.epoch+"_"+d.id)
            .attr("cx", d=>x(d.epoch))
            .attr("cy", d=>y(d.id))
            .attr("r", 10)
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .style("fill", d=>color(d.size))
        .on("mouseover", nodeMouseover)
        .on("mouseout", nodeMouseout)
        
        //// legend /////

        // y axis bar
        var yBar = d3
            .scaleLinear()
            .domain([0, d3.max(data.nodes, d => d.size)])
            .range([margin.top+height-margin.bottom, margin.top])

        var lastEpoch = Math.max.apply(null, data.nodes.map(d=>d.epoch));
        
        // array with n elements equi-spaced between [start, end]
        function linspaceArray(start, end, n) {
            var arr = [];
            var step = (end - start) / (n - 1);
            for (var i = 0; i < n; i++) {
                arr.push(start + (step * i));
            }
        return arr;
        }
        var mydata = linspaceArray(0, Math.max.apply(null, data.nodes.map(d=>d.size)), 1000)
        
        // legend
        svg.append("g")
        .selectAll("rect")
        .data(mydata)
        .enter()
        .append("rect")
            .attr("x", x(lastEpoch)+20)
            .attr("y", d=>yBar(d))
            .attr("width", 20)
            .attr("height", 1)
            .style("fill", d=>color(d))
        var ticksPosition = x(lastEpoch)+40
        
        // thick
        svg.append("g")
        .attr("transform", "translate("+ticksPosition+","+0+")")  
        .call(d3.axisRight(yBar)
        .tickFormat(function(d){
            return d;
        }).ticks(5))
        .append("text")
        .attr("transform", "rotate(90)")
            .attr("x", height/2+margin.top)
            .attr("y", -40)
        .attr("text-anchor", "end")
        .attr("stroke", "black")
        .attr("stroke-width", 1.0)
        .text("Topic Size");
    })
};