"undefined"!=typeof Prism&&"undefined"!=typeof document&&document.createRange&&(Prism.plugins.KeepMarkup=!0,Prism.hooks.add("before-highlight",function(e){if(e.element.children.length&&Prism.util.isActive(e.element,"keep-markup",!0)){var o=Prism.util.isActive(e.element,"drop-tokens",!1),d=0,t=[];s(e.element),t.length&&(e.keepMarkup=t)}function r(e){if(function(e){return!o||"span"!==e.nodeName.toLowerCase()||!e.classList.contains("token")}(e)){var n={clone:e.cloneNode(!1),posOpen:d};t.push(n),s(e),n.posClose=d}else s(e)}function s(e){for(var n=0,o=e.childNodes.length;n<o;n++){var t=e.childNodes[n];1===t.nodeType?r(t):3===t.nodeType&&(d+=t.data.length)}}}),Prism.hooks.add("after-highlight",function(n){if(n.keepMarkup&&n.keepMarkup.length){var s=function(e,n){for(var o=0,t=e.childNodes.length;o<t;o++){var d=e.childNodes[o];if(1===d.nodeType){if(!s(d,n))return!1}else 3===d.nodeType&&(!n.nodeStart&&n.pos+d.data.length>n.node.posOpen&&(n.nodeStart=d,n.nodeStartPos=n.node.posOpen-n.pos),n.nodeStart&&n.pos+d.data.length>=n.node.posClose&&(n.nodeEnd=d,n.nodeEndPos=n.node.posClose-n.pos),n.pos+=d.data.length);if(n.nodeStart&&n.nodeEnd){var r=document.createRange();return r.setStart(n.nodeStart,n.nodeStartPos),r.setEnd(n.nodeEnd,n.nodeEndPos),n.node.clone.appendChild(r.extractContents()),r.insertNode(n.node.clone),r.detach(),!1}}return!0};n.keepMarkup.forEach(function(e){s(n.element,{node:e,pos:0})}),n.highlightedCode=n.element.innerHTML}}));