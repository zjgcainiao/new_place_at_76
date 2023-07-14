/**!
 * lg-zoom.js | 1.3.0 | October 14th 2020
 * http://sachinchoolur.github.io/lg-zoom.js
 * Copyright (c) 2016 Sachin N; 
 * @license GPLv3 
 */
!function(e){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{var t;t="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,t.LgZoom=e()}}(function(){var e,t,o;return function(){function e(t,o,r){function i(l,s){if(!o[l]){if(!t[l]){var n="function"==typeof require&&require;if(!s&&n)return n(l,!0);if(a)return a(l,!0);var u=new Error("Cannot find module '"+l+"'");throw u.code="MODULE_NOT_FOUND",u}var c=o[l]={exports:{}};t[l][0].call(c.exports,function(e){return i(t[l][1][e]||e)},c,c.exports,e,t,o,r)}return o[l].exports}for(var a="function"==typeof require&&require,l=0;l<r.length;l++)i(r[l]);return i}return e}()({1:[function(t,o,r){!function(t,o){if("function"==typeof e&&e.amd)e([],o);else if(void 0!==r)o();else{var i={exports:{}};o(),t.lgZoom=i.exports}}(this,function(){"use strict";var e=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var o=arguments[t];for(var r in o)Object.prototype.hasOwnProperty.call(o,r)&&(e[r]=o[r])}return e},t=function e(){var t=!1,o=navigator.userAgent.match(/Chrom(e|ium)\/([0-9]+)\./);return o&&parseInt(o[2],10)<54&&(t=!0),t},o={scale:1,zoom:!0,actualSize:!0,enableZoomAfter:300,useLeftForZoom:t()},r=function t(r){return this.el=r,this.core=window.lgData[this.el.getAttribute("lg-uid")],this.core.s=e({},o,this.core.s),this.core.s.zoom&&this.core.doCss()&&(this.init(),this.zoomabletimeout=!1,this.pageX=window.innerWidth/2,this.pageY=window.innerHeight/2+(document.documentElement.scrollTop||document.body.scrollTop)),this};r.prototype.init=function(){var e=this,t='<button type="button" aria-label="Zoom in" id="lg-zoom-in" class="lg-icon"></button><button type="button" aria-label="Zoom out" id="lg-zoom-out" class="lg-icon"></button>';e.core.s.actualSize&&(t+='<button type="button" aria-label="Actual size" id="lg-actual-size" class="lg-icon"></button>'),e.core.s.useLeftForZoom?utils.addClass(e.core.outer,"lg-use-left-for-zoom"):utils.addClass(e.core.outer,"lg-use-transition-for-zoom"),this.core.outer.querySelector(".lg-toolbar").insertAdjacentHTML("beforeend",t),utils.on(e.core.el,"onSlideItemLoad.lgtmzoom",function(t){var o=e.core.s.enableZoomAfter+t.detail.delay;utils.hasClass(document.body,"lg-from-hash")&&t.detail.delay?o=0:utils.removeClass(document.body,"lg-from-hash"),e.zoomabletimeout=setTimeout(function(){utils.addClass(e.core.___slide[t.detail.index],"lg-zoomable")},o+30)});var o=1,r=function t(o){var r=e.core.outer.querySelector(".lg-current .lg-image"),i,a,l=(window.innerWidth-r.clientWidth)/2,s=(window.innerHeight-r.clientHeight)/2+(document.documentElement.scrollTop||document.body.scrollTop);i=e.pageX-l,a=e.pageY-s;var n=(o-1)*i,u=(o-1)*a;utils.setVendor(r,"Transform","scale3d("+o+", "+o+", 1)"),r.setAttribute("data-scale",o),e.core.s.useLeftForZoom?(r.parentElement.style.left=-n+"px",r.parentElement.style.top=-u+"px"):utils.setVendor(r.parentElement,"Transform","translate3d(-"+n+"px, -"+u+"px, 0)"),r.parentElement.setAttribute("data-x",n),r.parentElement.setAttribute("data-y",u)},i=function t(){o>1?utils.addClass(e.core.outer,"lg-zoomed"):e.resetZoom(),o<1&&(o=1),r(o)},a=function t(r,a,l,s){var n=a.clientWidth,u;u=e.core.s.dynamic?e.core.s.dynamicEl[l].width||a.naturalWidth||n:e.core.items[l].getAttribute("data-width")||a.naturalWidth||n;var c;utils.hasClass(e.core.outer,"lg-zoomed")?o=1:u>n&&(c=u/n,o=c||2),s?(e.pageX=window.innerWidth/2,e.pageY=window.innerHeight/2+(document.documentElement.scrollTop||document.body.scrollTop)):(e.pageX=r.pageX||r.targetTouches[0].pageX,e.pageY=r.pageY||r.targetTouches[0].pageY),i(),setTimeout(function(){utils.removeClass(e.core.outer,"lg-grabbing"),utils.addClass(e.core.outer,"lg-grab")},10)},l=!1;utils.on(e.core.el,"onAferAppendSlide.lgtmzoom",function(t){var o=t.detail.index,r=e.core.___slide[o].querySelector(".lg-image");e.core.isTouch||utils.on(r,"dblclick",function(e){a(e,r,o)}),e.core.isTouch&&utils.on(r,"touchstart",function(e){l?(clearTimeout(l),l=null,a(e,r,o)):l=setTimeout(function(){l=null},300),e.preventDefault()})}),utils.on(window,"resize.lgzoom scroll.lgzoom orientationchange.lgzoom",function(){e.pageX=window.innerWidth/2,e.pageY=window.innerHeight/2+(document.documentElement.scrollTop||document.body.scrollTop),r(o)}),utils.on(document.getElementById("lg-zoom-out"),"click.lg",function(){e.core.outer.querySelector(".lg-current .lg-image")&&(o-=e.core.s.scale,i())}),utils.on(document.getElementById("lg-zoom-in"),"click.lg",function(){e.core.outer.querySelector(".lg-current .lg-image")&&(o+=e.core.s.scale,i())}),utils.on(document.getElementById("lg-actual-size"),"click.lg",function(t){a(t,e.core.___slide[e.core.index].querySelector(".lg-image"),e.core.index,!0)}),utils.on(e.core.el,"onBeforeSlide.lgtm",function(){o=1,e.resetZoom()}),e.core.isTouch||e.zoomDrag(),e.core.isTouch&&e.zoomSwipe()},r.prototype.getModifier=function(e,t,o){var r=e;e=Math.abs(e);var i=this.getCurrentTransform(o);if(!i)return 1;var a=1;if("X"===t){var l=Math.sign(parseFloat(i[0]));0===e||180===e?a=1:90===e&&(a=-90===r&&1===l||90===r&&-1===l?-1:1),a*=l}else{var s=Math.sign(parseFloat(i[3]));if(0===e||180===e)a=1;else if(90===e){var n=parseFloat(i[1]),u=parseFloat(i[2]);a=Math.sign(n*u*r*s)}a*=s}return a},r.prototype.getImageSize=function(e,t,o){var r={y:"offsetHeight",x:"offsetWidth"};return 90===t&&(o="x"===o?"y":"x"),e[r[o]]},r.prototype.getDragCords=function(e,t){return 90===t?{x:e.pageY,y:e.pageX}:{x:e.pageX,y:e.pageY}},r.prototype.getSwipeCords=function(e,t){var o=e.targetTouches[0].pageX,r=e.targetTouches[0].pageY;return 90===t?{x:r,y:o}:{x:o,y:r}},r.prototype.getPossibleDragCords=function(e,t){var o=(this.core.outer.querySelector(".lg").clientHeight-this.getImageSize(e,t,"y"))/2,r=Math.abs(this.getImageSize(e,t,"y")*Math.abs(e.getAttribute("data-scale"))-this.core.outer.querySelector(".lg").clientHeight+o),i=(this.core.outer.querySelector(".lg").clientWidth-this.getImageSize(e,t,"x"))/2,a=Math.abs(this.getImageSize(e,t,"x")*Math.abs(e.getAttribute("data-scale"))-this.core.outer.querySelector(".lg").clientWidth+i);return 90===t?{minY:i,maxY:a,minX:o,maxX:r}:{minY:o,maxY:r,minX:i,maxX:a}},r.prototype.getDragAllowedAxises=function(e,t){var o=this.getImageSize(e,t,"y")*e.getAttribute("data-scale")>this.core.outer.querySelector(".lg").clientHeight,r=this.getImageSize(e,t,"x")*e.getAttribute("data-scale")>this.core.outer.querySelector(".lg").clientWidth;return 90===t?{allowX:o,allowY:r}:{allowX:r,allowY:o}},r.prototype.getCurrentTransform=function(e){if(!e)return 0;var t=window.getComputedStyle(e,null),o=t.getPropertyValue("-webkit-transform")||t.getPropertyValue("-moz-transform")||t.getPropertyValue("-ms-transform")||t.getPropertyValue("-o-transform")||t.getPropertyValue("transform")||"none";return"none"!==o?o.split("(")[1].split(")")[0].split(","):0},r.prototype.getCurrentRotation=function(e){if(!e)return 0;var t=this.getCurrentTransform(e);return t?Math.round(Math.atan2(t[1],t[0])*(180/Math.PI)):0},r.prototype.resetZoom=function(){utils.removeClass(this.core.outer,"lg-zoomed");for(var e=0;e<this.core.___slide.length;e++)this.core.___slide[e].querySelector(".lg-img-wrap")&&(this.core.___slide[e].querySelector(".lg-img-wrap").removeAttribute("style"),this.core.___slide[e].querySelector(".lg-img-wrap").removeAttribute("data-x"),this.core.___slide[e].querySelector(".lg-img-wrap").removeAttribute("data-y"));for(var t=0;t<this.core.___slide.length;t++)this.core.___slide[t].querySelector(".lg-image")&&(this.core.___slide[t].querySelector(".lg-image").removeAttribute("style"),this.core.___slide[t].querySelector(".lg-image").removeAttribute("data-scale"));this.pageX=window.innerWidth/2,this.pageY=window.innerHeight/2+(document.documentElement.scrollTop||document.body.scrollTop)},r.prototype.zoomSwipe=function(){for(var e=this,t={},o={},r=!1,i=!1,a=!1,l=0,s,n=0;n<e.core.___slide.length;n++)utils.on(e.core.___slide[n],"touchstart.lg",function(o){if(utils.hasClass(e.core.outer,"lg-zoomed")){var r=e.core.___slide[e.core.index].querySelector(".lg-object");s=e.core.___slide[e.core.index].querySelector(".lg-img-rotate"),l=e.getCurrentRotation(s);var n=e.getDragAllowedAxises(r,Math.abs(l));a=n.allowY,i=n.allowX,(i||a)&&(o.preventDefault(),t=e.getSwipeCords(o,Math.abs(l)))}});for(var u=0;u<e.core.___slide.length;u++)utils.on(e.core.___slide[u],"touchmove.lg",function(n){if(utils.hasClass(e.core.outer,"lg-zoomed")){var u=e.core.___slide[e.core.index].querySelector(".lg-img-wrap"),c,g;n.preventDefault(),r=!0,o=e.getSwipeCords(n,Math.abs(l)),utils.addClass(e.core.outer,"lg-zoom-dragging"),g=a?-Math.abs(u.getAttribute("data-y"))+(o.y-t.y)*e.getModifier(l,"Y",s):-Math.abs(u.getAttribute("data-y")),c=i?-Math.abs(u.getAttribute("data-x"))+(o.x-t.x)*e.getModifier(l,"X",s):-Math.abs(u.getAttribute("data-x")),(Math.abs(o.x-t.x)>15||Math.abs(o.y-t.y)>15)&&(e.core.s.useLeftForZoom?(u.style.left=c+"px",u.style.top=g+"px"):utils.setVendor(u,"Transform","translate3d("+c+"px, "+g+"px, 0)"))}});for(var c=0;c<e.core.___slide.length;c++)utils.on(e.core.___slide[c],"touchend.lg",function(){utils.hasClass(e.core.outer,"lg-zoomed")&&r&&(r=!1,utils.removeClass(e.core.outer,"lg-zoom-dragging"),e.touchendZoom(t,o,i,a,l))})},r.prototype.zoomDrag=function(){for(var e=this,t={},o={},r=!1,i=!1,a=!1,l=!1,s=0,n,u=0;u<e.core.___slide.length;u++)utils.on(e.core.___slide[u],"mousedown.lgzoom",function(o){var i=e.core.___slide[e.core.index].querySelector(".lg-object");n=e.core.___slide[e.core.index].querySelector(".lg-img-rotate"),s=e.getCurrentRotation(n);var u=e.getDragAllowedAxises(i,Math.abs(s));l=u.allowY,a=u.allowX,utils.hasClass(e.core.outer,"lg-zoomed")&&utils.hasClass(o.target,"lg-object")&&(a||l)&&(o.preventDefault(),t=e.getDragCords(o,Math.abs(s)),r=!0,e.core.outer.scrollLeft+=1,e.core.outer.scrollLeft-=1,utils.removeClass(e.core.outer,"lg-grab"),utils.addClass(e.core.outer,"lg-grabbing"))});utils.on(window,"mousemove.lgzoom",function(u){if(r){var c=e.core.___slide[e.core.index].querySelector(".lg-img-wrap"),g,d;i=!0,o=e.getDragCords(u,Math.abs(s)),utils.addClass(e.core.outer,"lg-zoom-dragging"),d=l?-Math.abs(c.getAttribute("data-y"))+(o.y-t.y)*e.getModifier(s,"Y",n):-Math.abs(c.getAttribute("data-y")),g=a?-Math.abs(c.getAttribute("data-x"))+(o.x-t.x)*e.getModifier(s,"X",n):-Math.abs(c.getAttribute("data-x")),e.core.s.useLeftForZoom?(c.style.left=g+"px",c.style.top=d+"px"):utils.setVendor(c,"Transform","translate3d("+g+"px, "+d+"px, 0)")}}),utils.on(window,"mouseup.lgzoom",function(n){r&&(r=!1,utils.removeClass(e.core.outer,"lg-zoom-dragging"),!i||t.x===o.x&&t.y===o.y||(o=e.getDragCords(n,Math.abs(s)),e.touchendZoom(t,o,a,l,s)),i=!1),utils.removeClass(e.core.outer,"lg-grabbing"),utils.addClass(e.core.outer,"lg-grab")})},r.prototype.touchendZoom=function(e,t,o,r,i){var a=this,l=a.core.___slide[a.core.index].querySelector(".lg-img-wrap"),s=a.core.___slide[a.core.index].querySelector(".lg-object"),n=a.core.___slide[a.core.index].querySelector(".lg-img-rotate"),u=-Math.abs(l.getAttribute("data-x"))+(t.x-e.x)*a.getModifier(i,"X",n),c=-Math.abs(l.getAttribute("data-y"))+(t.y-e.y)*a.getModifier(i,"Y",n),g=a.getPossibleDragCords(s,Math.abs(i));(Math.abs(t.x-e.x)>15||Math.abs(t.y-e.y)>15)&&(r&&(c<=-g.maxY?c=-g.maxY:c>=-g.minY&&(c=-g.minY)),o&&(u<=-g.maxX?u=-g.maxX:u>=-g.minX&&(u=-g.minX)),r?l.setAttribute("data-y",Math.abs(c)):c=-Math.abs(l.getAttribute("data-y")),o?l.setAttribute("data-x",Math.abs(u)):u=-Math.abs(l.getAttribute("data-x")),a.core.s.useLeftForZoom?(l.style.left=u+"px",l.style.top=c+"px"):utils.setVendor(l,"Transform","translate3d("+u+"px, "+c+"px, 0)"))},r.prototype.destroy=function(){var e=this;utils.off(e.core.el,".lgzoom"),utils.off(window,".lgzoom");for(var t=0;t<e.core.___slide.length;t++)utils.off(e.core.___slide[t],".lgzoom");utils.off(e.core.el,".lgtmzoom"),e.resetZoom(),clearTimeout(e.zoomabletimeout),e.zoomabletimeout=!1},window.lgModules.zoom=r})},{}]},{},[1])(1)});