/**
  * bootstrap-table - An extended table to integration with some of the most widely used CSS frameworks. (Supports Bootstrap, Semantic UI, Bulma, Material Design, Foundation)
  *
  * @version v1.21.1
  * @homepage https://bootstrap-table.com
  * @author wenzhixin <wenzhixin2010@gmail.com> (http://wenzhixin.net.cn/)
  * @license MIT
  */

!function(t,n){"object"==typeof exports&&"undefined"!=typeof module?n(require("jquery")):"function"==typeof define&&define.amd?define(["jquery"],n):n((t="undefined"!=typeof globalThis?globalThis:t||self).jQuery)}(this,(function(t){"use strict";function n(t){return t&&"object"==typeof t&&"default"in t?t:{default:t}}var r=n(t),e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},o=function(t){return t&&t.Math==Math&&t},i=o("object"==typeof globalThis&&globalThis)||o("object"==typeof window&&window)||o("object"==typeof self&&self)||o("object"==typeof e&&e)||function(){return this}()||Function("return this")(),u={},a=function(t){try{return!!t()}catch(t){return!0}},c=!a((function(){return 7!=Object.defineProperty({},1,{get:function(){return 7}})[1]})),f=!a((function(){var t=function(){}.bind();return"function"!=typeof t||t.hasOwnProperty("prototype")})),l=f,s=Function.prototype.call,p=l?s.bind(s):function(){return s.apply(s,arguments)},y={},g={}.propertyIsEnumerable,h=Object.getOwnPropertyDescriptor,d=h&&!g.call({1:2},1);y.f=d?function(t){var n=h(this,t);return!!n&&n.enumerable}:g;var b,m,v=function(t,n){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:n}},w=f,S=Function.prototype,O=S.bind,j=S.call,P=w&&O.bind(j,j),T=w?function(t){return t&&P(t)}:function(t){return t&&function(){return j.apply(t,arguments)}},x=T,E=x({}.toString),A=x("".slice),C=function(t){return A(E(t),8,-1)},F=a,R=C,M=Object,k=T("".split),z=F((function(){return!M("z").propertyIsEnumerable(0)}))?function(t){return"String"==R(t)?k(t,""):M(t)}:M,L=TypeError,I=function(t){if(null==t)throw L("Can't call method on "+t);return t},N=z,D=I,q=function(t){return N(D(t))},H=function(t){return"function"==typeof t},U=H,G=function(t){return"object"==typeof t?null!==t:U(t)},_=i,B=H,K=function(t){return B(t)?t:void 0},Y=function(t,n){return arguments.length<2?K(_[t]):_[t]&&_[t][n]},Q=T({}.isPrototypeOf),W=i,Z=Y("navigator","userAgent")||"",J=W.process,V=W.Deno,X=J&&J.versions||V&&V.version,$=X&&X.v8;$&&(m=(b=$.split("."))[0]>0&&b[0]<4?1:+(b[0]+b[1])),!m&&Z&&(!(b=Z.match(/Edge\/(\d+)/))||b[1]>=74)&&(b=Z.match(/Chrome\/(\d+)/))&&(m=+b[1]);var tt=m,nt=tt,rt=a,et=!!Object.getOwnPropertySymbols&&!rt((function(){var t=Symbol();return!String(t)||!(Object(t)instanceof Symbol)||!Symbol.sham&&nt&&nt<41})),ot=et&&!Symbol.sham&&"symbol"==typeof Symbol.iterator,it=Y,ut=H,at=Q,ct=Object,ft=ot?function(t){return"symbol"==typeof t}:function(t){var n=it("Symbol");return ut(n)&&at(n.prototype,ct(t))},lt=String,st=H,pt=function(t){try{return lt(t)}catch(t){return"Object"}},yt=TypeError,gt=function(t){if(st(t))return t;throw yt(pt(t)+" is not a function")},ht=p,dt=H,bt=G,mt=TypeError,vt={exports:{}},wt=i,St=Object.defineProperty,Ot=function(t,n){try{St(wt,t,{value:n,configurable:!0,writable:!0})}catch(r){wt[t]=n}return n},jt=Ot,Pt="__core-js_shared__",Tt=i[Pt]||jt(Pt,{}),xt=Tt;(vt.exports=function(t,n){return xt[t]||(xt[t]=void 0!==n?n:{})})("versions",[]).push({version:"3.22.8",mode:"global",copyright:"© 2014-2022 Denis Pushkarev (zloirock.ru)",license:"https://github.com/zloirock/core-js/blob/v3.22.8/LICENSE",source:"https://github.com/zloirock/core-js"});var Et=I,At=Object,Ct=function(t){return At(Et(t))},Ft=Ct,Rt=T({}.hasOwnProperty),Mt=Object.hasOwn||function(t,n){return Rt(Ft(t),n)},kt=T,zt=0,Lt=Math.random(),It=kt(1..toString),Nt=function(t){return"Symbol("+(void 0===t?"":t)+")_"+It(++zt+Lt,36)},Dt=i,qt=vt.exports,Ht=Mt,Ut=Nt,Gt=et,_t=ot,Bt=qt("wks"),Kt=Dt.Symbol,Yt=Kt&&Kt.for,Qt=_t?Kt:Kt&&Kt.withoutSetter||Ut,Wt=function(t){if(!Ht(Bt,t)||!Gt&&"string"!=typeof Bt[t]){var n="Symbol."+t;Gt&&Ht(Kt,t)?Bt[t]=Kt[t]:Bt[t]=_t&&Yt?Yt(n):Qt(n)}return Bt[t]},Zt=p,Jt=G,Vt=ft,Xt=function(t,n){var r=t[n];return null==r?void 0:gt(r)},$t=function(t,n){var r,e;if("string"===n&&dt(r=t.toString)&&!bt(e=ht(r,t)))return e;if(dt(r=t.valueOf)&&!bt(e=ht(r,t)))return e;if("string"!==n&&dt(r=t.toString)&&!bt(e=ht(r,t)))return e;throw mt("Can't convert object to primitive value")},tn=TypeError,nn=Wt("toPrimitive"),rn=function(t,n){if(!Jt(t)||Vt(t))return t;var r,e=Xt(t,nn);if(e){if(void 0===n&&(n="default"),r=Zt(e,t,n),!Jt(r)||Vt(r))return r;throw tn("Can't convert object to primitive value")}return void 0===n&&(n="number"),$t(t,n)},en=ft,on=function(t){var n=rn(t,"string");return en(n)?n:n+""},un=G,an=i.document,cn=un(an)&&un(an.createElement),fn=function(t){return cn?an.createElement(t):{}},ln=!c&&!a((function(){return 7!=Object.defineProperty(fn("div"),"a",{get:function(){return 7}}).a})),sn=c,pn=p,yn=y,gn=v,hn=q,dn=on,bn=Mt,mn=ln,vn=Object.getOwnPropertyDescriptor;u.f=sn?vn:function(t,n){if(t=hn(t),n=dn(n),mn)try{return vn(t,n)}catch(t){}if(bn(t,n))return gn(!pn(yn.f,t,n),t[n])};var wn={},Sn=c&&a((function(){return 42!=Object.defineProperty((function(){}),"prototype",{value:42,writable:!1}).prototype})),On=G,jn=String,Pn=TypeError,Tn=function(t){if(On(t))return t;throw Pn(jn(t)+" is not an object")},xn=c,En=ln,An=Sn,Cn=Tn,Fn=on,Rn=TypeError,Mn=Object.defineProperty,kn=Object.getOwnPropertyDescriptor,zn="enumerable",Ln="configurable",In="writable";wn.f=xn?An?function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),"function"==typeof t&&"prototype"===n&&"value"in r&&In in r&&!r.writable){var e=kn(t,n);e&&e.writable&&(t[n]=r.value,r={configurable:Ln in r?r.configurable:e.configurable,enumerable:zn in r?r.enumerable:e.enumerable,writable:!1})}return Mn(t,n,r)}:Mn:function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),En)try{return Mn(t,n,r)}catch(t){}if("get"in r||"set"in r)throw Rn("Accessors not supported");return"value"in r&&(t[n]=r.value),t};var Nn=wn,Dn=v,qn=c?function(t,n,r){return Nn.f(t,n,Dn(1,r))}:function(t,n,r){return t[n]=r,t},Hn={exports:{}},Un=c,Gn=Mt,_n=Function.prototype,Bn=Un&&Object.getOwnPropertyDescriptor,Kn=Gn(_n,"name"),Yn={EXISTS:Kn,PROPER:Kn&&"something"===function(){}.name,CONFIGURABLE:Kn&&(!Un||Un&&Bn(_n,"name").configurable)},Qn=H,Wn=Tt,Zn=T(Function.toString);Qn(Wn.inspectSource)||(Wn.inspectSource=function(t){return Zn(t)});var Jn,Vn,Xn,$n=Wn.inspectSource,tr=H,nr=$n,rr=i.WeakMap,er=tr(rr)&&/native code/.test(nr(rr)),or=vt.exports,ir=Nt,ur=or("keys"),ar={},cr=er,fr=i,lr=T,sr=G,pr=qn,yr=Mt,gr=Tt,hr=function(t){return ur[t]||(ur[t]=ir(t))},dr=ar,br="Object already initialized",mr=fr.TypeError,vr=fr.WeakMap;if(cr||gr.state){var wr=gr.state||(gr.state=new vr),Sr=lr(wr.get),Or=lr(wr.has),jr=lr(wr.set);Jn=function(t,n){if(Or(wr,t))throw new mr(br);return n.facade=t,jr(wr,t,n),n},Vn=function(t){return Sr(wr,t)||{}},Xn=function(t){return Or(wr,t)}}else{var Pr=hr("state");dr[Pr]=!0,Jn=function(t,n){if(yr(t,Pr))throw new mr(br);return n.facade=t,pr(t,Pr,n),n},Vn=function(t){return yr(t,Pr)?t[Pr]:{}},Xn=function(t){return yr(t,Pr)}}var Tr={set:Jn,get:Vn,has:Xn,enforce:function(t){return Xn(t)?Vn(t):Jn(t,{})},getterFor:function(t){return function(n){var r;if(!sr(n)||(r=Vn(n)).type!==t)throw mr("Incompatible receiver, "+t+" required");return r}}},xr=a,Er=H,Ar=Mt,Cr=c,Fr=Yn.CONFIGURABLE,Rr=$n,Mr=Tr.enforce,kr=Tr.get,zr=Object.defineProperty,Lr=Cr&&!xr((function(){return 8!==zr((function(){}),"length",{value:8}).length})),Ir=String(String).split("String"),Nr=Hn.exports=function(t,n,r){"Symbol("===String(n).slice(0,7)&&(n="["+String(n).replace(/^Symbol\(([^)]*)\)/,"$1")+"]"),r&&r.getter&&(n="get "+n),r&&r.setter&&(n="set "+n),(!Ar(t,"name")||Fr&&t.name!==n)&&zr(t,"name",{value:n,configurable:!0}),Lr&&r&&Ar(r,"arity")&&t.length!==r.arity&&zr(t,"length",{value:r.arity});try{r&&Ar(r,"constructor")&&r.constructor?Cr&&zr(t,"prototype",{writable:!1}):t.prototype&&(t.prototype=void 0)}catch(t){}var e=Mr(t);return Ar(e,"source")||(e.source=Ir.join("string"==typeof n?n:"")),t};Function.prototype.toString=Nr((function(){return Er(this)&&kr(this).source||Rr(this)}),"toString");var Dr=H,qr=qn,Hr=Hn.exports,Ur=Ot,Gr={},_r=Math.ceil,Br=Math.floor,Kr=Math.trunc||function(t){var n=+t;return(n>0?Br:_r)(n)},Yr=function(t){var n=+t;return n!=n||0===n?0:Kr(n)},Qr=Yr,Wr=Math.max,Zr=Math.min,Jr=Yr,Vr=Math.min,Xr=function(t){return t>0?Vr(Jr(t),9007199254740991):0},$r=function(t){return Xr(t.length)},te=q,ne=function(t,n){var r=Qr(t);return r<0?Wr(r+n,0):Zr(r,n)},re=$r,ee=function(t){return function(n,r,e){var o,i=te(n),u=re(i),a=ne(e,u);if(t&&r!=r){for(;u>a;)if((o=i[a++])!=o)return!0}else for(;u>a;a++)if((t||a in i)&&i[a]===r)return t||a||0;return!t&&-1}},oe={includes:ee(!0),indexOf:ee(!1)},ie=Mt,ue=q,ae=oe.indexOf,ce=ar,fe=T([].push),le=function(t,n){var r,e=ue(t),o=0,i=[];for(r in e)!ie(ce,r)&&ie(e,r)&&fe(i,r);for(;n.length>o;)ie(e,r=n[o++])&&(~ae(i,r)||fe(i,r));return i},se=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"].concat("length","prototype");Gr.f=Object.getOwnPropertyNames||function(t){return le(t,se)};var pe={};pe.f=Object.getOwnPropertySymbols;var ye=Y,ge=Gr,he=pe,de=Tn,be=T([].concat),me=ye("Reflect","ownKeys")||function(t){var n=ge.f(de(t)),r=he.f;return r?be(n,r(t)):n},ve=Mt,we=me,Se=u,Oe=wn,je=a,Pe=H,Te=/#|\.prototype\./,xe=function(t,n){var r=Ae[Ee(t)];return r==Fe||r!=Ce&&(Pe(n)?je(n):!!n)},Ee=xe.normalize=function(t){return String(t).replace(Te,".").toLowerCase()},Ae=xe.data={},Ce=xe.NATIVE="N",Fe=xe.POLYFILL="P",Re=xe,Me=i,ke=u.f,ze=qn,Le=function(t,n,r,e){e||(e={});var o=e.enumerable,i=void 0!==e.name?e.name:n;return Dr(r)&&Hr(r,i,e),e.global?o?t[n]=r:Ur(n,r):(e.unsafe?t[n]&&(o=!0):delete t[n],o?t[n]=r:qr(t,n,r)),t},Ie=Ot,Ne=function(t,n,r){for(var e=we(n),o=Oe.f,i=Se.f,u=0;u<e.length;u++){var a=e[u];ve(t,a)||r&&ve(r,a)||o(t,a,i(n,a))}},De=Re,qe=C,He=Array.isArray||function(t){return"Array"==qe(t)},Ue=TypeError,Ge=on,_e=wn,Be=v,Ke={};Ke[Wt("toStringTag")]="z";var Ye="[object z]"===String(Ke),Qe=H,We=C,Ze=Wt("toStringTag"),Je=Object,Ve="Arguments"==We(function(){return arguments}()),Xe=T,$e=a,to=H,no=Ye?We:function(t){var n,r,e;return void 0===t?"Undefined":null===t?"Null":"string"==typeof(r=function(t,n){try{return t[n]}catch(t){}}(n=Je(t),Ze))?r:Ve?We(n):"Object"==(e=We(n))&&Qe(n.callee)?"Arguments":e},ro=$n,eo=function(){},oo=[],io=Y("Reflect","construct"),uo=/^\s*(?:class|function)\b/,ao=Xe(uo.exec),co=!uo.exec(eo),fo=function(t){if(!to(t))return!1;try{return io(eo,oo,t),!0}catch(t){return!1}},lo=function(t){if(!to(t))return!1;switch(no(t)){case"AsyncFunction":case"GeneratorFunction":case"AsyncGeneratorFunction":return!1}try{return co||!!ao(uo,ro(t))}catch(t){return!0}};lo.sham=!0;var so=!io||$e((function(){var t;return fo(fo.call)||!fo(Object)||!fo((function(){t=!0}))||t}))?lo:fo,po=He,yo=so,go=G,ho=Wt("species"),bo=Array,mo=function(t){var n;return po(t)&&(n=t.constructor,(yo(n)&&(n===bo||po(n.prototype))||go(n)&&null===(n=n[ho]))&&(n=void 0)),void 0===n?bo:n},vo=a,wo=tt,So=Wt("species"),Oo=function(t,n){var r,e,o,i,u,a=t.target,c=t.global,f=t.stat;if(r=c?Me:f?Me[a]||Ie(a,{}):(Me[a]||{}).prototype)for(e in n){if(i=n[e],o=t.dontCallGetSet?(u=ke(r,e))&&u.value:r[e],!De(c?e:a+(f?".":"#")+e,t.forced)&&void 0!==o){if(typeof i==typeof o)continue;Ne(i,o)}(t.sham||o&&o.sham)&&ze(i,"sham",!0),Le(r,e,i,t)}},jo=a,Po=He,To=G,xo=Ct,Eo=$r,Ao=function(t){if(t>9007199254740991)throw Ue("Maximum allowed index exceeded");return t},Co=function(t,n,r){var e=Ge(n);e in t?_e.f(t,e,Be(0,r)):t[e]=r},Fo=function(t,n){return new(mo(t))(0===n?0:n)},Ro=function(t){return wo>=51||!vo((function(){var n=[];return(n.constructor={})[So]=function(){return{foo:1}},1!==n[t](Boolean).foo}))},Mo=tt,ko=Wt("isConcatSpreadable"),zo=Mo>=51||!jo((function(){var t=[];return t[ko]=!1,t.concat()[0]!==t})),Lo=Ro("concat"),Io=function(t){if(!To(t))return!1;var n=t[ko];return void 0!==n?!!n:Po(t)};Oo({target:"Array",proto:!0,arity:1,forced:!zo||!Lo},{concat:function(t){var n,r,e,o,i,u=xo(this),a=Fo(u,0),c=0;for(n=-1,e=arguments.length;n<e;n++)if(Io(i=-1===n?u:arguments[n]))for(o=Eo(i),Ao(c+o),r=0;r<o;r++,c++)r in i&&Co(a,c,i[r]);else Ao(c+1),Co(a,c++,i);return a.length=c,a}}),r.default.fn.bootstrapTable.locales["uz-Latn-UZ"]=r.default.fn.bootstrapTable.locales.uz={formatCopyRows:function(){return"Copy Rows"},formatPrint:function(){return"Print"},formatLoadingMessage:function(){return"Yuklanyapti, iltimos kuting"},formatRecordsPerPage:function(t){return"".concat(t," qator har sahifada")},formatShowingRows:function(t,n,r,e){return void 0!==e&&e>0&&e>r?"Ko'rsatypati ".concat(t," dan ").concat(n," gacha ").concat(r," qatorlarni (filtered from ").concat(e," total rows)"):"Ko'rsatypati ".concat(t," dan ").concat(n," gacha ").concat(r," qatorlarni")},formatSRPaginationPreText:function(){return"previous page"},formatSRPaginationPageText:function(t){return"to page ".concat(t)},formatSRPaginationNextText:function(){return"next page"},formatDetailPagination:function(t){return"Showing ".concat(t," rows")},formatClearSearch:function(){return"Filtrlarni tozalash"},formatSearch:function(){return"Qidirish"},formatNoMatches:function(){return"Hech narsa topilmadi"},formatPaginationSwitch:function(){return"Sahifalashni yashirish/ko'rsatish"},formatPaginationSwitchDown:function(){return"Show pagination"},formatPaginationSwitchUp:function(){return"Hide pagination"},formatRefresh:function(){return"Yangilash"},formatToggleOn:function(){return"Show card view"},formatToggleOff:function(){return"Hide card view"},formatColumns:function(){return"Ustunlar"},formatColumnsToggleAll:function(){return"Toggle all"},formatFullscreen:function(){return"Fullscreen"},formatAllRows:function(){return"Hammasi"},formatAutoRefresh:function(){return"Auto Refresh"},formatExport:function(){return"Eksport"},formatJumpTo:function(){return"GO"},formatAdvancedSearch:function(){return"Advanced search"},formatAdvancedCloseButton:function(){return"Close"},formatFilterControlSwitch:function(){return"Hide/Show controls"},formatFilterControlSwitchHide:function(){return"Hide controls"},formatFilterControlSwitchShow:function(){return"Show controls"}},r.default.extend(r.default.fn.bootstrapTable.defaults,r.default.fn.bootstrapTable.locales["uz-Latn-UZ"])}));
