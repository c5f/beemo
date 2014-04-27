'use strict';

var app = angular.module('beemoApp', [
    'ngRoute', 
    'restangular',
    'nvd3ChartDirectives'
]).

    // Route provider config
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.
  
        // Route provider URL path directives
        when('/', {redirectTo: '/dashboard'}).
        when('/dashboard', {controller:'DashboardCtrl', templateUrl: 'static/views/dashboard.html'}).
  
        // Static redirect for bower components
        otherwise({redirectTo: '/static/'});
  
    }]).

  // Restangular config for pagination
  config(function(RestangularProvider) {

      RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
          if (operation === "getList") {
                var newResponse = response.results;
                newResponse._resultmeta = {
                    "count": response.count,
                    "next": response.next,
                    "previous": response.previous
                };
                return newResponse;
          }
          return response;
      });

  });
