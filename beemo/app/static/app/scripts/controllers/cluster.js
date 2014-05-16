'use strict';

// Data service
app.service('DataService', function ($http, $log) {

    this.data = [];

    var filterCalls = function (calls, filters) {
        if (filters === undefined || filters.length == 0) {
            // If no filters were provided, take the first 200 calls
            calls = calls.slice(0, 200);
            $log.debug('Taking first 200 calls. No filters yet.');
        } else {
            // TODO: Implement filters
            $log.error('Somehow got into the unimplemented filterCalls else block...\nfilters:' + filters);
            calls = [];
        }

        return calls;
    }

    this.loadData = function (callback, filters) {
        $http.get('/api/calls/').success(function (response) {

            var result = filterCalls(response, filters);

            callback(result);
        });
    };
});

// Analysis service
app.service('KMeansAnalysisService', function ($log) {

    // Elements list
    var elements = [];

    // Clusters list
    var clusters = [];

    // Scale for X
    var xScale = 1;

    // Scale for Y
    var yScale = 1;

    /**
     * Element class definition.
     */
    var Element = function (xVal, yVal, object) {

        // Store the coordinates
        this.location = { x: null, y: null };

        this.location.x = (xVal) ? xVal : 0;
        this.location.y = (yVal) ? yVal : 0;
        this.location.size = 1;

        // Store a reference to the original data object
        this.object = object;

        // Store a reference to a parent Cluster - initialized to null and updated by Cluster methods
        this.cluster = null;
    }

    /**
     * Cluster class definition.
     */
    var Cluster = function () {

        // Store a list of elements
        this.elements = [];

        // Store the centroid of this Cluster
        this.centroid = { x: null, y: null };

        // Function for calculating and updating the Centroid of this Cluster - called by add/remove
        this.updateCentroid = function () {

            var xTotal = 0;
            var yTotal = 0;
            var element;

            // TODO: add support for date clustering
            for (var index in this.elements) {

                element = this.elements[index];

                xTotal += Number(element.location.x);
                yTotal += Number(element.location.y);
            }

            // Update centroid coordinates.
            this.centroid.x = xTotal / this.elements.length;
            this.centroid.y = yTotal / this.elements.length;
        }

        // Function for adding an Element to this Cluster
        this.addElement = function (newElement) {
            this.elements.push(newElement);

            // Update the Element's Cluster reference
            newElement.cluster = this;

            // Update this Cluster's centroid
            this.updateCentroid();
        }

        // Function for removing an Element from this Cluster
        this.removeElement = function (element) {
            
            var index = this.elements.indexOf(element);

            if (index === -1) {

                // Stop if the Element does not belong to this Cluster
                $log.error("Trying to remove an Element from a Cluster that doesn't contain it!");

                return null;
            } else {

                // Remove the Element from this Cluster's collection
                var oldElement = this.elements.splice(index, 1)[0];

                // Remove the Element's Cluster reference
                oldElement.cluster = null;

                // Update this Cluster's centroid
                this.updateCentroid();

                // Return the old Element to be added to another Cluster
                return oldElement;
            }            
        }

        // Function for calculating distance to this cluster
        this.getDistance = function (element) {
            return Math.sqrt(
                Math.pow(Math.abs(element.location.x - this.centroid.x) * xScale, 2) +
                Math.pow(Math.abs(element.location.y - this.centroid.y) * yScale, 2)
                );
        }
    }

    // Builds the list of Elements from base objects and the two attributes to be compared
    var buildElementList = function (objects, xAttribute, yAttribute) {

        // Map creates a new array, so we don't have to worry about emptying the old one
        return objects.map(function (object) {
            return new Element(object[xAttribute], object[yAttribute], object);
        });
    };

    // Builds the list of Clusters from the k-number and a list of Elements
    var buildClusterList = function (kNumber) {

        var newClusters = [];

        for (var i = 0; i < kNumber; ++i) {
            // Create a new Cluster
            newClusters.push(new Cluster());
        }

        return newClusters;
    };

    // Finds the closest cluster to a given Element
    var findClosestCluster = function (element) {
        var minDistance, closestCluster, distance;

        clusters.forEach(function (cluster) {
            distance = cluster.getDistance(element);

            if (minDistance === undefined || distance < minDistance) {
                minDistance = distance;
                closestCluster = cluster;
            }
        });

        return closestCluster;
    };

    // Seeds the clusters with initial data
    var seedClusters = function () {
        var kNumber = clusters.length;

        if (kNumber > 0) {

            // Special case if we have fewer elements than clusters
            if (elements.length < kNumber) {
                // Just seed with what we have
                elements.forEach(function (element, index) {
                    clusters[index].addElement(element);
                });
            } else {
                // Add one element to each cluster
                clusters.forEach(function (cluster, index) {
                    cluster.addElement(elements[index]);
                });

                // Then add every other element to its closest cluster
                elements.forEach(function (element, index) {
                    if (element.cluster === null) {
                        findClosestCluster(element).addElement(element);
                    }
                });
            }
        }
    };

    // Finds scales based on ranges.
    var updateScales = function () {
        var xMin, xMax, yMin, yMax, xVals, yVals, xRng, yRng;

        // Reset scales
        xScale = 1;
        yScale = 1;

        // Generate value lists
        var xVals = elements.map(function (element) {
            return element.location.x;
        });

        var yVals = elements.map(function (element) {
            return element.location.y;
        })

        // Find min/max/range
        xMin = Math.min.apply(Math, xVals);
        xMax = Math.max.apply(Math, xVals);
        yMin = Math.min.apply(Math, yVals);
        yMax = Math.max.apply(Math, yVals);
        xRng = xMax - xMin;
        yRng = yMax - yMin;

        // Always scale up
        if (xRng > yRng) {
            yScale = xRng / yRng;
        } else {
            xScale = yRng / xRng;
        }
    }

    // Analysis function
    this.analyze = function (data, callback) {

        elements = buildElementList(data.callData, data.xAttrib.value, data.yAttrib.value);
        clusters = buildClusterList(data.kNumber);

        updateScales();
        seedClusters();

        // Sentinel flag
        var finished = false;

        while (!finished) {

            finished = true;

            elements.forEach(function (element) {
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

        callback(clusters);
    }
});

// Graph/page controller
app.controller('ClusterController', function ($scope, $log, DataService, KMeansAnalysisService) {

    // Bind database data schema to $scope
    // TODO: Pull this schema from an API request
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

    // Graph data
    $scope.graphData = {
        // Form parameters
        xAttrib: $scope.schema[0],
        yAttrib: $scope.schema[1],
        kNumber: 3,

        // Data filters
        filters: [],

        // Base dataset
        callData: [],

        // Graphable data
        graphData: [],

        // nvd3 functions
        xFunction: function () {
            return function (element) {
                return element.x;
            }
        },

        yFunction: function () {
            return function (element) {
                return element.y;
            }
        },
    };

    // Graph elements
    $scope.elements = [];

    // Analyze action
    $scope.analyzeClicked = function () {
        KMeansAnalysisService.analyze($scope.graphData, function (graphClusters) {

            // Empty existing graphData
            $scope.graphData.graphData = [];

            var clusterCount = 1;

            // Massage data into nvd3 format.
            graphClusters.forEach(function (cluster) {
                $scope.graphData.graphData.push({
                    key: (cluster.elements.length > 0) ? "Cluster " + clusterCount++ : "Empty Cluster",
                    values: cluster.elements.map(function (element) {
                        return { x:element.location.x, y:element.location.y, size: element.location.size};
                    }),
                    cluster: cluster
                });
            });

            // Add cluster centroids to their own group
            // $scope.graphData.graphData.push({
            //     key: "Centroids",
            //     values: graphClusters.map(function (cluster) {
            //         return { x:cluster.centroid.x, y:cluster.centroid.y, size: cluster.elements.length * 5};
            //     }),
            //     clusters: graphClusters
            // });
        });
    };

    // Load calls and assign them back to the $scope variable.
    DataService.loadData(function (calls) {
        $scope.graphData.callData = calls;
    }, $scope.graphData.filters);

    // TODO: Remove this awful binding.
    window.scope = $scope;

});
