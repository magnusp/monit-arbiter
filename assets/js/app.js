'use strict';

/**
 * Magnus Persson 2014-03-09.
 */

var app = angular.module('arbiter', []).
    value('httpds',function monitHttpdFactory() {
        return [
            'http://10.0.1.16:2812',
            'http://10.0.1.16:2812'
        ];
    }).factory('monitMeta', function monitMetaFactory($http, $q, httpds) {
        /*var deferreds=[];
        httpds().map(function(item) {
            console.log(item+'/_status?format=xml');
            deferreds.push($http.get({method: 'GET', url: item+'/_status?format=xml'}));
        });
        $q.all(deferreds).then(function(result) {
            console.log(arguments);
        });*/
        return $http.get('/meta');
    });

app.controller('MonitCtrl', function ($scope, monitMeta) {
    monitMeta.then(function(result) {
        console.log(result);
    });
    /*$http.get('/meta').then(function (res) {
     console.log(res.data);
     $scope.monits = res.data;
     });*/
});