!function(){if("undefined"!=typeof Prism){var m=/^diff-([\w-]+)/i,d=/<\/?(?!\d)[^\s>\/=$<%]+(?:\s(?:\s*[^\s>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))|(?=[\s/>])))+)?\s*\/?>/g,c=RegExp("(?:__|[^\r\n<])*(?:\r\n?|\n|(?:__|[^\r\n<])(?![^\r\n]))".replace(/__/g,function(){return d.source}),"gi"),a=!1;Prism.hooks.add("before-sanity-check",function(e){var i=e.language;m.test(i)&&!e.grammar&&(e.grammar=Prism.languages[i]=Prism.languages.diff)}),Prism.hooks.add("before-tokenize",function(e){a||Prism.languages.diff||Prism.plugins.autoloader||(a=!0,console.warn("Prism's Diff Highlight plugin requires the Diff language definition (prism-diff.js).Make sure the language definition is loaded or use Prism's Autoloader plugin."));var i=e.language;m.test(i)&&!Prism.languages[i]&&(Prism.languages[i]=Prism.languages.diff)}),Prism.hooks.add("wrap",function(e){var i,a;if("diff"!==e.language){var s=m.exec(e.language);if(!s)return;i=s[1],a=Prism.languages[i]}var r=Prism.languages.diff&&Prism.languages.diff.PREFIXES;if(r&&e.type in r){var n,g=e.content.replace(d,"").replace(/&lt;/g,"<").replace(/&amp;/g,"&"),f=g.replace(/(^|[\r\n])./g,"$1");n=a?Prism.highlight(f,a,i):Prism.util.encode(f);var u,l=new Prism.Token("prefix",r[e.type],[/\w+/.exec(e.type)[0]]),t=Prism.Token.stringify(l,e.language),o=[];for(c.lastIndex=0;u=c.exec(n);)o.push(t+u[0]);/(?:^|[\r\n]).$/.test(g)&&o.push(t),e.content=o.join(""),a&&e.classes.push("language-"+i)}})}}();