/*!
 * cleave.js - 1.6.0
 * https://github.com/nosir/cleave.js
 * Apache License Version 2.0
 *
 * Copyright (C) 2012-2020 Max Huang https://github.com/nosir/
 */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("react")):"function"==typeof define&&define.amd?define(["react"],t):"object"==typeof exports?exports.Cleave=t(require("react")):e.Cleave=t(e.React)}(this,function(e){return function(e){function t(r){if(n[r])return n[r].exports;var i=n[r]={exports:{},id:r,loaded:!1};return e[r].call(i.exports,i,i.exports,t),i.loaded=!0,i.exports}var n={};return t.m=e,t.c=n,t.p="",t(0)}([function(e,t,n){"use strict";function r(e,t){var n={};for(var r in e)t.indexOf(r)>=0||Object.prototype.hasOwnProperty.call(e,r)&&(n[r]=e[r]);return n}var i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o=n(1),a=n(2),s=n(9),c=n(10),l=n(11),u=n(12),p=n(13),d=n(14),m=n(15),f=a({componentDidMount:function(){this.init()},componentDidUpdate:function(e){var t=this,n=(t.props.options||{}).phoneRegionCode,r=t.props.value,i=t.properties;t.updateRegisteredEvents(t.props),e.value!==r&&void 0!==r&&null!==r&&(r=r.toString(),r!==t.properties.result&&(t.properties.initValue=r,t.onInput(r,!0)));var o=(e.options||{}).phoneRegionCode;o!==n&&n&&n!==t.properties.phoneRegionCode&&(t.properties.phoneRegionCode=n,t.initPhoneFormatter(),t.onInput(t.properties.result)),d.setSelection(t.element,t.state.cursorPosition,i.document)},updateRegisteredEvents:function(e){var t=this,n=t.registeredEvents,r=n.onKeyDown,i=n.onChange,o=n.onFocus,a=n.onBlur,s=n.onInit;e.onInit&&e.onInit!==s&&(t.registeredEvents.onInit=e.onInit),e.onChange&&e.onChange!==i&&(t.registeredEvents.onChange=e.onChange),e.onFocus&&e.onFocus!==o&&(t.registeredEvents.onFocus=e.onFocus),e.onBlur&&e.onBlur!==a&&(t.registeredEvents.onBlur=e.onBlur),e.onKeyDown&&e.onKeyDown!==r&&(t.registeredEvents.onKeyDown=e.onKeyDown)},getInitialState:function(){var e=this,t=e.props,n=t.value,r=t.options,i=t.onKeyDown,o=t.onChange,a=t.onFocus,s=t.onBlur,c=t.onInit;return e.registeredEvents={onInit:c||d.noop,onChange:o||d.noop,onFocus:a||d.noop,onBlur:s||d.noop,onKeyDown:i||d.noop},r||(r={}),r.initValue=n,e.properties=m.assign({},r),{value:e.properties.result,cursorPosition:0}},init:function(){var e=this,t=e.properties;return t.numeral||t.phone||t.creditCard||t.time||t.date||0!==t.blocksLength||t.prefix?(t.maxLength=d.getMaxLength(t.blocks),e.isAndroid=d.isAndroid(),e.initPhoneFormatter(),e.initDateFormatter(),e.initTimeFormatter(),e.initNumeralFormatter(),(t.initValue||t.prefix&&!t.noImmediatePrefix)&&e.onInput(t.initValue),void e.registeredEvents.onInit(e)):(e.onInput(t.initValue),void e.registeredEvents.onInit(e))},initNumeralFormatter:function(){var e=this,t=e.properties;t.numeral&&(t.numeralFormatter=new s(t.numeralDecimalMark,t.numeralIntegerScale,t.numeralDecimalScale,t.numeralThousandsGroupStyle,t.numeralPositiveOnly,t.stripLeadingZeroes,t.prefix,t.signBeforePrefix,t.tailPrefix,t.delimiter))},initTimeFormatter:function(){var e=this,t=e.properties;t.time&&(t.timeFormatter=new l(t.timePattern,t.timeFormat),t.blocks=t.timeFormatter.getBlocks(),t.blocksLength=t.blocks.length,t.maxLength=d.getMaxLength(t.blocks))},initDateFormatter:function(){var e=this,t=e.properties;t.date&&(t.dateFormatter=new c(t.datePattern,t.dateMin,t.dateMax),t.blocks=t.dateFormatter.getBlocks(),t.blocksLength=t.blocks.length,t.maxLength=d.getMaxLength(t.blocks))},initPhoneFormatter:function(){var e=this,t=e.properties;if(t.phone)try{t.phoneFormatter=new u(new t.root.Cleave.AsYouTypeFormatter(t.phoneRegionCode),t.delimiter)}catch(n){throw new Error("Please include phone-type-formatter.{country}.js lib")}},setRawValue:function(e){var t=this,n=t.properties;e=void 0!==e&&null!==e?e.toString():"",n.numeral&&(e=e.replace(".",n.numeralDecimalMark)),n.postDelimiterBackspace=!1,t.onChange({target:{value:e},stopPropagation:d.noop,preventDefault:d.noop,persist:d.noop})},getRawValue:function(){var e=this,t=e.properties,n=t.result;return t.rawValueTrimPrefix&&(n=d.getPrefixStrippedValue(n,t.prefix,t.prefixLength,t.result,t.delimiter,t.delimiters,t.noImmediatePrefix,t.tailPrefix,t.signBeforePrefix)),n=t.numeral?t.numeralFormatter?t.numeralFormatter.getRawValue(n):"":d.stripDelimiters(n,t.delimiter,t.delimiters)},getISOFormatDate:function(){var e=this,t=e.properties;return t.date?t.dateFormatter.getISOFormatDate():""},getISOFormatTime:function(){var e=this,t=e.properties;return t.time?t.timeFormatter.getISOFormatTime():""},onInit:function(e){return e},onKeyDown:function(e){var t=this,n=t.properties,r=e.which||e.keyCode;t.lastInputValue=n.result,t.isBackward=8===r,t.registeredEvents.onKeyDown(e)},onFocus:function(e){var t=this,n=t.properties;n.prefix&&n.noImmediatePrefix&&!e.target.value&&t.onInput(n.prefix),e.target.rawValue=t.getRawValue(),e.target.value=n.result,t.registeredEvents.onFocus(e),d.fixPrefixCursor(t.element,n.prefix,n.delimiter,n.delimiters)},onBlur:function(e){var t=this,n=t.properties;e.target.rawValue=t.getRawValue(),e.target.value=n.result,t.registeredEvents.onBlur(e)},onChange:function(e){var t=this,n=t.properties;t.isBackward=t.isBackward||"deleteContentBackward"===e.inputType;var r=d.getPostDelimiter(t.lastInputValue,n.delimiter,n.delimiters);t.isBackward&&r?n.postDelimiterBackspace=r:n.postDelimiterBackspace=!1,t.onInput(e.target.value),e.target.rawValue=t.getRawValue(),e.target.value=n.result,t.registeredEvents.onChange(e)},onInput:function(e,t){var n=this,r=n.properties,i=d.getPostDelimiter(e,r.delimiter,r.delimiters);return t||r.numeral||!r.postDelimiterBackspace||i||(e=d.headStr(e,e.length-r.postDelimiterBackspace.length)),r.phone?(!r.prefix||r.noImmediatePrefix&&!e.length?r.result=r.phoneFormatter.format(e):r.result=r.prefix+r.phoneFormatter.format(e).slice(r.prefix.length),void n.updateValueState()):r.numeral?(r.prefix&&r.noImmediatePrefix&&0===e.length?r.result="":r.result=r.numeralFormatter.format(e),void n.updateValueState()):(r.date&&(e=r.dateFormatter.getValidatedDate(e)),r.time&&(e=r.timeFormatter.getValidatedTime(e)),e=d.stripDelimiters(e,r.delimiter,r.delimiters),e=d.getPrefixStrippedValue(e,r.prefix,r.prefixLength,r.result,r.delimiter,r.delimiters,r.noImmediatePrefix,r.tailPrefix,r.signBeforePrefix),e=r.numericOnly?d.strip(e,/[^\d]/g):e,e=r.uppercase?e.toUpperCase():e,e=r.lowercase?e.toLowerCase():e,r.prefix&&(r.tailPrefix?e+=r.prefix:e=r.prefix+e,0===r.blocksLength)?(r.result=e,void n.updateValueState()):(r.creditCard&&n.updateCreditCardPropsByValue(e),e=r.maxLength>0?d.headStr(e,r.maxLength):e,r.result=d.getFormattedValue(e,r.blocks,r.blocksLength,r.delimiter,r.delimiters,r.delimiterLazyShow),void n.updateValueState()))},updateCreditCardPropsByValue:function(e){var t,n=this,r=n.properties;d.headStr(r.result,4)!==d.headStr(e,4)&&(t=p.getInfo(e,r.creditCardStrictMode),r.blocks=t.blocks,r.blocksLength=r.blocks.length,r.maxLength=d.getMaxLength(r.blocks),r.creditCardType!==t.type&&(r.creditCardType=t.type,r.onCreditCardTypeChanged.call(n,r.creditCardType)))},updateValueState:function(){var e=this,t=e.properties;if(!e.element)return void e.setState({value:t.result});var n=e.element.selectionEnd,r=e.element.value,i=t.result;return e.lastInputValue=i,n=d.getNextCursorPosition(n,r,i,t.delimiter,t.delimiters),e.isAndroid?void window.setTimeout(function(){e.setState({value:i,cursorPosition:n})},1):void e.setState({value:i,cursorPosition:n})},render:function(){var e=this,t=e.props,n=(t.value,t.options,t.onKeyDown,t.onFocus,t.onBlur,t.onChange,t.onInit,t.htmlRef),a=r(t,["value","options","onKeyDown","onFocus","onBlur","onChange","onInit","htmlRef"]);return o.createElement("input",i({type:"text",ref:function(t){e.element=t,n&&n.apply(this,arguments)},value:e.state.value,onKeyDown:e.onKeyDown,onChange:e.onChange,onFocus:e.onFocus,onBlur:e.onBlur},a))}});e.exports=f},function(t,n){t.exports=e},function(e,t,n){"use strict";var r=n(1),i=n(3);if("undefined"==typeof r)throw Error("create-react-class could not find the React object. If you are using script tags, make sure that React is being loaded before create-react-class.");var o=(new r.Component).updater;e.exports=i(r.Component,r.isValidElement,o)},function(e,t,n){"use strict";function r(e){return e}function i(e,t,n){function i(e,t,n){for(var r in t)t.hasOwnProperty(r)&&"production"!==process.env.NODE_ENV&&c("function"==typeof t[r],"%s: %s type `%s` is invalid; it must be a function, usually from React.PropTypes.",e.displayName||"ReactClass",l[n],r)}function p(e,t){var n=D.hasOwnProperty(t)?D[t]:null;F.hasOwnProperty(t)&&s("OVERRIDE_BASE"===n,"ReactClassInterface: You are attempting to override `%s` from your class specification. Ensure that your method names do not overlap with React methods.",t),e&&s("DEFINE_MANY"===n||"DEFINE_MANY_MERGED"===n,"ReactClassInterface: You are attempting to define `%s` on your component more than once. This conflict may be due to a mixin.",t)}function d(e,n){if(n){s("function"!=typeof n,"ReactClass: You're attempting to use a component class or function as a mixin. Instead, just use a regular object."),s(!t(n),"ReactClass: You're attempting to use a component as a mixin. Instead, just use a regular object.");var r=e.prototype,i=r.__reactAutoBindPairs;n.hasOwnProperty(u)&&I.mixins(e,n.mixins);for(var o in n)if(n.hasOwnProperty(o)&&o!==u){var a=n[o],l=r.hasOwnProperty(o);if(p(l,o),I.hasOwnProperty(o))I[o](e,a);else{var d=D.hasOwnProperty(o),m="function"==typeof a,f=m&&!d&&!l&&n.autobind!==!1;if(f)i.push(o,a),r[o]=a;else if(l){var v=D[o];s(d&&("DEFINE_MANY_MERGED"===v||"DEFINE_MANY"===v),"ReactClass: Unexpected spec policy %s for key %s when mixing in component specs.",v,o),"DEFINE_MANY_MERGED"===v?r[o]=h(r[o],a):"DEFINE_MANY"===v&&(r[o]=g(r[o],a))}else r[o]=a,"production"!==process.env.NODE_ENV&&"function"==typeof a&&n.displayName&&(r[o].displayName=n.displayName+"_"+o)}}}else if("production"!==process.env.NODE_ENV){var y=typeof n,x="object"===y&&null!==n;"production"!==process.env.NODE_ENV&&c(x,"%s: You're attempting to include a mixin that is either null or not an object. Check the mixins included by the component, as well as any mixins they include themselves. Expected object but got %s.",e.displayName||"ReactClass",null===n?null:y)}}function m(e,t){if(t)for(var n in t){var r=t[n];if(t.hasOwnProperty(n)){var i=n in I;s(!i,'ReactClass: You are attempting to define a reserved property, `%s`, that shouldn\'t be on the "statics" key. Define it as an instance property instead; it will still be accessible on the constructor.',n);var o=n in e;if(o){var a=b.hasOwnProperty(n)?b[n]:null;return s("DEFINE_MANY_MERGED"===a,"ReactClass: You are attempting to define `%s` on your component more than once. This conflict may be due to a mixin.",n),void(e[n]=h(e[n],r))}e[n]=r}}}function f(e,t){s(e&&t&&"object"==typeof e&&"object"==typeof t,"mergeIntoWithNoDuplicateKeys(): Cannot merge non-objects.");for(var n in t)t.hasOwnProperty(n)&&(s(void 0===e[n],"mergeIntoWithNoDuplicateKeys(): Tried to merge two objects with the same key: `%s`. This conflict may be due to a mixin; in particular, this may be caused by two getInitialState() or getDefaultProps() methods returning objects with clashing keys.",n),e[n]=t[n]);return e}function h(e,t){return function(){var n=e.apply(this,arguments),r=t.apply(this,arguments);if(null==n)return r;if(null==r)return n;var i={};return f(i,n),f(i,r),i}}function g(e,t){return function(){e.apply(this,arguments),t.apply(this,arguments)}}function v(e,t){var n=t.bind(e);if("production"!==process.env.NODE_ENV){n.__reactBoundContext=e,n.__reactBoundMethod=t,n.__reactBoundArguments=null;var r=e.constructor.displayName,i=n.bind;n.bind=function(o){for(var a=arguments.length,s=Array(a>1?a-1:0),l=1;l<a;l++)s[l-1]=arguments[l];if(o!==e&&null!==o)"production"!==process.env.NODE_ENV&&c(!1,"bind(): React component methods may only be bound to the component instance. See %s",r);else if(!s.length)return"production"!==process.env.NODE_ENV&&c(!1,"bind(): You are binding a component method to the component. React does this for you automatically in a high-performance way, so you can safely remove this call. See %s",r),n;var u=i.apply(n,arguments);return u.__reactBoundContext=e,u.__reactBoundMethod=t,u.__reactBoundArguments=s,u}}return n}function y(e){for(var t=e.__reactAutoBindPairs,n=0;n<t.length;n+=2){var r=t[n],i=t[n+1];e[r]=v(e,i)}}function x(e){var t=r(function(e,r,i){"production"!==process.env.NODE_ENV&&c(this instanceof t,"Something is calling a React component directly. Use a factory or JSX instead. See: https://fb.me/react-legacyfactory"),this.__reactAutoBindPairs.length&&y(this),this.props=e,this.context=r,this.refs=a,this.updater=i||n,this.state=null;var o=this.getInitialState?this.getInitialState():null;"production"!==process.env.NODE_ENV&&void 0===o&&this.getInitialState._isMockFunction&&(o=null),s("object"==typeof o&&!Array.isArray(o),"%s.getInitialState(): must return an object or null",t.displayName||"ReactCompositeComponent"),this.state=o});t.prototype=new P,t.prototype.constructor=t,t.prototype.__reactAutoBindPairs=[],E.forEach(d.bind(null,t)),d(t,N),d(t,e),d(t,w),t.getDefaultProps&&(t.defaultProps=t.getDefaultProps()),"production"!==process.env.NODE_ENV&&(t.getDefaultProps&&(t.getDefaultProps.isReactClassApproved={}),t.prototype.getInitialState&&(t.prototype.getInitialState.isReactClassApproved={})),s(t.prototype.render,"createClass(...): Class specification must implement a `render` method."),"production"!==process.env.NODE_ENV&&(c(!t.prototype.componentShouldUpdate,"%s has a method called componentShouldUpdate(). Did you mean shouldComponentUpdate()? The name is phrased as a question because the function is expected to return a value.",e.displayName||"A component"),c(!t.prototype.componentWillRecieveProps,"%s has a method called componentWillRecieveProps(). Did you mean componentWillReceiveProps()?",e.displayName||"A component"),c(!t.prototype.UNSAFE_componentWillRecieveProps,"%s has a method called UNSAFE_componentWillRecieveProps(). Did you mean UNSAFE_componentWillReceiveProps()?",e.displayName||"A component"));for(var i in D)t.prototype[i]||(t.prototype[i]=null);return t}var E=[],D={mixins:"DEFINE_MANY",statics:"DEFINE_MANY",propTypes:"DEFINE_MANY",contextTypes:"DEFINE_MANY",childContextTypes:"DEFINE_MANY",getDefaultProps:"DEFINE_MANY_MERGED",getInitialState:"DEFINE_MANY_MERGED",getChildContext:"DEFINE_MANY_MERGED",render:"DEFINE_ONCE",componentWillMount:"DEFINE_MANY",componentDidMount:"DEFINE_MANY",componentWillReceiveProps:"DEFINE_MANY",shouldComponentUpdate:"DEFINE_ONCE",componentWillUpdate:"DEFINE_MANY",componentDidUpdate:"DEFINE_MANY",componentWillUnmount:"DEFINE_MANY",UNSAFE_componentWillMount:"DEFINE_MANY",UNSAFE_componentWillReceiveProps:"DEFINE_MANY",UNSAFE_componentWillUpdate:"DEFINE_MANY",updateComponent:"OVERRIDE_BASE"},b={getDerivedStateFromProps:"DEFINE_MANY_MERGED"},I={displayName:function(e,t){e.displayName=t},mixins:function(e,t){if(t)for(var n=0;n<t.length;n++)d(e,t[n])},childContextTypes:function(e,t){"production"!==process.env.NODE_ENV&&i(e,t,"childContext"),e.childContextTypes=o({},e.childContextTypes,t)},contextTypes:function(e,t){"production"!==process.env.NODE_ENV&&i(e,t,"context"),e.contextTypes=o({},e.contextTypes,t)},getDefaultProps:function(e,t){e.getDefaultProps?e.getDefaultProps=h(e.getDefaultProps,t):e.getDefaultProps=t},propTypes:function(e,t){"production"!==process.env.NODE_ENV&&i(e,t,"prop"),e.propTypes=o({},e.propTypes,t)},statics:function(e,t){m(e,t)},autobind:function(){}},N={componentDidMount:function(){this.__isMounted=!0}},w={componentWillUnmount:function(){this.__isMounted=!1}},F={replaceState:function(e,t){this.updater.enqueueReplaceState(this,e,t)},isMounted:function(){return"production"!==process.env.NODE_ENV&&(c(this.__didWarnIsMounted,"%s: isMounted is deprecated. Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks.",this.constructor&&this.constructor.displayName||this.name||"Component"),this.__didWarnIsMounted=!0),!!this.__isMounted}},P=function(){};return o(P.prototype,e.prototype,F),x}var o=n(4),a=n(5),s=n(6);if("production"!==process.env.NODE_ENV)var c=n(7);var l,u="mixins";l="production"!==process.env.NODE_ENV?{prop:"prop",context:"context",childContext:"child context"}:{},e.exports=i},function(e,t){"use strict";function n(e){if(null===e||void 0===e)throw new TypeError("Object.assign cannot be called with null or undefined");return Object(e)}function r(){try{if(!Object.assign)return!1;var e=new String("abc");if(e[5]="de","5"===Object.getOwnPropertyNames(e)[0])return!1;for(var t={},n=0;n<10;n++)t["_"+String.fromCharCode(n)]=n;var r=Object.getOwnPropertyNames(t).map(function(e){return t[e]});if("0123456789"!==r.join(""))return!1;var i={};return"abcdefghijklmnopqrst".split("").forEach(function(e){i[e]=e}),"abcdefghijklmnopqrst"===Object.keys(Object.assign({},i)).join("")}catch(o){return!1}}var i=Object.getOwnPropertySymbols,o=Object.prototype.hasOwnProperty,a=Object.prototype.propertyIsEnumerable;e.exports=r()?Object.assign:function(e,t){for(var r,s,c=n(e),l=1;l<arguments.length;l++){r=Object(arguments[l]);for(var u in r)o.call(r,u)&&(c[u]=r[u]);if(i){s=i(r);for(var p=0;p<s.length;p++)a.call(r,s[p])&&(c[s[p]]=r[s[p]])}}return c}},function(e,t){"use strict";var n={};"production"!==process.env.NODE_ENV&&Object.freeze(n),e.exports=n},function(e,t){"use strict";function n(e,t,n,i,o,a,s,c){if(r(t),!e){var l;if(void 0===t)l=new Error("Minified exception occurred; use the non-minified dev environment for the full error message and additional helpful warnings.");else{var u=[n,i,o,a,s,c],p=0;l=new Error(t.replace(/%s/g,function(){return u[p++]})),l.name="Invariant Violation"}throw l.framesToPop=1,l}}var r=function(e){};"production"!==process.env.NODE_ENV&&(r=function(e){if(void 0===e)throw new Error("invariant requires an error message argument")}),e.exports=n},function(e,t,n){"use strict";var r=n(8),i=r;if("production"!==process.env.NODE_ENV){var o=function(e){for(var t=arguments.length,n=Array(t>1?t-1:0),r=1;r<t;r++)n[r-1]=arguments[r];var i=0,o="Warning: "+e.replace(/%s/g,function(){return n[i++]});"undefined"!=typeof console&&console.error(o);try{throw new Error(o)}catch(a){}};i=function(e,t){if(void 0===t)throw new Error("`warning(condition, format, ...args)` requires a warning message argument");if(0!==t.indexOf("Failed Composite propType: ")&&!e){for(var n=arguments.length,r=Array(n>2?n-2:0),i=2;i<n;i++)r[i-2]=arguments[i];o.apply(void 0,[t].concat(r))}}}e.exports=i},function(e,t){"use strict";function n(e){return function(){return e}}var r=function(){};r.thatReturns=n,r.thatReturnsFalse=n(!1),r.thatReturnsTrue=n(!0),r.thatReturnsNull=n(null),r.thatReturnsThis=function(){return this},r.thatReturnsArgument=function(e){return e},e.exports=r},function(e,t){"use strict";var n=function r(e,t,n,i,o,a,s,c,l,u){var p=this;p.numeralDecimalMark=e||".",p.numeralIntegerScale=t>0?t:0,p.numeralDecimalScale=n>=0?n:2,p.numeralThousandsGroupStyle=i||r.groupStyle.thousand,p.numeralPositiveOnly=!!o,p.stripLeadingZeroes=a!==!1,p.prefix=s||""===s?s:"",p.signBeforePrefix=!!c,p.tailPrefix=!!l,p.delimiter=u||""===u?u:",",p.delimiterRE=u?new RegExp("\\"+u,"g"):""};n.groupStyle={thousand:"thousand",lakh:"lakh",wan:"wan",none:"none"},n.prototype={getRawValue:function(e){return e.replace(this.delimiterRE,"").replace(this.numeralDecimalMark,".")},format:function(e){var t,r,i,o,a=this,s="";switch(e=e.replace(/[A-Za-z]/g,"").replace(a.numeralDecimalMark,"M").replace(/[^\dM-]/g,"").replace(/^\-/,"N").replace(/\-/g,"").replace("N",a.numeralPositiveOnly?"":"-").replace("M",a.numeralDecimalMark),a.stripLeadingZeroes&&(e=e.replace(/^(-)?0+(?=\d)/,"$1")),r="-"===e.slice(0,1)?"-":"",i="undefined"!=typeof a.prefix?a.signBeforePrefix?r+a.prefix:a.prefix+r:r,o=e,e.indexOf(a.numeralDecimalMark)>=0&&(t=e.split(a.numeralDecimalMark),o=t[0],s=a.numeralDecimalMark+t[1].slice(0,a.numeralDecimalScale)),"-"===r&&(o=o.slice(1)),a.numeralIntegerScale>0&&(o=o.slice(0,a.numeralIntegerScale)),a.numeralThousandsGroupStyle){case n.groupStyle.lakh:o=o.replace(/(\d)(?=(\d\d)+\d$)/g,"$1"+a.delimiter);break;case n.groupStyle.wan:o=o.replace(/(\d)(?=(\d{4})+$)/g,"$1"+a.delimiter);break;case n.groupStyle.thousand:o=o.replace(/(\d)(?=(\d{3})+$)/g,"$1"+a.delimiter)}return a.tailPrefix?r+o.toString()+(a.numeralDecimalScale>0?s.toString():"")+a.prefix:i+o.toString()+(a.numeralDecimalScale>0?s.toString():"")}},e.exports=n},function(e,t){"use strict";var n=function(e,t,n){var r=this;r.date=[],r.blocks=[],r.datePattern=e,r.dateMin=t.split("-").reverse().map(function(e){return parseInt(e,10)}),2===r.dateMin.length&&r.dateMin.unshift(0),r.dateMax=n.split("-").reverse().map(function(e){return parseInt(e,10)}),2===r.dateMax.length&&r.dateMax.unshift(0),r.initBlocks()};n.prototype={initBlocks:function(){var e=this;e.datePattern.forEach(function(t){"Y"===t?e.blocks.push(4):e.blocks.push(2)})},getISOFormatDate:function(){var e=this,t=e.date;return t[2]?t[2]+"-"+e.addLeadingZero(t[1])+"-"+e.addLeadingZero(t[0]):""},getBlocks:function(){return this.blocks},getValidatedDate:function(e){var t=this,n="";return e=e.replace(/[^\d]/g,""),t.blocks.forEach(function(r,i){if(e.length>0){var o=e.slice(0,r),a=o.slice(0,1),s=e.slice(r);switch(t.datePattern[i]){case"d":"00"===o?o="01":parseInt(a,10)>3?o="0"+a:parseInt(o,10)>31&&(o="31");break;case"m":"00"===o?o="01":parseInt(a,10)>1?o="0"+a:parseInt(o,10)>12&&(o="12")}n+=o,e=s}}),this.getFixedDateString(n)},getFixedDateString:function(e){var t,n,r,i=this,o=i.datePattern,a=[],s=0,c=0,l=0,u=0,p=0,d=0,m=!1;4===e.length&&"y"!==o[0].toLowerCase()&&"y"!==o[1].toLowerCase()&&(u="d"===o[0]?0:2,p=2-u,t=parseInt(e.slice(u,u+2),10),n=parseInt(e.slice(p,p+2),10),a=this.getFixedDate(t,n,0)),8===e.length&&(o.forEach(function(e,t){switch(e){case"d":s=t;break;case"m":c=t;break;default:l=t}}),d=2*l,u=s<=l?2*s:2*s+2,p=c<=l?2*c:2*c+2,t=parseInt(e.slice(u,u+2),10),n=parseInt(e.slice(p,p+2),10),r=parseInt(e.slice(d,d+4),10),m=4===e.slice(d,d+4).length,a=this.getFixedDate(t,n,r)),4!==e.length||"y"!==o[0]&&"y"!==o[1]||(p="m"===o[0]?0:2,d=2-p,n=parseInt(e.slice(p,p+2),10),r=parseInt(e.slice(d,d+2),10),m=2===e.slice(d,d+2).length,a=[0,n,r]),6!==e.length||"Y"!==o[0]&&"Y"!==o[1]||(p="m"===o[0]?0:4,d=2-.5*p,n=parseInt(e.slice(p,p+2),10),r=parseInt(e.slice(d,d+4),10),m=4===e.slice(d,d+4).length,a=[0,n,r]),a=i.getRangeFixedDate(a),i.date=a;var f=0===a.length?e:o.reduce(function(e,t){switch(t){case"d":return e+(0===a[0]?"":i.addLeadingZero(a[0]));case"m":return e+(0===a[1]?"":i.addLeadingZero(a[1]));case"y":return e+(m?i.addLeadingZeroForYear(a[2],!1):"");case"Y":return e+(m?i.addLeadingZeroForYear(a[2],!0):"")}},"");return f},getRangeFixedDate:function(e){var t=this,n=t.datePattern,r=t.dateMin||[],i=t.dateMax||[];return!e.length||r.length<3&&i.length<3?e:n.find(function(e){return"y"===e.toLowerCase()})&&0===e[2]?e:i.length&&(i[2]<e[2]||i[2]===e[2]&&(i[1]<e[1]||i[1]===e[1]&&i[0]<e[0]))?i:r.length&&(r[2]>e[2]||r[2]===e[2]&&(r[1]>e[1]||r[1]===e[1]&&r[0]>e[0]))?r:e},getFixedDate:function(e,t,n){return e=Math.min(e,31),t=Math.min(t,12),n=parseInt(n||0,10),(t<7&&t%2===0||t>8&&t%2===1)&&(e=Math.min(e,2===t?this.isLeapYear(n)?29:28:30)),[e,t,n]},isLeapYear:function(e){return e%4===0&&e%100!==0||e%400===0},addLeadingZero:function(e){return(e<10?"0":"")+e},addLeadingZeroForYear:function(e,t){return t?(e<10?"000":e<100?"00":e<1e3?"0":"")+e:(e<10?"0":"")+e}},e.exports=n},function(e,t){"use strict";var n=function(e,t){var n=this;n.time=[],n.blocks=[],n.timePattern=e,n.timeFormat=t,n.initBlocks()};n.prototype={initBlocks:function(){var e=this;e.timePattern.forEach(function(){e.blocks.push(2)})},getISOFormatTime:function(){var e=this,t=e.time;return t[2]?e.addLeadingZero(t[0])+":"+e.addLeadingZero(t[1])+":"+e.addLeadingZero(t[2]):""},getBlocks:function(){return this.blocks},getTimeFormatOptions:function(){var e=this;return"12"===String(e.timeFormat)?{maxHourFirstDigit:1,maxHours:12,maxMinutesFirstDigit:5,maxMinutes:60}:{maxHourFirstDigit:2,maxHours:23,maxMinutesFirstDigit:5,maxMinutes:60}},getValidatedTime:function(e){var t=this,n="";e=e.replace(/[^\d]/g,"");var r=t.getTimeFormatOptions();return t.blocks.forEach(function(i,o){if(e.length>0){var a=e.slice(0,i),s=a.slice(0,1),c=e.slice(i);switch(t.timePattern[o]){case"h":parseInt(s,10)>r.maxHourFirstDigit?a="0"+s:parseInt(a,10)>r.maxHours&&(a=r.maxHours+"");break;case"m":case"s":parseInt(s,10)>r.maxMinutesFirstDigit?a="0"+s:parseInt(a,10)>r.maxMinutes&&(a=r.maxMinutes+"")}n+=a,e=c}}),this.getFixedTimeString(n)},getFixedTimeString:function(e){var t,n,r,i=this,o=i.timePattern,a=[],s=0,c=0,l=0,u=0,p=0,d=0;return 6===e.length&&(o.forEach(function(e,t){switch(e){case"s":s=2*t;break;case"m":c=2*t;break;case"h":l=2*t}}),d=l,p=c,u=s,t=parseInt(e.slice(u,u+2),10),n=parseInt(e.slice(p,p+2),10),r=parseInt(e.slice(d,d+2),10),a=this.getFixedTime(r,n,t)),4===e.length&&i.timePattern.indexOf("s")<0&&(o.forEach(function(e,t){switch(e){case"m":c=2*t;break;case"h":l=2*t}}),d=l,p=c,t=0,n=parseInt(e.slice(p,p+2),10),r=parseInt(e.slice(d,d+2),10),a=this.getFixedTime(r,n,t)),i.time=a,0===a.length?e:o.reduce(function(e,t){switch(t){case"s":return e+i.addLeadingZero(a[2]);case"m":return e+i.addLeadingZero(a[1]);case"h":return e+i.addLeadingZero(a[0])}},"")},getFixedTime:function(e,t,n){return n=Math.min(parseInt(n||0,10),60),t=Math.min(t,60),e=Math.min(e,60),[e,t,n]},addLeadingZero:function(e){return(e<10?"0":"")+e}},e.exports=n},function(e,t){"use strict";var n=function(e,t){var n=this;n.delimiter=t||""===t?t:" ",n.delimiterRE=t?new RegExp("\\"+t,"g"):"",n.formatter=e};n.prototype={setFormatter:function(e){this.formatter=e},format:function(e){var t=this;t.formatter.clear(),e=e.replace(/[^\d+]/g,""),e=e.replace(/^\+/,"B").replace(/\+/g,"").replace("B","+"),e=e.replace(t.delimiterRE,"");for(var n,r="",i=!1,o=0,a=e.length;o<a;o++)n=t.formatter.inputDigit(e.charAt(o)),/[\s()-]/g.test(n)?(r=n,i=!0):i||(r=n);return r=r.replace(/[()]/g,""),r=r.replace(/[\s-]/g,t.delimiter)}},e.exports=n},function(e,t){"use strict";var n={blocks:{uatp:[4,5,6],amex:[4,6,5],diners:[4,6,4],discover:[4,4,4,4],mastercard:[4,4,4,4],dankort:[4,4,4,4],instapayment:[4,4,4,4],jcb15:[4,6,5],jcb:[4,4,4,4],maestro:[4,4,4,4],visa:[4,4,4,4],mir:[4,4,4,4],unionPay:[4,4,4,4],general:[4,4,4,4]},re:{uatp:/^(?!1800)1\d{0,14}/,amex:/^3[47]\d{0,13}/,discover:/^(?:6011|65\d{0,2}|64[4-9]\d?)\d{0,12}/,diners:/^3(?:0([0-5]|9)|[689]\d?)\d{0,11}/,mastercard:/^(5[1-5]\d{0,2}|22[2-9]\d{0,1}|2[3-7]\d{0,2})\d{0,12}/,dankort:/^(5019|4175|4571)\d{0,12}/,instapayment:/^63[7-9]\d{0,13}/,jcb15:/^(?:2131|1800)\d{0,11}/,jcb:/^(?:35\d{0,2})\d{0,12}/,maestro:/^(?:5[0678]\d{0,2}|6304|67\d{0,2})\d{0,12}/,mir:/^220[0-4]\d{0,12}/,visa:/^4\d{0,15}/,unionPay:/^(62|81)\d{0,14}/},getStrictBlocks:function(e){var t=e.reduce(function(e,t){return e+t},0);return e.concat(19-t)},getInfo:function(e,t){var r=n.blocks,i=n.re;t=!!t;for(var o in i)if(i[o].test(e)){var a=r[o];return{type:o,blocks:t?this.getStrictBlocks(a):a}}return{type:"unknown",blocks:t?this.getStrictBlocks(r.general):r.general}}};e.exports=n},function(e,t){"use strict";var n={noop:function(){},strip:function(e,t){return e.replace(t,"")},getPostDelimiter:function(e,t,n){if(0===n.length)return e.slice(-t.length)===t?t:"";var r="";return n.forEach(function(t){e.slice(-t.length)===t&&(r=t)}),r},getDelimiterREByDelimiter:function(e){return new RegExp(e.replace(/([.?*+^$[\]\\(){}|-])/g,"\\$1"),"g")},getNextCursorPosition:function(e,t,n,r,i){return t.length===e?n.length:e+this.getPositionOffset(e,t,n,r,i)},getPositionOffset:function(e,t,n,r,i){var o,a,s;return o=this.stripDelimiters(t.slice(0,e),r,i),a=this.stripDelimiters(n.slice(0,e),r,i),s=o.length-a.length,0!==s?s/Math.abs(s):0},stripDelimiters:function(e,t,n){var r=this;if(0===n.length){var i=t?r.getDelimiterREByDelimiter(t):"";return e.replace(i,"")}return n.forEach(function(t){t.split("").forEach(function(t){e=e.replace(r.getDelimiterREByDelimiter(t),"")})}),e},headStr:function(e,t){return e.slice(0,t)},getMaxLength:function(e){return e.reduce(function(e,t){return e+t},0)},getPrefixStrippedValue:function(e,t,n,r,i,o,a,s,c){if(0===n)return e;if(e===t&&""!==e)return"";if(c&&"-"==e.slice(0,1)){var l="-"==r.slice(0,1)?r.slice(1):r;return"-"+this.getPrefixStrippedValue(e.slice(1),t,n,l,i,o,a,s,c)}if(r.slice(0,n)!==t&&!s)return a&&!r&&e?e:"";if(r.slice(-n)!==t&&s)return a&&!r&&e?e:"";var u=this.stripDelimiters(r,i,o);return e.slice(0,n)===t||s?e.slice(-n)!==t&&s?u.slice(0,-n-1):s?e.slice(0,-n):e.slice(n):u.slice(n)},getFirstDiffIndex:function(e,t){for(var n=0;e.charAt(n)===t.charAt(n);)if(""===e.charAt(n++))return-1;return n},getFormattedValue:function(e,t,n,r,i,o){var a="",s=i.length>0,c="";return 0===n?e:(t.forEach(function(t,l){if(e.length>0){var u=e.slice(0,t),p=e.slice(t);c=s?i[o?l-1:l]||c:r,o?(l>0&&(a+=c),a+=u):(a+=u,u.length===t&&l<n-1&&(a+=c)),e=p}}),a)},fixPrefixCursor:function(e,t,n,r){if(e){var i=e.value,o=n||r[0]||" ";if(e.setSelectionRange&&t&&!(t.length+o.length<=i.length)){var a=2*i.length;setTimeout(function(){e.setSelectionRange(a,a)},1)}}},checkFullSelection:function(e){try{var t=window.getSelection()||document.getSelection()||{};return t.toString().length===e.length}catch(n){}return!1},setSelection:function(e,t,n){if(e===this.getActiveElement(n)&&!(e&&e.value.length<=t))if(e.createTextRange){var r=e.createTextRange();r.move("character",t),r.select()}else try{e.setSelectionRange(t,t)}catch(i){console.warn("The input element type does not support selection")}},getActiveElement:function(e){var t=e.activeElement;return t&&t.shadowRoot?this.getActiveElement(t.shadowRoot):t},isAndroid:function(){return navigator&&/android/i.test(navigator.userAgent)},isAndroidBackspaceKeydown:function(e,t){return!!(this.isAndroid()&&e&&t)&&t===e.slice(0,-1)}};e.exports=n},function(e,t){"use strict";var n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},r={assign:function(e,t){return e=e||{},t=t||{},e.creditCard=!!t.creditCard,e.creditCardStrictMode=!!t.creditCardStrictMode,e.creditCardType="",e.onCreditCardTypeChanged=t.onCreditCardTypeChanged||function(){},e.phone=!!t.phone,e.phoneRegionCode=t.phoneRegionCode||"AU",e.phoneFormatter={},e.time=!!t.time,e.timePattern=t.timePattern||["h","m","s"],e.timeFormat=t.timeFormat||"24",e.timeFormatter={},e.date=!!t.date,e.datePattern=t.datePattern||["d","m","Y"],e.dateMin=t.dateMin||"",e.dateMax=t.dateMax||"",e.dateFormatter={},e.numeral=!!t.numeral,e.numeralIntegerScale=t.numeralIntegerScale>0?t.numeralIntegerScale:0,e.numeralDecimalScale=t.numeralDecimalScale>=0?t.numeralDecimalScale:2,e.numeralDecimalMark=t.numeralDecimalMark||".",e.numeralThousandsGroupStyle=t.numeralThousandsGroupStyle||"thousand",e.numeralPositiveOnly=!!t.numeralPositiveOnly,e.stripLeadingZeroes=t.stripLeadingZeroes!==!1,e.signBeforePrefix=!!t.signBeforePrefix,e.tailPrefix=!!t.tailPrefix,e.swapHiddenInput=!!t.swapHiddenInput,e.numericOnly=e.creditCard||e.date||!!t.numericOnly,e.uppercase=!!t.uppercase,e.lowercase=!!t.lowercase,e.prefix=e.creditCard||e.date?"":t.prefix||"",e.noImmediatePrefix=!!t.noImmediatePrefix,e.prefixLength=e.prefix.length,e.rawValueTrimPrefix=!!t.rawValueTrimPrefix,e.copyDelimiter=!!t.copyDelimiter,e.initValue=void 0!==t.initValue&&null!==t.initValue?t.initValue.toString():"",e.delimiter=t.delimiter||""===t.delimiter?t.delimiter:t.date?"/":t.time?":":t.numeral?",":(t.phone," "),e.delimiterLength=e.delimiter.length,e.delimiterLazyShow=!!t.delimiterLazyShow,e.delimiters=t.delimiters||[],e.blocks=t.blocks||[],e.blocksLength=e.blocks.length,e.root="object"===("undefined"==typeof global?"undefined":n(global))&&global?global:window,e.document=t.document||e.root.document,e.maxLength=0,e.backspace=!1,e.result="",e.onValueChanged=t.onValueChanged||function(){},e}};e.exports=r}])});