// Get the users browser

var cur = "";

// From Stack overflow. http://stackoverflow.com/questions/9847580/how-to-detect-safari-chrome-ie-firefox-and-opera-browser
// Modified for CactusDev use

// Opera 8.0+
var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';
// At least Safari 3+: "[object HTMLElementConstructor]"
var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
// Internet Explorer 6-11
var isIE = /*@cc_on!@*/ false || !!document.documentMode;
// Edge 20+
var isEdge = !isIE && !!window.StyleMedia;
// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;

// Time for some ifs so we can do the thing.

if (isOpera) {
  cur = "Opera";
  console.log("GLHF.")
} else if (isFirefox) {
  cur = "Firefox"
  console.log("GLHF.");

} else if (isSafari) {
  cur = "Safari"
  console.log("GLHF.");

} else if (isIE) {
  cur = "Internet Explorer"
  console.log("GLHF.");

} else if (isEdge) {
  cur = "Edge"
  console.log("GLHF.");

} else if (isChrome) {
  cur = "Chrome"
}

console.log("You appear to be using " + cur);
