'use strict';

// Base data service for storing Restangular-received analyzed data.
app.service('DataService', function ($scope, Restangular) {

    // Observer pattern
    this.observerCallbacks = [];

    this.registerObserverCallback = function (callback) {
        this.observerCallbacks.push(callback);
    };

    this.notifyObservers = function () {
        angular.forEach(observerCallbacks, function (callback) {
            callback();
        })
    };

    // Graphable data
    $scope.graphData = [];

    // Data loading function - notifies observers when DataService.graphData has been updated.
    this.loadData = function (filters) {
        console.log('Loading data...');
        Restangular.all('calls').getList().
            then(function (response) {

                if (filters) {
                    // TODO: Implement filters
                } else {
                    console.log("No filters, default slice.");
                    // Default take last 100 calls
                    response = response.slice(0,100);
                }

                $scope.graphData = response;
                this.notifyObservers();
            });
    };

    this.setGraphData = function (newGraphData) {
        graphData = newGraphData;
    };
});

// K-means controller for the Beemo cluster analysis.
app.controller('ClusterController', function ($scope, Restangular, DataService) {

    // Setup Restangular
    Restangular.setBaseUrl('/api/');
    Restangular.setRequestSuffix('/');

    // Pass in the analyze function as the callback to loadData.
    $scope.analyzeClicked = function () {
        DataService.loadData($scope.analyze);
    }

    /**
     * k-means analysis function
     *
     * This function takes parameters for the graph data and a specification containing the attributes to analyze as 
     * X and Y values as well as the k-number for this analysis.
     *
     * This function returns a list of graphable objects each with x, y, and cluster attributes.  X and y attribute 
     * correlate to their positions on the graph, while the cluster attribute specifies which cluster each object 
     * belongs to.
     */
    $scope.analyze = function (baseData) {

        var xAttribute = $scope.graphSpec.xAttrib.value;
        var yAttribute = $scope.graphSpec.yAttrib.value;
        var kNumber = $scope.graphSpec.kNumber;

        // Store a list of the Elements
        var elements = $scope.buildElementList(baseData, xAttribute, yAttribute);

        // Store a list of the Clusters
        var clusters = $scope.buildClusterList(kNumber, elements);

        var findClosestCluster = function (element) {
            var minDistance, closestCluster, cluster, distance;

            for (var index in clusters) {
                cluster = clusters[index];
                distance = cluster.getDistance(element);

                if (minDistance === undefined || distance < minDistance) {
                    minDistance = distance;
                    closestCluster = cluster;
                }
            }

            return closestCluster;
        }

        // Sentinel flag
        var finished = false;

        while (!finished) {

            finished = true;

            this.elements.forEach(function (element) {
                var closestCluster = findClosestCluster(element);

                if (element.cluster !== closestCluster) {
                    var oldCluster = element.cluster;

                    if (oldCluster !== null) {
                        oldCluster.removeElement(element);                    
                    }

                    closestCluster.addElement(element);

                    finished = false;
                }
            });
        }

        console.log("Elements:");
        console.log(elements);
        DataService.graphData = elements;
        console.log("DataService updated:");
        console.log(DataService.graphData);
    }

    // Bind the DataService to $scope.
    $scope.DataService = DataService;

    // Bind database data schema to $scope
    $scope.schema = [
        {value: 'adherence_score',  name: 'Adherence Score', type: 'float'},
        // {value: 'completed_date',  name: 'Completed Date', type: 'date'},
        {value: 'fat_grams',  name: 'Fat Grams', type: 'int'},
        {value: 'fiber_grams',  name: 'Fiber Grams', type: 'int'},
        {value: 'fruit_servings',  name: 'Fruit Servings', type: 'int'},
        {value: 'number',  name: 'Call Number', type: 'int'},
        {value: 'steps',  name: 'Step Count', type: 'int'},
        {value: 'veg_servings', name: 'Vegetable Servings', type: 'int'}
    ];

    // Store the k-means analysis information in a $scope variable.
    $scope.graphSpec = {
        xAttrib: $scope.schema[0],
        yAttrib: $scope.schema[1],
        kNumber: 3
    };

    /**
     * Builds the list of elements from a set of objects and two attributes.
     */
    $scope.buildElementList = function (objects, xAttribute, yAttribute) {

        var results = objects.map(function (object) {
            return new $scope.Element(object[xAttribute], object[yAttribute], object);
        });

        return results;
    }

    /**
     * Builds the list of k new clusters and seeds them with elements (if there are enough).
     */
    $scope.buildClusterList = function (kNumber, elements) {
        var clusters = [];

        for (var i = 0; i < kNumber; ++i) {
            // Create a new
            clusters.push(new $scope.Cluster());

            // There are many ways to seed the cluster list, but this requires the least extra logic.
            if (i < elements.length)
            clusters[i].addElement(elements[i]);
        }

        return clusters;
    }

});

// Graph controller for the 
app.controller('GraphController', function ($scope, DataService) {

    var graphDataUpdated = function () {
        console.log("graphData updated from DataService.");
        $scope.graphData = DataService.graphData;
    }

    // Register the observer callback with DataService.
    DataService.registerObserverCallback(graphDataUpdated);

    // TODO: remove this binding
    window.scope = $scope;
});
