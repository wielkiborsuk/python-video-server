'use strict';

angular.module('clientApp', [])
  .controller('MainCtrl', function ($scope, $http) {
    $scope.curr = '';

    //$http.get($scope.prefix + '/list/').then(function (res) {
      //console.log(res);
      //$scope.list = res.data;
    //});

    $scope.select = function (video) {
      console.log('hahaha')
      $scope.curr = video;
      //$scope.player.src = $scope.filePrefix + '/' + video;
      $scope.player.src = video;
      $scope.player.children()[0].src = video;
      $scope.player.load();
      $scope.player.play();
    }

    function arr_del(arr, obj) {
      var idx = arr.indexOf(obj);
      if (idx > -1) {
        arr.splice(idx, 1);
      }
    }
  })
  .directive('player', function() {
    return {
      link: function (scope, element, attrs, controller) {
        scope.player = element[0];
        scope.player.volume = 0.2;
      }
    };
  });
