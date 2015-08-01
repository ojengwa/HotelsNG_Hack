var request = require('request');
var _ = require('underscore');
var jsonfy = require('jsonfy');
var set = []
var ip = require('ip-to-geolocation');

request('http://cms.hotels.ng/hackml/', function (error, response, body) {
  if (!error && response.statusCode == 200) {
    var obj = jsonfy(body);
    var data = getRoomWeight(obj);
    console.log(obj) // Show the HTML for the Google homepage.
  }
})

function getRoomWeight(data) {
  var count1 = count2 = count3 = count4 = 0
  data.forEach(function(entry) {
    var location = ip.queryIPv4(entry.ip_address);
    console.log(location);
    var cab =  entry["ip_address"] | 0;
    var cancelled =  entry["cancelled"] | 0;
    if (cab === 0 && cancelled === 0) {
      count1++;
    } else if (cab === 0 && cancelled === 1) {
      count2++;
    } else if (cab === 1 && cancelled === 0) {
      count3++;
    } else if(cab === 1 && cancelled === 1) {
      count4++;
    }
  });
  var weightedCabService = {
    "cab0can0": (count1/data.length) * 100,
    "cab0can1": (count2/data.length) * 100,
    "cab1can0": (count3/data.length) * 100,
    "cab1can1": (count4/data.length) * 100,
  };

  console.log("Cab Service Req: ", weightedCabService);
}