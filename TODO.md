beemo
=====

#### backend

* good for now - may need some tweaks to JSON output fields/formatting

#### frontend

* AngularJS and Restangular
    * install AngularJS
    * install Restangular
    * configure pagination
    * add data to scope
        
```javascript
// Restangular setup
Restangular.setBaseUrl("/appname/api/");
Restangular.setRequestSuffix("/");

// Scope binding
$scope.participants = Restangular.all("participant");
```

    * render with D3
        
```javascript
// get the container
var graph = d3.select(".container-class");

// the the bar selection
var bar = graph.selectAll("div");

// join the data to the bar selection
var barUpdate = bar.data(list-of-objects);

// .enter() defines behavior when new data is encountered for which a DOM element does not already exist.
var barEnter = barUpdate.enter().append("div");

// set the style of the bar
barEnter.style("width", function(d) { return d * 10 + "px"; });
barEnter.text(function(d) { return d });

// chained
d3.select(".container-class")
    .selectAll("div")
        .data(participants)
    .enter().append("div")
        .style("height", function(participant) { return participant.adherenceScore * 50 + "px"; })
        .text(function(participant) { return participant.adherenceScore });

// scaling function
var x = d3.scale.linear()
    .domain([0, d3.max(chartDataToScale)])
    .range([0, MAX_CHART_RANGE])

// applying the scaling function
d3.select(".chart")
    .selectAll("div")
        .data(data)
    .enter().append("div")
        .style("width", function(d) { return x(d) + "px"; })
        .text(function(d) { return d; });
```
