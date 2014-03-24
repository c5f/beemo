'use strict';

angular.module('beemoApp', [
  'ngRoute',
  'restangular',
])
  .config(function ($routeProvider, RestangularProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/views/main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/static/'
      });

    RestangularProvider.setBaseUrl('/api/');
  });
