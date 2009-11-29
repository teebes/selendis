// http://snook.ca/archives/javascript/testing_for_a_v
function oc(a) {
  var o = {};
  for(var i=0;i<a.length;i++) { o[a[i]]=''; }
  return o;
}


// http://www.thirstymind.org/2009/10/17/implementing-pythons-string-format-in-javascript/
function str_format(){
 
    var formatted_str = arguments[0] || '';
 
    for(var i=1; i<arguments.length; i++){
        var re = new RegExp("\\{"+(i-1)+"}", "gim");
        formatted_str = formatted_str.replace(re, arguments[i]);
    }
    
    return formatted_str;
}