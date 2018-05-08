var map;


var mapStyle = [{
  'featureType': 'all',
  'elementType': 'all',
  'stylers': [{'visibility': 'off'}]
}, {
  'featureType': 'landscape',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'color': '#fcfcfc'}]
}, {
  'featureType': 'water',
  'elementType': 'labels',
  'stylers': [{'visibility': 'off'}]
}, {
  'featureType': 'water',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'hue': '#5f94ff'}, {'lightness': 60}]
}];

  function initMap() {
    // load the map
      map = new google.maps.Map(document.getElementById('map'), {
      center: {lat:-37.9, lng:  144.97},
      zoom:  11,
      styles: mapStyle
    });
    
     map.data.setStyle(styleFeature);
     map.data.addListener('mouseover', mouseInToRegion);
     map.data.addListener('mouseout', mouseOutOfRegion);
     map.data.addListener('click',clickMap)

    var selectBox = document.getElementById('Aurin-Variable');
    google.maps.event.addDomListener(selectBox,'change',function(){
        // clearSentimentData();
        loadAurinData(selectBox.options[selectBox.selectedIndex].value);  
    });

    

    loadMapShapes();
  }


/** Loads the state boundary polygons from a GeoJSON source. */
function loadMapShapes() {
    
    map.data.loadGeoJson('https://raw.githubusercontent.com/lotharJiang/Cluster-Sentiment-Analysis/master/Data%20Visualisation/newVicJson.json',{idPropertyName:'Suburb_Name'});
    
    google.maps.event.addListenerOnce(map.data,"addfeature",function(){
      google.maps.event.trigger(document.getElementById('Aurin-Variable'),'change');
    })
}

function mouseInToRegion(e) {
  
  var selectBox = document.getElementById('Aurin-Variable');
  data = selectBox.options[selectBox.selectedIndex].value.toString().split(" ")[1];
  
  // set the hover state so the setStyle function can change the border
  e.feature.setProperty('state', 'hover');
  //update the label
  showDetails(e);
  

  document.getElementById('data-label').textContent=e.feature.getProperty('Suburb_Name');

  document.getElementById('data-value').textContent=e.feature.getProperty('polarity');
}

function mouseOutOfRegion(e) {
  // reset the hover state, returning the border to normal
  e.feature.setProperty('state', 'normal');
}

function showDetails(e) {
  stateName = document.getElementById('stateName');
  incoming = document.getElementById('incoming');
  uni = document.getElementById('uni');

  stateName.innerHTML = "Suburb Name: "+e.feature.getProperty('Suburb_Name');
  // stateName.style.right = 1024 - window.event.clientX-200;
  // stateName.style.top = window.event.clientY-10;
  
  incoming.innerHTML = "Incoming: "+e.feature.getProperty('incoming');
  // polarity.style.right = 1024 - window.event.clientX-200;
  // polarity.style.top = window.event.clientY-10;

  uni.innerHTML = "Education Rate: "+e.feature.getProperty('uni');
  // data.style.right = 1024 - window.event.clientX-200;
  // data.style.top = window.event.clientY-10;
  
}

function clickMap(e){
  var data = {}
  data.Suburb_Name = e.feature.getProperty('Suburb_Name')
  data.incoming = e.feature.getProperty('incoming')
  data.uni = e.feature.getProperty('uni')
  

  $.get("/table",function(result){
    window.location.href = 'http://localhost:5000/table'+'/'+e.feature.getProperty('Suburb_Name')+'|'+e.feature.getProperty('incoming')+'|'+e.feature.getProperty('uni');
});
}

function clearSentimentData() {
  
  map.data.forEach(function(row) {
    row.setProperty('incoming', 0);
    row.setProperty('uni',0);
  });

}

function loadAurinData(variable){
  var url = variable.toString().split(" ")[0];
  var attribute = variable.toString().split(" ")[1]; 
  var attribute_value = variable.toString().split(" ")[2];

  if(attribute=='polarity'){
    map.data.forEach(function(row){
        row.setProperty('polarity',0);
    });
    $.get(url,function(result){
      result['data']['rows'].forEach(function(row){
      try{ 
        state = row['key'];
        data = row['value'];
        map.data.getFeatureById(state).setProperty('polarity',data);
        console.log(map.data.getFeatureById(state).getProperty('polarity'));
      }catch(err){
        console.log('not find')
      }
      });
    
    });
  }else{
    $.get(url, function(result){
  
      var aurinData = JSON.parse(result);
        aurinData['features'].forEach(function(row){
        try{ 
          state = row['properties']['SSC_NAME'];
          data = row['properties'][attribute_value];
          map.data.getFeatureById(state).setProperty(attribute, data);
        }catch(err){
          console.log("not Find");
        }
        })
      
    });
  }
}

function styleFeature(feature) {
  lightness_uni = 100 - feature.getProperty('uni')*100
  lightness_incoming = 100 - feature.getProperty('incoming')/1000 
  lightness_polarity = 100 - feature.getProperty('polarity')*100
  var outlineWeight = 0.5, zIndex = 1;
  var color;
  var hue;

  if (feature.getProperty('state') === 'hover') {
    outlineWeight = zIndex = 2;
  }

  index = document.getElementById('Aurin-Variable').selectedIndex;
  if (index == 0){
    hue = 215;
    lightness = lightness_incoming;
  }
  else if(index == 1){
    hue = 0;
    lightness = lightness_uni;
  }else if(index == 2){
    hue = 120;
    if(lightness_polarity==undefined){
      lightness == 0;
    }else{
      lightness = lightness_polarity;
    }
  }

  return {
    strokeWeight: outlineWeight,
    zIndex: zIndex,
    fillColor: 'hsl('+hue+', 60%,' + lightness + '%)',
    fillOpacity: 0.75,
    visible: true
  };
}

function refreshData() {
  alert("connect with button");
  var httpRequest;
  document.getElementById("buttonRefresh").addEventListener('click', makeRequest);

  function makeRequest() {
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alertContents;
    alert("Readyto GET");
    httpRequest.open('GET', 'http://localhost:8080/index.html');
    httpRequest.send();
  }

  function alertContents() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        alert(httpRequest.responseText);
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
}

