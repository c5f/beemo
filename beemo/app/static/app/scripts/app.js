'use strict';

var app = angular.module('beemoApp', [
  'ngRoute',
  'nvd3ChartDirectives'
]);

// Route provider config
app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

  // Route provider URL path directives
  $routeProvider.
    when('/', {redirectTo: '/cluster'}).
    when('/dashboard', {controller:'DashboardCtrl', templateUrl: 'static/views/dashboard.html'}).
    when('/cluster', {controller:'ClusterController', templateUrl: 'static/views/cluster.html'}).

    // Static redirect for bower components
    otherwise({redirectTo: '/static/'});

}]);
