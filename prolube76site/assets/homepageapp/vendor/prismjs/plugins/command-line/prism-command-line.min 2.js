!function(){if("undefined"!=typeof Prism&&"undefined"!=typeof document){var d=/(?:^|\s)command-line(?:\s|$)/,f="command-line-prompt",m="".startsWith?function(e,t){return e.startsWith(t)}:function(e,t){return 0===e.indexOf(t)};Prism.hooks.add("before-highlight",function(e){var t=h(e);if(!t.complete&&e.code){var n=e.element.parentElement;if(n&&/pre/i.test(n.nodeName)&&(d.test(n.className)||d.test(e.element.className))){var a=e.element.querySelector("."+f);a&&a.remove();var s=e.code.split("\n");t.numberOfLines=s.length;var o=t.outputLines=[],r=n.getAttribute("data-output"),i=n.getAttribute("data-filter-output");if(null!==r)r.split(",").forEach(function(e){var t=e.split("-"),n=parseInt(t[0],10),a=2===t.length?parseInt(t[1],10):n;if(!isNaN(n)&&!isNaN(a)){n<1&&(n=1),a>s.length&&(a=s.length),a--;for(var r=--n;r<=a;r++)o[r]=s[r],s[r]=""}});else if(i)for(var l=0;l<s.length;l++)m(s[l],i)&&(o[l]=s[l].slice(i.length),s[l]="");e.code=s.join("\n")}else t.complete=!0}else t.complete=!0}),Prism.hooks.add("before-insert",function(e){var t=h(e);if(!t.complete){for(var n=e.highlightedCode.split("\n"),a=t.outputLines||[],r=0,s=a.length;r<s;r++)a.hasOwnProperty(r)&&(n[r]=a[r]);e.highlightedCode=n.join("\n")}}),Prism.hooks.add("complete",function(e){if(function(e){return"command-line"in(e.vars=e.vars||{})}(e)){var t=h(e);if(!t.complete){var n,a=e.element.parentElement;d.test(e.element.className)&&(e.element.className=e.element.className.replace(d," ")),d.test(a.className)||(a.className+=" command-line");var r=t.numberOfLines||0,s=c("data-prompt","");if(""!==s)n=p('<span data-prompt="'+s+'"></span>',r);else n=p('<span data-user="'+c("data-user","user")+'" data-host="'+c("data-host","localhost")+'"></span>',r);var o=document.createElement("span");o.className=f,o.innerHTML=n;for(var i=t.outputLines||[],l=0,m=i.length;l<m;l++)if(i.hasOwnProperty(l)){var u=o.children[l];u.removeAttribute("data-user"),u.removeAttribute("data-host"),u.removeAttribute("data-prompt")}e.element.insertBefore(o,e.element.firstChild),t.complete=!0}}function c(e,t){return(a.getAttribute(e)||t).replace(/"/g,"&quot")}})}function p(e,t){for(var n="",a=0;a<t;a++)n+=e;return n}function h(e){var t=e.vars=e.vars||{};return t["command-line"]=t["command-line"]||{}}}();