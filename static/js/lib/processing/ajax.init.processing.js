// Initializing a Processing.js Script with AJAX
// Adapted by -> ( F1LT3R @ hyper-metrix.com )
// USAGE: initProcessing("myScript.pjs", "myCanvasId");
// AJAX CREDITS: http://bulletproofajax.com/ - I took the basic AjAX script from BulletProof AJAX. Awesome book, get it!
// Processing CREDITS: http://ejohn.org/blog/processingjs/ - John Resig's Blog

function getHTTPObject() {
  var xhr = false;
  if (window.XMLHttpRequest) {
    xhr = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    try {
      xhr = new ActiveXObject("Msxml2.XMLHTTP");
    } catch(e) {
      try {
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
      } catch(e) {
        xhr = false;
      }
    }
  }
  return xhr;
}

function initProcessing(file, canvas) {
  var request = getHTTPObject();
  if (request) {
    request.onreadystatechange = function() {
      parseResponse(request, canvas);
    };
    request.open("GET", file, true);
    request.send(null);
  }
}

function parseResponse(request, canvas) {
  if (request.readyState == 4) {
    if (request.status == 200 || request.status == 304) {
      var targetCanvas = document.getElementById(canvas);
      Processing(targetCanvas, request.responseText);
    }
  }
}
